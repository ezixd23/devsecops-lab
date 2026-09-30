# Decisions Log

## Checkov findings on `insecure-example.tf` — accepted for now

Checkov found 12 issues on the example Azure storage account. 3 were introduced
intentionally to validate the scanner works (public blob access, outdated TLS,
open network rules by default) and have since been fixed. A 4th finding
(blob anonymous access) was resolved as a side effect of those fixes.

The remaining 8 findings are accepted as known, not fixed, at this stage:

- CKV_AZURE_33 — queue service logging not enabled
- CKV_AZURE_59 — public network access not fully disabled (network rules
  restrict *which* IPs can connect, but the public endpoint itself still exists)
- CKV_AZURE_206 — storage replication below GRS
- CKV2_AZURE_40 — Shared Key authorization still allowed
- CKV2_AZURE_41 — no SAS expiration policy configured
- CKV2_AZURE_1 — no customer-managed key encryption
- CKV2_AZURE_38 — soft-delete not enabled
- CKV2_AZURE_33 — no private endpoint configured

**Reason:** this is a standalone example resource, not tied to a real workload
yet. Several of these (private endpoint, CMK, fully disabling public access)
require networking infrastructure not yet built in this lab. Will revisit once
a real resource holding actual data is provisioned.
## Container image: hardening decisions and accepted risks

### What changed and how it was measured

The first image (`python:3.12`) was scanned with Trivy and then replaced by a hardened one
(`python:3.12-slim`, multi-stage build, non-root user with numeric UID 10001).

| | Unoptimized | Hardened |
|---|---|---|
| Size on disk | 1.63 GB | 189 MB |
| HIGH/CRITICAL findings (all) | 354 | not measured |
| HIGH/CRITICAL with a fix available | 60 (3 CRITICAL) | 6 (0 CRITICAL) |

The 3 CRITICAL findings were all in one OS package (`libunbound8`), which the application
does not use. The hardened image fixed them by not having the package at all.

### Gate policy

The pipeline fails on CRITICAL findings that have a fix available (`ignore-unfixed`).
HIGH findings do not block yet. Reason: a gate must be actionable. Blocking on findings
nobody can fix today teaches the team to ignore the gate.

### Accepted risks (known, not fixed in this phase)

- **6 HIGH findings in OpenSSL** (CVE-2026-75804, CVE-2026-84782), reported on `libssl3t64`,
  `openssl` and `openssl-provider-legacy`. Fixed upstream in `3.5.7-1~deb13u3`, but the base
  image had not been rebuilt yet. Exposure is believed to be low because the issues affect
  QUIC and DTLS, which the app does not use. This is an assumption, not a reachability
  analysis. Revisit when the base image is rebuilt.
- **Flask development server** is used as the container command. It is not meant for
  production. A WSGI server such as gunicorn would replace it before any real deployment.
- **Base image tag is mutable and there is no scheduled rebuild.** `python:3.12-slim` can
  change under the same tag, so builds are not fully reproducible. Planned: pin the image by
  digest and rebuild on a schedule to pick up OS patches.
