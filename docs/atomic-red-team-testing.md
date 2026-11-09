# Atomic Red Team on the lab VM

Atomic Red Team runs small tests that look like attacker techniques. Use it only on the Windows lab VM you own. One test number at a time. Then clean up that test before you start another.

The test numbers below were taken from the Atomic Red Team `master` branch while this repo was scaffolded. The project inserts tests, and numbers move. Before you run anything, confirm the test name with `-ShowDetails`. The name column lists the words you should see. The on screen title sometimes puts a hyphen between those words. If the words do not match, stop. Do not guess a different number.

Do not run `Invoke-AtomicTest All`.

## Where this is allowed

- One lab VM you control.
- A local account you created for the test.
- Your own lab tenant, and only for the two user sign-in check in the lab guide. That check is manual. It is not an Atomic spray.

## Where this is not allowed

- A work laptop, a family PC, or a server anyone else uses.
- A machine joined to an employer domain.
- Any host you do not own. If `-ShowDetails` shows a domain controller, a remote computer, or "all users", do not run it.
- Any tenant that contains accounts you did not create for this lab.

Take a snapshot first. An Azure managed disk snapshot adds storage cost. Delete it when you no longer need the rollback point. A local virtual machine checkpoint uses disk space on the PC that hosts the VM.

## Install

Do this on the lab VM, in an elevated PowerShell window. Read the installer in a browser before you run it:

[https://github.com/redcanaryco/invoke-atomicredteam/wiki/Installing-Atomic-Red-Team](https://github.com/redcanaryco/invoke-atomicredteam/wiki/Installing-Atomic-Red-Team)

```powershell
Set-ExecutionPolicy -Scope Process Bypass
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1')
Install-AtomicRedTeam -getAtomics
```

The default folder is `C:\AtomicRedTeam`. If the installer prints a different path, use that path. Import the module in each new window:

```powershell
Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1" -Force
```

## How to run one test

Replace the technique and the number. Keep `-ShowDetails` first.

```powershell
Invoke-AtomicTest T1082 -TestNumbers 1 -ShowDetails
Invoke-AtomicTest T1082 -TestNumbers 1 -CheckPrereqs
Invoke-AtomicTest T1082 -TestNumbers 1
Invoke-AtomicTest T1082 -TestNumbers 1 -Cleanup
```

Run `-GetPrereqs` only after `-CheckPrereqs` says something is missing, and only after you have read what it downloads. Several tests download binaries. You can skip those and use the manual command in this file instead.

Some PowerShell tests run inside the Atomic window. Defender then logs the Atomic process, not the technique command. When a `DeviceProcessEvents` query stays empty, run the manual line in this file. It starts a new `powershell.exe`, which is the process the query looks for.

Checkpoints for the first test you keep: screenshots 9, 10, 11, 12, and 14 in [screenshot-checklist.md](screenshot-checklist.md).

## Tests that match the queries

| Query | Command | Name you must see in ShowDetails |
| --- | --- | --- |
| `detections/discovery/system-information-discovery.kql` | `Invoke-AtomicTest T1082 -TestNumbers 1` | System Information Discovery |
| `detections/discovery/process-discovery.kql` | `Invoke-AtomicTest T1057 -TestNumbers 2` | Process Discovery, tasklist |
| `detections/discovery/network-connection-discovery.kql` | `Invoke-AtomicTest T1049 -TestNumbers 1` | System Network Connections Discovery |
| `detections/discovery/local-account-discovery.kql` | `Invoke-AtomicTest T1087.001 -TestNumbers 8` | Enumerate all accounts on Windows (Local) |
| `detections/execution/encoded-powershell.kql` | `Invoke-AtomicTest T1059.001 -TestNumbers 15` | ATHPowerShellCommandLineParameter -EncodedCommand parameter variations |
| `detections/command-and-control/powershell-webclient-download.kql` | `Invoke-AtomicTest T1105 -TestNumbers 10` | Windows PowerShell Download |
| `detections/collection/archive-staged-in-temp.kql` | `Invoke-AtomicTest T1074.001 -TestNumbers 3` | Zip a Folder with PowerShell for Staging in Temp |
| `detections/persistence/new-local-user.kql` | `Invoke-AtomicTest T1136.001 -TestNumbers 4` | Create a new user in a command prompt |
| `detections/persistence/local-administrators-member-added.kql` | `Invoke-AtomicTest T1136.001 -TestNumbers 8` | Create a new Windows admin user |
| `detections/persistence/scheduled-task-created.kql` | `Invoke-AtomicTest T1053.005 -TestNumbers 1` | Scheduled Task Startup Script |
| `detections/persistence/windows-service-created.kql` | `Invoke-AtomicTest T1543.003 -TestNumbers 2` | Service Installation CMD |
| `detections/persistence/registry-run-key.kql` | `Invoke-AtomicTest T1547.001 -TestNumbers 1` | Reg Key Run |
| `detections/defense-impairment/wevtutil-clear-event-log.kql` | `Invoke-AtomicTest T1685.005 -TestNumbers 1` | Clear Logs |
| `detections/defense-impairment/security-audit-log-cleared.kql` | see below | Clear Logs |
| `detections/defense-impairment/defender-realtime-protection-disabled.kql` | `Invoke-AtomicTest T1685 -TestNumbers 19` | Tamper with Windows Defender ATP PowerShell |
| `detections/credential-access/sam-hive-save.kql` | `Invoke-AtomicTest T1003.002 -TestNumbers 1` | Registry dump of SAM, creds, and secrets |
| `detections/credential-access/lsass-memory-dump.kql` | `Invoke-AtomicTest T1003.001 -TestNumbers 2` | Dump LSASS.exe Memory using comsvcs.dll |
| `detections/lateral-movement/rdp-logon.kql` | `Invoke-AtomicTest T1021.001 -TestNumbers 1` | RDP to Remote Host |
| `detections/credential-access/windows-failed-logon-brute-force.kql` | do not use the stock test | see manual steps in the lab guide |
| `detections/credential-access/entra-password-spray.kql` | do not run this atomic | see manual steps in the lab guide |

T1110.001 test 1 tries SMB passwords against `%logonserver%`. On a domain joined PC that can be a domain controller. Use the manual `net use` steps in the lab guide instead, aimed at `127.0.0.1` and the user `labguess`.

T1110.003 test 4, and the other spray tests under T1110.003, try a password across many accounts. Do not run them. Two manual failed sign-ins, on two lab users, are enough for the starter query.

## Do not run these

- `Invoke-AtomicTest All`, or any technique with no `-TestNumbers`.
- T1110.003 in full. It is a password spray.
- T1098 test 2, Domain Account and Group Manipulate. The default group is Domain Admins.
- T1136.001 test 9. It downloads a remote script. Tests 4 and 8 are the local `net user` tests.
- T1003.001 tests that use Mimikatz (test 6 and test 10 when this file was written). Test 2 uses `comsvcs.dll`, which is already on Windows. It still dumps LSASS. Skip it if you do not want that file on disk.
- T1685.005 test 4, BlackCat Ransomware Full Log Clear. It clears every log. Test 1 clears one log. That is the only clear test to consider.
- T1543.003 tests that install a service on a remote computer. Test 2 is local. The manual `sc.exe` command below avoids the download.
- Any test whose details mention ESXi, AWS, Azure roles, or a domain controller, unless the target is a lab you built for that purpose. This repo does not use those tests.

## Manual commands when the atomic is a poor fit

Run these on the lab VM. They exist so the process command line is visible, or so you can avoid a download.

Encoded PowerShell. The text it runs is `Write-Output "lab encoded command test"`.

```powershell
$bytes = [System.Text.Encoding]::Unicode.GetBytes('Write-Output "lab encoded command test"')
$encoded = [Convert]::ToBase64String($bytes)
powershell.exe -NoProfile -EncodedCommand $encoded
```

Download of the Atomic Red Team license file, then delete it:

```powershell
powershell.exe -NoProfile -Command "(New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/LICENSE.txt', \"$env:TEMP\Atomic-license.txt\")"
Remove-Item "$env:TEMP\Atomic-license.txt" -Force -ErrorAction Ignore
```

Local service that points at `cmd.exe`. `sc.exe` requires the space after `binPath=`.

```bat
sc.exe create LabSvc binPath= "C:\Windows\System32\cmd.exe" start= demand
sc.exe delete LabSvc
```

Defender, in a new process, then turn it back on in the same sitting. Leave Tamper Protection on. If Windows blocks the change, record the error. That is a result. Then run the second command anyway.

```powershell
powershell.exe -NoProfile -Command "Set-MpPreference -DisableRealtimeMonitoring 1"
powershell.exe -NoProfile -Command "Set-MpPreference -DisableRealtimeMonitoring 0"
```

Open Windows Security and confirm the setting labelled **Real-time protection** is On.

Security log clear, only as the last test, and only if Sentinel already has the events you need:

```powershell
Invoke-AtomicTest T1685.005 -TestNumbers 1 -ShowDetails
Invoke-AtomicTest T1685.005 -TestNumbers 1 -InputArgs @{log_name="Security"}
```

There is no cleanup. The local Security log does not come back. Event ID 1102 is the event the Sentinel query looks for.

## Cleanup commands

Run the matching cleanup even if the test seemed to fail.

Discovery tests T1082-1, T1057-2, T1049-1, and T1087.001-8 do not leave a file behind.

Encoded command test 15: if ShowDetails created a file, delete that file. The manual command above only prints a line.

```powershell
Remove-Item "$env:TEMP\Atomic-license.txt" -Force -ErrorAction Ignore
Remove-Item "$env:TEMP\Folder_to_zip.zip" -Force -ErrorAction Ignore
```

Local users:

```bat
net user T1136.001_CMD /delete
net user T1136.001_Admin /delete
net user labguess /delete
```

Scheduled tasks. Do this before you restart the VM. The startup task launches Calculator.

```bat
schtasks /delete /tn "T1053_005_OnLogon" /f
schtasks /delete /tn "T1053_005_OnStartup" /f
```

Run key:

```bat
reg delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "Atomic Red Team" /f
```

Service. Also delete `AtomicService.exe` under `C:\AtomicRedTeam\atomics\T1543.003\bin\` if the prereq downloaded it.

```bat
sc.exe stop AtomicTestService_CMD
sc.exe delete AtomicTestService_CMD
sc.exe delete LabSvc
```

SAM hives. These files are credential material. Delete them before you shut down.

```bat
del %temp%\sam
del %temp%\system
del %temp%\security
dir %temp%\sam
```

The last `dir` should say the file is not found.

LSASS dump:

```powershell
Remove-Item "$env:TEMP\lsass-comsvcs.dmp" -Force -ErrorAction Ignore
```

RDP test. Then list stored credentials and confirm the `TERMSRV` entry is gone.

```powershell
cmdkey /delete:TERMSRV/127.0.0.1
cmdkey /list
```

Defender, if test 19 or the manual command changed settings:

```powershell
Set-MpPreference -DisableRealtimeMonitoring 0
Set-MpPreference -DisableBehaviorMonitoring 0
Set-MpPreference -DisableScriptScanning 0
Set-MpPreference -DisableBlockAtFirstSeen 0
```

Confirm **Real-time protection** is On in Windows Security.

## After the last sitting

You can remove the Atomic Red Team folder when you no longer need it:

```powershell
Remove-Item -Recurse -Force C:\AtomicRedTeam -ErrorAction Ignore
```

Restore the snapshot if the VM is unstable. Then delete extra snapshots so storage cost does not linger.

Go back to the lab guide and fill only the index rows you earned.
