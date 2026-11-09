# Lab guide

Run this on a tenant and a VM you own. Do not point any test at an employer network, a customer tenant, or a machine that holds real passwords you care about.

These queries do not create Azure resources. The cost is the data you already ingest, plus anything new you turn on. Set a daily cap before you hunt.

## Time

These are planning estimates for someone who already has the Sentinel workspace from [Sentinel-Home-SOC-Lab](https://github.com/Sasa021/Sentinel-Home-SOC-Lab).

| Part | Estimate |
| --- | --- |
| Confirm the workspace, cap, and connectors | 45 to 90 minutes |
| Audit policy and a check that SecurityEvent rows arrive | 30 to 45 minutes |
| Install Atomic Red Team and take a snapshot | 30 to 45 minutes |
| One safe discovery test, plus the query and notes | 20 to 40 minutes |
| A first pass of the discovery hunts only | about 2 hours |
| Account, task, service, and Run key tests, with cleanup | about 2 hours |
| Credential dump tests | a separate sitting, after a snapshot |
| Log clearing | last, and only if you accept that the local log is gone |
| Report from the template | about 2 hours after you have real notes |

You do not have to test all 20 queries in one day. Leave Tested and Fired blank for any query you skip.

## Prerequisites

- The Microsoft Sentinel workspace from Sentinel-Home-SOC-Lab, in a subscription you control. Do not create another workspace.
- Rights on that resource group to read logs and to set a daily cap.
- A Windows 10 or Windows 11 lab VM you own. It must not be joined to an employer domain.
- Two local accounts on that VM: your admin, and a spare admin. A failed logon test must not be able to lock the only admin.
- A snapshot or checkpoint of the VM before the first atomic test. An Azure disk snapshot costs storage money. A local Hyper-V or VirtualBox snapshot uses disk space on your PC. Delete extra snapshots when the lab is finished.
- A browser signed in to the lab tenant at [https://portal.azure.com](https://portal.azure.com).
- Optional, for `DeviceProcessEvents` and `DeviceFileEvents`: Microsoft Defender for Endpoint on that VM, with advanced hunting available. Use the Defender portal at [https://security.microsoft.com](https://security.microsoft.com). Do not buy a plan for this project without reading the current price.
- Optional, for `SigninLogs`: the Microsoft Entra ID connector with Sign-in logs. If the portal says the license cannot export those logs, skip that query.

Clone this repo on a machine you use for notes. You can paste queries from the files. You do not need the repo cloned on the lab VM.

## Cost and cleanup

Read the current pages before you rely on a number. Prices change.

- Microsoft Sentinel billing: [https://learn.microsoft.com/en-us/azure/sentinel/billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)
- Azure Monitor Logs costs: [https://learn.microsoft.com/en-us/azure/azure-monitor/logs/cost-logs](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/cost-logs)

What those pages said when this guide was written:

- The Sentinel free trial waives analytics log ingestion and Sentinel analysis for the first 10 GB per day, for 31 days, with a limit of 20 workspaces per tenant. Automation, bring your own machine learning, and the Sentinel data lake can still be charged during the trial. Do not turn those on for this lab.
- After the trial, analytics logs are pay as you go unless you choose a commitment tier. Commitment tiers start at a large daily volume and lock you in for 31 days. Do not pick one for a home lab.
- The separate Log Analytics Free Trial tier caps a workspace at 500 MB per day and 7 days of retention. That is not the same offer as the Sentinel 31 day trial. Do not switch tiers until you have read the cost page.
- On analytics pay as you go, Azure Monitor currently includes 5 GB per month per billing account at no charge. Once Sentinel is enabled, Sentinel meters can replace that story. The billing article is the source of truth.

Practical rules:

1. Set a daily cap at 1 GB before you run tests. Raise it only if ingestion stops and you know why.
2. Do not stream Defender raw events into Sentinel for this project. Hunt those tables in the Defender portal.
3. Do not enable User and Entity Behavior Analytics, a data lake, or playbooks that call paid APIs.
4. Check Cost Management in the Azure portal at the end of each sitting.
5. When the whole lab is finished, remove connectors you enabled only for this repo. Do not delete the Sentinel-Home-SOC-Lab resource group if that project is still in use.
6. Delete lab users, scheduled tasks, services, Run key values, dump files, and hive copies. The cleanup commands are in [atomic-red-team-testing.md](atomic-red-team-testing.md).
7. Delete old VM snapshots so you are not paying for disks you no longer need.

Checkpoint: screenshot 2, `evidence/02-daily-cap.png`.

## 1. Confirm the Sentinel workspace

1. Open [https://portal.azure.com](https://portal.azure.com) and sign in with the lab tenant.
2. Search for **Microsoft Sentinel** and open it.
3. Select the workspace you created for Sentinel-Home-SOC-Lab.
4. If you do not see it, stop. Build it in that repo first. Do not click **Create** here.
5. Note the workspace name and resource group in your private notes. Do not commit the subscription ID.

Checkpoint: screenshot 1, `evidence/01-sentinel-workspace.png`.

## 2. Set the daily cap

1. In the Azure portal search box, open **Log Analytics workspaces**.
2. Open the same workspace Sentinel uses.
3. In the left menu, open **Usage and estimated costs**.
4. Open **Daily cap**.
5. Turn the cap on.
6. Set the cap to **1** GB.
7. Save.

If the blade is named slightly differently, use the portal search on that workspace for "daily cap". The value that matters is a cap of 1 GB per day.

Checkpoint: screenshot 2, `evidence/02-daily-cap.png`.

## 3. Confirm connectors

### Windows Security Events

1. In Microsoft Sentinel, open **Configuration**, then **Data connectors**.
2. Search for **Windows Security Events**.
3. Open the Azure Monitor Agent connector, not the legacy agent. The legacy agent is retired.
4. If the status is already Connected, leave it. That connection belongs to Sentinel-Home-SOC-Lab.
5. If it is not connected, follow the connector steps in Sentinel-Home-SOC-Lab. Do not invent a second data collection rule from this guide.

Checkpoint: screenshot 3, `evidence/03-windows-security-events-connector.png`.

### Entra ID sign-in logs

1. In **Data connectors**, search for **Microsoft Entra ID**.
2. Open the connector page.
3. Tick **Sign-in logs** only. Leave the other log types unticked. Audit logs and provisioning logs add volume you do not need for these queries.
4. Select **Apply changes**.

If the page refuses the checkbox because of a license, capture that page and skip `detections/credential-access/entra-password-spray.kql`. Do not buy Entra ID P1 only to tick a box. Write the gap in the report.

Checkpoint: screenshot 4, `evidence/04-entra-signin-connector.png`.

### Defender

Use this only for the queries whose header says `DeviceProcessEvents` or `DeviceFileEvents`.

1. Open [https://security.microsoft.com](https://security.microsoft.com).
2. Go to **Settings**, then **Endpoints**, then **Onboarding**.
3. Operating system: **Windows 10 and 11**.
4. Deployment method: **Local Script**.
5. Download the package and run it as administrator on the lab VM only.
6. Do not commit the package. It contains an organisation id. `.gitignore` is set to ignore common package names. Keep the file out of this repo anyway.
7. In the Defender portal, open **Assets**, then **Devices**, and wait until the lab VM is listed as onboarded. This can take up to an hour.

Checkpoint: screenshot 6, `evidence/06-defender-device-onboarded.png`.

Leave the Microsoft Defender XDR connector in Sentinel turned off for raw events. Incidents and alerts are optional and not required to run the `.kql` files.

## 4. Turn on the audit policy

The `SecurityEvent` queries need these Windows audit subcategories. Names below are the English Windows labels. If a command says the subcategory was not found, run `auditpol /list /subcategory:*` and use the label your language shows.

On the lab VM, open **Command Prompt** as administrator.

```bat
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"User Account Management" /success:enable /failure:enable
auditpol /set /subcategory:"Security Group Management" /success:enable /failure:enable
auditpol /set /subcategory:"Security System Extension" /success:enable
auditpol /set /subcategory:"Other Object Access Events" /success:enable
```

Check the settings:

```bat
auditpol /get /subcategory:"Logon"
auditpol /get /subcategory:"User Account Management"
auditpol /get /subcategory:"Security Group Management"
auditpol /get /subcategory:"Security System Extension"
auditpol /get /subcategory:"Other Object Access Events"
```

You want Success and Failure for Logon, User Account Management, and Security Group Management. Success is enough for Security System Extension and Other Object Access Events.

Optional, and only if you also want command lines inside `SecurityEvent` event 4688. The Defender queries do not need this.

```bat
auditpol /set /subcategory:"Process Creation" /success:enable
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit" /v ProcessCreationIncludeCmdLine_Enabled /t REG_DWORD /d 1 /f
```

Checkpoint: screenshot 5, `evidence/05-audit-policy.png`.

### Confirm events are arriving

Lock and unlock the lab VM, or sign out and back in. Wait 10 to 15 minutes. In Sentinel, open **Logs**, set the time range to **Last 24 hours**, and run:

```kql
SecurityEvent
| where TimeGenerated > ago(1d)
| where EventID in (4624, 4625)
| summarize Events = count() by EventID, Computer
| order by Events desc
```

This check is not one of the detection files. If it returns no rows, stop. Fix the data collection rule before you run Atomic Red Team. Do not paste a number you did not see.

## 5. Where to run each query

Set the time picker to **Last 7 days** every time. The picker can hide rows even when the query says `ago(1d)`.

| Header `data_source` | Where to paste the file |
| --- | --- |
| `SecurityEvent` | Sentinel, **Logs**, on the Sentinel-Home-SOC-Lab workspace |
| `SigninLogs` | Sentinel, **Logs**, same workspace |
| `DeviceProcessEvents` | Defender portal, **Hunting**, **Advanced hunting** |
| `DeviceFileEvents` | Defender portal, **Hunting**, **Advanced hunting** |

In Sentinel: **General**, **Logs**. Paste the whole file, including the comments. Select **Run**.

In Defender: **Hunting**, **Advanced hunting**. Paste the query. Set the time range to 7 days. Select **Run query**.

Checkpoint: screenshot 7, `evidence/07-sentinel-query.png`, and screenshot 8, `evidence/08-defender-hunting-query.png`.

Sign-in logs can lag 15 to 30 minutes, sometimes longer. Security events through the Azure Monitor Agent are often visible within 15 minutes. If the first run is empty, wait and run it once more before you write "did not fire".

## 6. Run tests

Follow [atomic-red-team-testing.md](atomic-red-team-testing.md) for install, snapshot, one test at a time, and cleanup.

Suggested order, safest first:

1. T1082-1 system information, then `detections/discovery/system-information-discovery.kql`.
2. T1057-2 tasklist, then `detections/discovery/process-discovery.kql`.
3. T1049-1 netstat, then `detections/discovery/network-connection-discovery.kql`.
4. T1087.001-8 local accounts, then `detections/discovery/local-account-discovery.kql`.
5. Encoded PowerShell, manual command in the atomic guide if the harness does not spawn `powershell.exe`. Then `detections/execution/encoded-powershell.kql`.
6. T1105-10 download of the Atomic Red Team license file, or the manual `powershell.exe` line in the atomic guide. Then `detections/command-and-control/powershell-webclient-download.kql`.
7. T1074.001-3 zip into Temp. Then `detections/collection/archive-staged-in-temp.kql`.
8. T1136.001-4 new local user. Then `detections/persistence/new-local-user.kql`. Run cleanup.
9. T1136.001-8 new local admin. Then `detections/persistence/local-administrators-member-added.kql`. Run cleanup. This test also creates a user, so 4720 can fire as well.
10. T1053.005-1 scheduled tasks. Then `detections/persistence/scheduled-task-created.kql`. Delete the tasks before you restart. They start `calc.exe`.
11. T1547.001-1 Run key. Then `detections/persistence/registry-run-key.kql`. Run cleanup.
12. Service create. Prefer the manual `sc.exe` command in the atomic guide so you do not download a binary. Then `detections/persistence/windows-service-created.kql`. Delete the service.
13. Manual failed logons for `detections/credential-access/windows-failed-logon-brute-force.kql`. Steps are below. Do not aim T1110.001-1 at a domain controller.
14. Manual Entra sign-in failures for `detections/credential-access/entra-password-spray.kql`, and only if screenshot 4 shows the connector is allowed.
15. T1021.001-1 RDP attempt to `127.0.0.1`. Then `detections/lateral-movement/rdp-logon.kql`. Run cleanup and check `cmdkey /list`.
16. T1003.002-1 registry hive save. Then `detections/credential-access/sam-hive-save.kql`. Delete the files in `%temp%` in the same sitting.
17. T1003.001-2 comsvcs LSASS dump. Then `detections/credential-access/lsass-memory-dump.kql`. Delete the dump. Skip this if you do not want credential material on the VM. Leaving the query untested is acceptable.
18. T1685-19 Defender real time protection. Then `detections/defense-impairment/defender-realtime-protection-disabled.kql`. Run the cleanup immediately and confirm Windows Security shows protection on.
19. T1685.005-1 clear the System log. Then `detections/defense-impairment/wevtutil-clear-event-log.kql`. There is no undo.
20. Optional: the same clear test with `log_name` set to `Security`, only after Sentinel already has the events you need. Then `detections/defense-impairment/security-audit-log-cleared.kql`.

After each test, fill one row in your notes: query path, time, fired or not, evidence file. Update [detections-index.md](../detections-index.md) only for that query.

Checkpoints: screenshots 9 to 14.

### Manual failed logons

Use this instead of a domain brute force. It creates Event ID 4625 on the lab VM.

Create a standard user. The `*` makes Windows prompt for a password, so the password is not stored in this file.

```bat
net user labguess * /add
```

Then run this at least five times within ten minutes. It should fail.

```bat
net use \\127.0.0.1\IPC$ /user:%COMPUTERNAME%\labguess WrongPassword
```

Wait for ingestion, with the Sentinel time range on **Last 7 days**, and run `detections/credential-access/windows-failed-logon-brute-force.kql`. The starter threshold is 5.

Cleanup:

```bat
net use \\127.0.0.1\IPC$ /delete
net user labguess /delete
```

If the first cleanup command says the connection does not exist, that is fine. Do not run the failed logon against your admin account.

### Manual Entra password spray check

Do not run Atomic Red Team T1110.003. Those tests try a password against many or all accounts. Use two lab users and one wrong password each.

1. Open [https://entra.microsoft.com](https://entra.microsoft.com).
2. Go to **Users**, **New user**, **Create new user**.
3. Create `lab.spray1` and `lab.spray2` on your lab domain. Give them no directory roles.
4. Set a password you do not use anywhere else.
5. In a private browser window, open [https://portal.azure.com](https://portal.azure.com).
6. Try `lab.spray1` with a wrong password once.
7. Within a few minutes, on the same network, try `lab.spray2` with a wrong password once.
8. Stop. Do not use a word list. Do not target any other account.
9. Wait, then run `detections/credential-access/entra-password-spray.kql`.

The starter rule needs two users and two failures from the same IP in the same 15 minute bin. If the tries are far apart, or leave from different networks, the query can correctly return nothing. Record that.

Cleanup: block sign-in for both users, then delete them.

## 7. Record what happened

- A row that matches the test: set Fired to `yes` and point at the screenshot.
- A query that returns no rows after you waited: set Fired to `no`. Keep the empty screenshot.
- A query you did not run: leave both cells blank.
- Change `status: untested` to `status: tested` in the `.kql` file only after you ran it.
- Replace the `PLACEHOLDER` tuning note with the threshold or exclusion you actually kept. If you changed nothing, write that you kept the starter values and why.

Checkpoint: screenshot 15, `evidence/15-detections-index.png`.

Copy [report-template.md](report-template.md) to a new file such as `docs/lab-report.md` when you are ready to write the report. Do not fill the template with example findings.

## 8. Close the lab for the day

1. Run cleanup for every test you started. Confirm Defender real time protection is on if you touched it.
2. Delete dump files and registry hive copies from `%temp%`.
3. Delete lab users you created.
4. Confirm scheduled tasks `T1053_005_OnLogon` and `T1053_005_OnStartup` are gone before you shut down.
5. Glance at **Usage and estimated costs** and at Azure Cost Management.
6. Keep the daily cap on.

If the VM misbehaves after a LSASS test, restore the snapshot. Do not keep hunting on a broken image.
