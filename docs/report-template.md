# Detection lab report

Replace every PLACEHOLDER with your own notes. Delete any section you did not do, and write one line that says you skipped it. Do not invent rows, counts, or host names.

| Field | Your answer |
| --- | --- |
| Author | PLACEHOLDER |
| Date | PLACEHOLDER |
| Lab repo | https://github.com/Sasa021/KQL-Detection-Library |
| Sentinel lab | https://github.com/Sasa021/Sentinel-Home-SOC-Lab |
| Workspace name | PLACEHOLDER |
| Azure region | PLACEHOLDER |
| Lab VM name | PLACEHOLDER |
| Windows version | PLACEHOLDER |

## 1. Purpose

PLACEHOLDER. One short paragraph on what you wanted to show. A useful version says you wrote KQL, mapped it to ATT&CK, and checked it on your own lab VM.

## 2. Scope

In scope:

- Your lab tenant and the Sentinel workspace from Sentinel-Home-SOC-Lab.
- Your lab VM.
- The queries you actually ran.

Out of scope:

- Any employer or customer tenant.
- Production data.
- Queries you left blank in `detections-index.md`.

## 3. Environment

PLACEHOLDER. Record the connectors that were connected, the daily cap you set, and whether Defender advanced hunting was available. If Entra sign-in export was blocked by a license, say that here. Do not paste tenant IDs, subscription IDs, or workspace IDs.

## 4. Cost and cleanup

PLACEHOLDER. Say whether you saw charges in Cost Management, whether the daily cap stayed on, and which lab accounts, tasks, services, and files you removed. If you restored a snapshot, say so.

## 5. Tests

One row per test you performed. Leave the table empty until then. Add rows. Do not fill them with guesses.

| Query file | ATT&CK | Action you ran | Time range you used | Fired (yes/no) | Evidence file |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 6. Results

PLACEHOLDER. For each `yes`, describe the row in your own words: event ID or file name, account, and computer. Cover IPs and emails. For each `no`, say how long you waited and what you would check next. An empty result is allowed.

Do not paste a screenshot that is not in `evidence/`.

## 7. False positives you saw

PLACEHOLDER. Only list noise you actually observed. If you saw none, write that you did not judge false positives yet, because the lab window was short.

## 8. Lessons learned

PLACEHOLDER. Answer these in your own words:

- Which hunt was too noisy to alert on?
- Which test failed to show up, and what might explain it?
- What would you change in a threshold or an exclusion?
- Which atomic test should a later student skip?

## 9. What I would tell a hiring manager

PLACEHOLDER. Three to six sentences. Stick to what you ran. Do not say the library detected an intrusion.

## Appendix

List the evidence files you committed. Example format, with your real file names only:

- `evidence/01-sentinel-workspace.png`: workspace overview, subscription covered.
