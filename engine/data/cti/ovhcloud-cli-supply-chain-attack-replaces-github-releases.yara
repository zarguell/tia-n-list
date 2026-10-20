rule OVHcloud_CLI_Trojanized_Dirty_Release_Build
{
    meta:
        author = "Tia N. List"
        date = "2026-10-20"
        status = "experimental"
        description = "OVHcloud CLI release binaries replaced by the GlassWorm-linked actor were compiled from a dirty local checkout rather than GoReleaser, leaving the pseudo-version v0.15.1-0.20261013083505-5ead8ef9b43d+dirty and vcs.modified=true in the Go build info. Derived from case analysis (GitHub issue ovh/ovhcloud-cli#300) - NOT validated against a live sample."
        reference = "https://github.com/ovh/ovhcloud-cli/issues/300"
        falsepositives = "Any Go binary built from an uncommitted checkout of ovhcloud-cli for development; the embedded +dirty pseudo-version is the high-confidence anchor for the campaign build"
    strings:
        $pseudo = "v0.15.1-0.20261013083505-5ead8ef9b43d+dirty" ascii
        $vcs_modified = "vcs.modified=true" ascii
        $module = "github.com/ovh/ovhcloud-cli" ascii
    condition:
        $pseudo or ($vcs_modified and $module)
}
