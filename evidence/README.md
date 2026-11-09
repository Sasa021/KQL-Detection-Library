# Evidence

This folder is where you put proof from your own lab. Nothing in this folder yet is a finding. Do not add a screenshot until it comes from a test you ran.

## Redact before you commit

Screenshots and exports often contain identifiers you should not publish.

Remove or cover all of the following before a file goes into git:

- Public and private IP addresses
- Tenant IDs and subscription IDs
- Workspace IDs and agent IDs
- Email addresses and user principal names
- Passwords, tokens, keys, and connection strings
- Employee names that are not you, and any data from a real organisation

A lab username you created, such as `labguess`, can stay if it identifies the test. Your own admin account name is your choice. When you are unsure, cover it.

Do not commit memory dumps, registry hive copies, packet captures, or raw `.evtx` files. Those can contain passwords and other secrets. `.gitignore` ignores `evidence/raw/`, `evidence/unredacted/`, `*.dmp`, `*.evtx`, and `*.pcap` for that reason.

The Defender onboarding package contains an organisation id. Keep it on the lab VM. Do not put it in this repo.

## File names

Use the names in [docs/screenshot-checklist.md](../docs/screenshot-checklist.md). Example: `evidence/01-sentinel-workspace.png`.

If a shot shows a secret you missed, delete it from git history is harder than deleting the file before the first commit. Check the image at full size before you add it.

## Empty is a valid result

A query that returns no rows is still evidence, if the screenshot shows the query text, the time range, and the empty grid. Write that outcome in the report. Do not edit the image to add a row.
