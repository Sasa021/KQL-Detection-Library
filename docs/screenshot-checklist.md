# Screenshot checklist

Take these yourself. Do not download a sample image and do not edit a row into an empty result.

Save the files in `evidence/` with the names below. Read [evidence/README.md](../evidence/README.md) before you commit them. Redact IP addresses, tenant IDs, subscription IDs, workspace IDs, email addresses, and secrets.

If you skip a step, do not create a fake image. Write one sentence in the report that says you skipped it and why.

1. **`evidence/01-sentinel-workspace.png`**
   Microsoft Sentinel overview for the workspace from Sentinel-Home-SOC-Lab. The workspace name and resource group must be readable. Cover the subscription ID and tenant ID.

2. **`evidence/02-daily-cap.png`**
   Log Analytics workspace, Usage and estimated costs, with the daily cap turned on. The cap value must be readable.

3. **`evidence/03-windows-security-events-connector.png`**
   The Windows Security Events data connector page. The status must be visible (Connected, or the exact status the portal shows if it is not connected).

4. **`evidence/04-entra-signin-connector.png`**
   The Microsoft Entra ID connector page with the Sign-in logs checkbox visible. If the tenant cannot export sign-in logs, capture the message that says so. That is a real result.

5. **`evidence/05-audit-policy.png`**
   Administrator command prompt on the lab VM showing `auditpol /get` for Logon, User Account Management, Security Group Management, and Security System Extension. Success and Failure settings must be readable.

6. **`evidence/06-defender-device-onboarded.png`**
   Defender portal device inventory with the lab VM onboarded. Cover any tenant or user email in the corner. If you are not using Defender for this lab, skip this file and say so in the report.

7. **`evidence/07-sentinel-query.png`**
   Sentinel Logs with one `.kql` file pasted in full, the time range set to Last 7 days, and the Run control visible. The result grid can be empty if you have not run the matching test yet. The query file name must be written in the report next to this shot.

8. **`evidence/08-defender-hunting-query.png`**
   Defender XDR advanced hunting with a `DeviceProcessEvents` or `DeviceFileEvents` query visible and the time range visible. Skip this file if the lab VM is not onboarded, and say so in the report.

9. **`evidence/09-atomic-showdetails.png`**
   `Invoke-AtomicTest` with `-ShowDetails` for one test, before you run it. The technique ID, test number, and test name must be readable.

10. **`evidence/10-atomic-prereqs.png`**
    `-CheckPrereqs` output for that same test. If there are no prerequisites, the command output saying so is enough.

11. **`evidence/11-atomic-execution.png`**
    The test running on the lab VM. Cover any password the tool prints. Prefer a test from the safe list in [atomic-red-team-testing.md](atomic-red-team-testing.md).

12. **`evidence/12-query-after-test.png`**
    The matching query after the test, with the time range visible. If a row fired, the computer name and the command line or event ID must be visible, with IPs and emails covered. If no row fired, keep the empty grid. Do not add a row in an editor.

13. **`evidence/13-empty-result.png`**
    A query in a window where you did not perform the matching action, or a query you expected to stay quiet. The empty grid and the query text must both be visible. Write the file name of the query in the report.

14. **`evidence/14-atomic-cleanup.png`**
    Cleanup output for the test in screenshot 11, plus a check that the change is gone. Examples: `net user` no longer lists the lab account, `schtasks /query` does not list the test task, or Windows Security shows real time protection on again.

15. **`evidence/15-detections-index.png`**
    `detections-index.md` after you have filled Tested and Fired only for queries you actually ran. Blank cells must still be blank for the queries you did not run.
