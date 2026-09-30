Per Ars Technica, Cloudflare plans to issue quantum-safe TLS certificates. The story reached the list through a single Mastodon post linking the article, so published detail is thin, but the direction is what matters: certificate issuance moving to quantum-resistant algorithms is the step that closes the retroactive decryption window for TLS traffic, since sessions recorded today are only breakable later if the certificates and key exchange protecting them eventually fall to a quantum computer.

Cloudflare terminates a large share of the web's TLS, so its issuance defaults tend to propagate to the rest of the ecosystem quickly.

Watch the rollout timeline, how browsers and client libraries handle the new certificates in practice, and whether other large certificate authorities match the move.
