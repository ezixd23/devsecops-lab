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