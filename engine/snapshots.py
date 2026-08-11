#!/usr/bin/env python3
"""Tia N. List — daily STIX snapshots (tier 4).

Immutable daily bundles: /cti/snapshots/YYYY-MM-DD/ with the full STIX 2.1
bundle (curated IOCs as indicators + CTI records as ThreatActor/Malware/
Campaign objects), the IOC feeds in all formats, and a manifest with per-file
sha256 for pin-ability. A 'latest' pointer names the newest snapshot.

Determinism: all timestamps are date-level (no clock time), so a same-day
rebuild produces byte-identical files and the manifest hash is stable within
the day. Snapshots are immutable — a given date is never rewritten with
different content; the next day starts a new directory.
"""
import hashlib
import json
import os
import uuid
from datetime import datetime, timedelta, timezone

TTL_DAYS = 30


def _day(date_str):
    """Date-level ISO timestamp (deterministic within a day)."""
    return date_str + "T00:00:00Z"


def _valid_until(i, date_str):
    """STIX valid_until: last_seen + TTL for active IOCs (matching the status
    model), last_seen for expired/revoked (self-expired at observation end)."""
    last = i["last_seen"] or date_str
    if i["status"] == "active":
        d = datetime.fromisoformat(last + "T00:00:00Z") + timedelta(days=TTL_DAYS)
        return d.strftime("%Y-%m-%d") + "T00:00:00Z"
    return _day(last)


def _stix_id(kind, seed):
    return f"{kind}--{uuid.uuid5(uuid.NAMESPACE_URL, seed)}"


def build_bundle(iocs, records, base_url, date_str):
    """Full STIX 2.1 bundle: identity + indicators (curated IOCs) + objects
    from the CTI records (threat actors, malware, campaigns), all date-anchored."""
    identity = _stix_id("identity", "https://tia-n-list/")
    objects = [{
        "type": "identity", "spec_version": "2.1", "id": identity,
        "name": "Tia N. List", "identity_class": "organization",
        "created": _day(date_str), "modified": _day(date_str),
        "description": "Daily threat intelligence and detection content from Tia N. List coverage.",
    }]
    # curated indicators
    for i in iocs:
        if i["type"] == "ipv4":
            pattern = f"[ipv4-addr:value = '{i['value']}']"
        elif i["type"] == "domain":
            pattern = f"[domain-name:value = '{i['value']}']"
        else:
            pattern = f"[file:hashes.SHA-256 = '{i['value']}']"
        objects.append({
            "type": "indicator", "spec_version": "2.1",
            "id": _stix_id("indicator", "https://tia-n-list/ioc/" + i["value"]),
            "created": _day(i["first_seen"] or date_str),
            "modified": _day(i["last_seen"] or date_str),
            "name": f"{i['value']} ({i['type']})",
            "pattern": pattern,
            "valid_from": _day(i["first_seen"] or date_str),
            "valid_until": _valid_until(i, date_str),
            "labels": ["malicious-activity"],
            "confidence": 70 if i["confidence"] == "corroborated" else 40,
            "x_tia_status": i["status"],
            "x_tia_confidence": i["confidence"],
            "external_references": [{
                "source_name": "Tia N. List",
                "url": base_url + f"cti/iocs/?q={i['value']}",
            }],
        })
    # CTI records -> STIX objects (malware / campaigns / threat actors)
    for sid, r in records.items():
        created = (r.get("updated_at") or date_str + "T00:00:00Z")[:10]
        refs = [{"source_name": "Tia N. List",
                 "url": base_url + f"cti/{sid}/"}]
        for t in r.get("attack", []):
            refs.append({"source_name": "MITRE ATT&CK", "external_id": t["id"]})
        common = {"spec_version": "2.1", "created": _day(created),
                  "modified": _day(created), "external_references": refs,
                  "labels": [t["id"] for t in r.get("attack", [])]}
        for name in r.get("malware", []):
            objects.append({
                "type": "malware", "id": _stix_id("malware", f"https://tia-n-list/malware/{sid}/{name}"),
                "name": name, "is_family": False, "confidence": 70 if r.get("confidence") == "reviewed" else 40,
                **common})
        for name in r.get("campaigns", []):
            objects.append({
                "type": "campaign", "id": _stix_id("campaign", f"https://tia-n-list/campaign/{sid}/{name}"),
                "name": name, **common})
        for name in r.get("actors", []):
            objects.append({
                "type": "threat-actor", "id": _stix_id("threat-actor", f"https://tia-n-list/actor/{sid}/{name}"),
                "name": name, "threat_actor_types": ["threat-actor"], **common})
    objects.sort(key=lambda o: (o["type"], o.get("name", "")))
    return {
        "type": "bundle", "id": _stix_id("bundle", "https://tia-n-list/snapshot/" + date_str),
        "spec_version": "2.1", "objects": objects,
    }


def _sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write_snapshot(iocs, records, base_url, out_dir, date_str):
    """Write the daily snapshot directory; returns the manifest dict."""
    os.makedirs(out_dir, exist_ok=True)
    bundle = build_bundle(iocs, records, base_url, date_str)
    iocs_json = json.dumps(iocs, indent=1)
    iocs_csv = _to_csv(iocs)
    iocs_txt = "".join(f"{i['type']}:{i['value']}\n" for i in iocs) + "\n"
    files = {
        "stix-bundle.json": json.dumps(bundle, indent=1),
        "iocs.json": iocs_json,
        "iocs.csv": iocs_csv,
        "iocs.txt": iocs_txt,
    }
    manifest = {"date": date_str, "generated": date_str, "files": {},
                "counts": {
                    "iocs": len(iocs),
                    "by_type": {t: sum(1 for i in iocs if i["type"] == t)
                                for t in ("ipv4", "domain", "sha256")},
                    "stix_objects": len(bundle["objects"]),
                    "cti_records": len(records),
                }}
    for name, text in files.items():
        with open(os.path.join(out_dir, name), "w") as f:
            f.write(text)
        manifest["files"][name] = {"bytes": len(text), "sha256": _sha256(text)}
    manifest_text = json.dumps(manifest, indent=1)
    manifest["files"]["manifest.json"] = {
        "bytes": len(manifest_text), "sha256": _sha256(manifest_text)}
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    return manifest


def _to_csv(iocs):
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["value", "type", "first_seen", "last_seen", "status",
                "confidence", "n_sources", "stories"])
    for i in iocs:
        w.writerow([i["value"], i["type"], i["first_seen"], i["last_seen"],
                    i["status"], i["confidence"], i["n_sources"],
                    " ".join(i["stories"])])
    return buf.getvalue()


def list_snapshots(snapshots_root):
    """[(date, manifest)] for existing snapshot dirs, newest first."""
    out = []
    if not os.path.isdir(snapshots_root):
        return out
    for d in sorted(os.listdir(snapshots_root), reverse=True):
        m = os.path.join(snapshots_root, d, "manifest.json")
        if os.path.exists(m):
            out.append((d, json.load(open(m))))
    return out
