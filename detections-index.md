# Detection index

These queries are starters. Every file is marked `untested`. The last two columns are blank on purpose. Fill **Tested** and **Fired** only after you run that query against your own lab data.

Use `yes` or `no`. Leave the cells blank when you have not run the test. Do not copy a result from this table into a report unless you produced it.

| Query | Technique | Data source | Tested (yes/no) | Fired (yes/no) |
| --- | --- | --- | --- | --- |
| [detections/collection/archive-staged-in-temp.kql](detections/collection/archive-staged-in-temp.kql) | T1074.001 | DeviceFileEvents | | |
| [detections/command-and-control/powershell-webclient-download.kql](detections/command-and-control/powershell-webclient-download.kql) | T1105 | DeviceProcessEvents | | |
| [detections/credential-access/entra-password-spray.kql](detections/credential-access/entra-password-spray.kql) | T1110.003 | SigninLogs | | |
| [detections/credential-access/lsass-memory-dump.kql](detections/credential-access/lsass-memory-dump.kql) | T1003.001 | DeviceProcessEvents | | |
| [detections/credential-access/sam-hive-save.kql](detections/credential-access/sam-hive-save.kql) | T1003.002 | DeviceProcessEvents | | |
| [detections/credential-access/windows-failed-logon-brute-force.kql](detections/credential-access/windows-failed-logon-brute-force.kql) | T1110.001 | SecurityEvent | | |
| [detections/defense-impairment/defender-realtime-protection-disabled.kql](detections/defense-impairment/defender-realtime-protection-disabled.kql) | T1685 | DeviceProcessEvents | | |
| [detections/defense-impairment/security-audit-log-cleared.kql](detections/defense-impairment/security-audit-log-cleared.kql) | T1685.005 | SecurityEvent | | |
| [detections/defense-impairment/wevtutil-clear-event-log.kql](detections/defense-impairment/wevtutil-clear-event-log.kql) | T1685.005 | DeviceProcessEvents | | |
| [detections/discovery/local-account-discovery.kql](detections/discovery/local-account-discovery.kql) | T1087.001 | DeviceProcessEvents | | |
| [detections/discovery/network-connection-discovery.kql](detections/discovery/network-connection-discovery.kql) | T1049 | DeviceProcessEvents | | |
| [detections/discovery/process-discovery.kql](detections/discovery/process-discovery.kql) | T1057 | DeviceProcessEvents | | |
| [detections/discovery/system-information-discovery.kql](detections/discovery/system-information-discovery.kql) | T1082 | DeviceProcessEvents | | |
| [detections/execution/encoded-powershell.kql](detections/execution/encoded-powershell.kql) | T1059.001 | DeviceProcessEvents | | |
| [detections/lateral-movement/rdp-logon.kql](detections/lateral-movement/rdp-logon.kql) | T1021.001 | SecurityEvent | | |
| [detections/persistence/local-administrators-member-added.kql](detections/persistence/local-administrators-member-added.kql) | T1098.007 | SecurityEvent | | |
| [detections/persistence/new-local-user.kql](detections/persistence/new-local-user.kql) | T1136.001 | SecurityEvent | | |
| [detections/persistence/registry-run-key.kql](detections/persistence/registry-run-key.kql) | T1547.001 | DeviceProcessEvents | | |
| [detections/persistence/scheduled-task-created.kql](detections/persistence/scheduled-task-created.kql) | T1053.005 | DeviceProcessEvents | | |
| [detections/persistence/windows-service-created.kql](detections/persistence/windows-service-created.kql) | T1543.003 | DeviceProcessEvents | | |
