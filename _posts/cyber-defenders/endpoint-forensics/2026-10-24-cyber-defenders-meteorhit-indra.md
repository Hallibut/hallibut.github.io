---
title: "Cyber Defenders - MeteorHit - Indra Writeup"
date: 2026-10-24 23:55:00 +0700
categories: [Cyber Defenders, Endpoint Forensics]
tags: [cyber-defenders, endpoint-forensics, writeup]
---

**Category**: Endpoint Forensics

**Checkout the lab here**: [https://cyberdefenders.org/blueteam-ctf-challenges/meteorhit-indra/](https://cyberdefenders.org/blueteam-ctf-challenges/meteorhit-indra/)

![image.png](/assets/img/cyber-defenders/meteorhit-indra/image.png)

> **Description**
> 
> A critical network infrastructure has encountered significant operational disruptions, leading to system outages and compromised machines. Public message boards displayed politically charged messages, and several systems were wiped, causing widespread service failures. Initial investigations reveal that attackers compromised the Active Directory (AD) system and deployed wiper malware across multiple machines.  
> 
> Fortunately, during the attack, an alert employee noticed suspicious activity and immediately powered down several key systems, preventing the malware from completing its wipe across the entire network. However, the damage has already been done, and your team has been tasked with investigating the extent of the compromise.  
> 
> You have been provided with forensic artifacts collected via KAPE SANS Triage from one of the affected machines to determine how the attackers gained access, the scope of the malware's deployment, and what critical systems or data were impacted before the shutdown.
{: .prompt-info }

A classic endpoint triage scenario dealing with Active Directory compromise and wiper malware deployment. Let's dig in.

> **Q1: The attack began with using a Group Policy Object (GPO) to execute a malicious batch file. What is the name of the malicious GPO responsible for initiating the attack by running a script?**

In Windows Active Directory environments, Group Policy Objects (GPOs) can configure scripts to run automatically during system startup or user logon. These Startup/Shutdown scripts are tracked within the system registry under `HKLM`.

![image 1.png](/assets/img/cyber-defenders/meteorhit-indra/image%201.png)

I inspected the local registry hive using Registry Explorer at the key:

```text
Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Startup\0\0
```

Inside this key, the `Script` value pointed directly to a network share script: `\\WIN-499DAFSKAR7\Data\scripts\setup.bat`. The timestamp recorded at **2024-09-24 16:04:11 UTC** confirmed that a batch script was staged to execute automatically upon system startup via Group Policy.

![image 2.png](/assets/img/cyber-defenders/meteorhit-indra/image%202.png)

To identify the specific GPO responsible, I checked the corresponding GPO registry entry and located the `DisplayName` property, which held the value **DeploySetup**. This confirmed the display name of the malicious Group Policy Object.

**Answer: DeploySetup**

> **Q2: During the investigation, a specific file containing critical components necessary for the later stages of the attack was found on the system. This file, expanded using a built-in tool, played a crucial role in staging the malware. What is the name of the file, and where was it located on the system? Please provide the full file path.**

When a startup script configured via GPO is triggered, the Windows Group Policy Script Engine (**`gpscript.exe`**) is responsible for invoking it. In this incident, `gpscript.exe` launched `cmd.exe` to interpret and run `setup.bat`.

![image 3.png](/assets/img/cyber-defenders/meteorhit-indra/image%203.png)

Filtering Sysmon Event ID 1 (Process Creation) for child processes of `gpscript.exe` revealed that `cmd.exe` was spawned with Process ID (PID) **4600**.

![image 4.png](/assets/img/cyber-defenders/meteorhit-indra/image%204.png)

To trace every action executed by `setup.bat`, I filtered Sysmon logs for all processes where the Parent Process ID (PPID) was **4600**.

![image 5.png](/assets/img/cyber-defenders/meteorhit-indra/image%205.png)

Sorting these process creation events chronologically uncovered the staging sequence:

![image 6.png](/assets/img/cyber-defenders/meteorhit-indra/image%206.png)

- **16:04:16:** The attacker forcefully (`/F`) deleted the default Windows Scheduled Task named `AnalyzeAll` under the `Power Efficiency Diagnostics` branch.
- **16:04:16:** Executed `cmd.exe /c hostname` to confirm the local machine's identity on the network.
- **16:04:17:** Executed the native Windows `expand` utility to decompress `env.cab` into the target directory `C:\ProgramData\Microsoft\env`.

**Answer: C:\ProgramData\Microsoft\env\env.cab**

> **Q3: The attacker employed password-protected archives to conceal malicious files, making it important to uncover the password used for extraction. Identifying this password is key to accessing the contents and analyzing the attack further. What is the password used to extract the malicious files?**

Continuing along the command-line timeline of PPID 4600:

- **16:04:18:** The batch script invoked `Rar.exe` from the staging directory to unpack an encrypted archive named `programs.rar` using the command-line switch `-phackemall`.

By embedding the password directly into the automated script, the attacker bypassed static antivirus detection on the archive while staging their secondary payloads.

**Answer: hackemall**

> **Q4: Several commands were executed to add exclusions to Windows Defender, preventing it from scanning specific files. This behavior is commonly used by attackers to ensure that malicious files are not detected by the system's built-in antivirus. Tracking these exclusion commands is crucial for identifying which files have been protected from antivirus scans. What is the name of the first file added to the Windows Defender exclusion list?**

Following archive extraction, the script took immediate steps to isolate the machine and blind the local endpoint security controls:

- **16:04:18:** Ran `ipconfig /release` to sever DHCP networking.
- **16:04:18:** Executed a PowerShell command (`Get-NetAdapter | ? { $_.NetEnabled } | Disable-NetAdapter`) to disable all active network interfaces.
- **16:04:23:** Queried the registry with `reg query` to check for the presence of third-party antivirus software (specifically Kaspersky).
- **16:04:30 onward:** Ran a succession of PowerShell `Add-MpPreference -ExclusionPath` commands to whitelist tools and directories from Windows Defender scanning.

The very first file specified in the exclusion list commands was `update.bat`:

```powershell
powershell -Command "Add-MpPreference -Force -ExclusionPath 'C:\ProgramData\Microsoft\env\update.bat'"
```

**Answer: update.bat**

> **Q5: A scheduled task has been configured to execute a file after a set delay. Understanding this delay is important for investigating the timing of potential malicious activity. How many seconds after the task creation time is it scheduled to run?**
> 
> **Note: Consider the system's time zone when answering questions related to time.**

Examining the subsequent commands executed by the batch script:

![image 7.png](/assets/img/cyber-defenders/meteorhit-indra/image%207.png)

- **16:04:42:** Extracted `bcd.rar` using `Rar.exe` with password `phackemall`.
- **16:04:42:** Ran `cmd.exe /c bcdedit /v | findstr identifier` to query the Boot Configuration Data GUIDs.
- **16:04:43:** Extracted `ms.rar` using `Rar.exe` with password `phackemall`.
- **16:04:43:** Modified lock screen registry values under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP` (`LockScreenImagePath` and `LockScreenImageUrl`) to point to a graphic stored in `C:\temp`.
- **16:04:43:** Invoked PowerShell to calculate a scheduled execution time 3.5 minutes into the future: `powershell -command "(Get-Date).AddMinutes(3.5).ToString('HH:mm:ss')"`.
- **16:04:43:** Called `schtasks /CREATE /SC ONCE` to register a task named `mstask`, set to execute `C:\ProgramData\Microsoft\env\env.exe C:\temp\msconf.conf` with highest privileges (`/RL HIGHEST`) under `NT AUTHORITY\SYSTEM`.
- **16:04:43:** Executed `ping localhost -n 20` as an artificial delay.

A delay of 3.5 minutes equates to $3.5 \times 60 = 210$ seconds.

**Answer: 210**

> **Q6: After the malware execution, the wmic utility was used to unjoin the computer system from a domain or workgroup. Tracking this operation is essential for identifying system reconfigurations or unauthorized changes. What is the Process ID (PID) of the utility responsible for performing this action?**

The staging script finished by scheduling the primary payload, `env.exe`. Searching for executions of `env.exe` across the Sysmon logs revealed its execution:

![image 8.png](/assets/img/cyber-defenders/meteorhit-indra/image%208.png)

`svchost.exe` (handling the Task Scheduler service) launched `env.exe` with the configuration file `C:\temp\msconf.conf`. Once initialized, `env.exe` spawned multiple `cmd.exe` instances to execute disruptive system commands, including a command calling `wmic` to unjoin the victim machine from the Active Directory domain.

![image 9.png](/assets/img/cyber-defenders/meteorhit-indra/image%209.png)

The parent `cmd.exe` process that issued this command had PID **7200**.

![image 10.png](/assets/img/cyber-defenders/meteorhit-indra/image%2010.png)

I filtered Sysmon Event ID 1 logs for child processes spawned by parent PID **7200**:

![image 11.png](/assets/img/cyber-defenders/meteorhit-indra/image%2011.png)

This revealed the exact command invoked:

```text
wmic computersystem where name="DESKTOP-VBIOB4B" call unjoindomainorworkgroup
```

![image 12.png](/assets/img/cyber-defenders/meteorhit-indra/image%2012.png)

Inspecting the process details for `WMIC.exe` showed its Process ID was **7492**.

**Answer: 7492**

> **Q7: The malware executed a command to delete the Windows Boot Manager, a critical component responsible for loading the operating system during startup. This action can render the system unbootable, leading to serious operational disruptions and making recovery more difficult. What command did the malware use to delete the Windows Boot Manager?**

Boot configuration on Windows is managed by `bcdedit.exe`. The wiper utilized `bcdedit.exe` to delete boot entries, rendering the operating system unable to restart.

![image 13.png](/assets/img/cyber-defenders/meteorhit-indra/image%2013.png)

Reviewing the child commands spawned by `env.exe` showed several `bcdedit.exe /delete` commands targeting various boot identifiers.

![image 14.png](/assets/img/cyber-defenders/meteorhit-indra/image%2014.png)

According to Microsoft documentation, the well-known identifier for the Windows Boot Manager object is `{9dea862c-5cdd-4e70-acc1-f32b344d4795}`. Tracing the log entries for this specific GUID revealed the exact deletion command:

```text
C:\Windows\Sysnative\bcdedit.exe /delete {9dea862c-5cdd-4e70-acc1-f32b344d4795} /f
```

**Answer: C:\Windows\Sysnative\bcdedit.exe /delete {9dea862c-5cdd-4e70-acc1-f32b344d4795} /f**

> **Q8: The malware created a scheduled task to ensure persistence and maintain control over the compromised system. This task is configured to run with elevated privileges every time the system starts, ensuring the malware continues to execute. What is the name of the scheduled task created by the malware to maintain persistence?**

To ensure that the wiper and lock components would re-trigger even if the system survived a reboot, `env.exe` registered a persistence task.

![image 15.png](/assets/img/cyber-defenders/meteorhit-indra/image%2015.png)

Filtering Sysmon Event ID 1 for executions of `schtasks.exe` spawned by `env.exe` revealed the following creation command:

```text
C:\Windows\System32\cmd.exe /c schtasks /CREATE /SC ONSTART /TN "Aa153!EGzN" /RL HIGHEST /RU SYSTEM /TR "\"C:\ProgramData\Microsoft\env\env.exe\" C:\temp\msconf.conf"
```

The task was configured with `/SC ONSTART` (to launch on every system boot), running under `NT AUTHORITY\SYSTEM` with highest privileges (`/RL HIGHEST`), and named **`Aa153!EGzN`**.

**Answer: Aa153!EGzN**

> **Q9: A malicious program was used to lock the screen, preventing users from accessing the system. Investigating this malware is important to identify its behavior and mitigate its impact. What is the name of this malware? (not the filename)**

In parallel with deleting system configuration and boot data, the threat actors deployed a screen locker component to prevent administrators and users from logging into the console to interrupt the wiper.

![image 16.png](/assets/img/cyber-defenders/meteorhit-indra/image%2016.png)

In the process creation events under `env.exe`, the malware executed the following command:

```text
"C:\temp\mssetup.exe" /LOCK
```

![image 17.png](/assets/img/cyber-defenders/meteorhit-indra/image%2017.png)

I examined the Sysmon Event ID 1 record for `mssetup.exe` to retrieve its cryptographic hashes:

- **MD5:** `9A49102F53291A644BD14C8202D8FBE3`
- **SHA256:** `074BCC51B77D8E35B96ED444DC479B2878BF61BF7B07E4D7BD4CF136CC3C0DCE`

![image 18.png](/assets/img/cyber-defenders/meteorhit-indra/image%2018.png)

Querying this SHA256 hash on VirusTotal revealed that security vendors widely categorize this binary as **BreakWin** (e.g., `Trojan.BreakWin`, `Trojan:Win32/BreakWin`), the specialized screen locker component deployed in the Indra / MeteorExpress attack campaign.

**Answer: BreakWin**

> **Q10: The disk shows a pattern where malware overwrites data (potentially with zero-bytes) and then deletes it, a behavior commonly linked to Wiper malware activity. The USN (Update Sequence Number) is vital for tracking filesystem changes on an NTFS volume, enabling investigators to trace when files are created, modified, or deleted, even if they are no longer present. This is critical for building a timeline of file activity and detecting potential tampering. What is the USN associated with the deletion of the file msuser.reg?**

Wiper malware typically overwrites files before unlinking them to hinder file carving and recovery. Although the files themselves are removed, the NTFS Change Journal (`$UsnJrnl:$J`) maintains a record of filesystem transactions, recording each change alongside a monotonically increasing Update Sequence Number (USN).

![image 19.png](/assets/img/cyber-defenders/meteorhit-indra/image%2019.png)

Using Eric Zimmerman's **MFTECmd** to parse `$UsnJrnl:$J` and opening the resulting CSV in **Timeline Explorer**, I filtered by the filename `msuser.reg`.

At timestamp **2024-09-24 16:08:41 UTC**, the final journal record corresponding to the file deletion was logged with Update Sequence Number **11721008**.

**Answer: 11721008**

> **Conclusion**
> 
> Through forensic analysis of the KAPE triage artifacts collected from `DESKTOP-VBIOB4B`, I reconstructed an intrusion orchestrated by the threat actor group known as **Indra**, utilizing the **MeteorExpress / MeteorHit** wiper toolkit. The intrusion commenced on **2024-09-24 at 16:04:11 UTC** when a compromised Active Directory domain controller pushed a malicious Group Policy Object named **DeploySetup**, executing `setup.bat` from a shared network folder (`\\WIN-499DAFSKAR7\Data\scripts\setup.bat`) as a Startup script.
> 
> Upon execution via `gpscript.exe`, the batch script de-provisioned network connectivity (`ipconfig /release` and disabling all adapters), checked for antivirus solutions, whitelisted malicious components in Windows Defender, and unpacked encrypted RAR archives (`programs.rar`, `bcd.rar`, `ms.rar`) using hardcoded passwords (`hackemall`, `phackemall`). It then scheduled the core wiper binary `env.exe` to run 210 seconds later via Task Scheduler under `SYSTEM`.
> 
> Once triggered, `env.exe` severed the host from the domain via WMIC, erased the Windows Boot Manager using `bcdedit.exe`, created a persistent boot task (`Aa153!EGzN`), launched the **BreakWin** screen locker (`mssetup.exe /LOCK`), and initiated systematic file wiping and zeroing across disk volumes—a destructive sequence that was ultimately halted midway when an alert employee performed an emergency manual shutdown.

### Summary

| Item | Details |
| --- | --- |
| Incident Type | Active Directory GPO Abuse, Destructive Wiper Deployment (MeteorHit / MeteorExpress), Screen Locker (BreakWin), Bootloader Destruction |
| Severity | **Critical**: Endpoint bootloader wiped, Active Directory GPO weaponized, domain unjoined, local files overwritten and deleted |
| Timeline | 2024-09-24 **16:04:11 UTC** to **16:08:41 UTC** |
| Attack Source | Domain Controller / File Share `WIN-499DAFSKAR7` hosting malicious script `\\WIN-499DAFSKAR7\Data\scripts\setup.bat` |
| Affected Systems | `DESKTOP-VBIOB4B` (Domain: `abc.local`) and other domain-joined network workstations |
| Compromised Components | Group Policy Object `DeploySetup`, Windows Boot Configuration Data (BCD), local NTFS filesystem, Domain membership |
| Impact Mitigation | Quick action by an alert employee who powered down machines, preventing the wiper from completely overwriting all storage volumes |

### Timeline

All times are recorded in UTC on 2024-09-24, extracted directly from Windows Registry, Sysmon Event ID 1, and the NTFS `$UsnJrnl`.

| Time (UTC) | Host | Event Description | Artifact / Source |
| --- | --- | --- | --- |
| 16:04:11 | DESKTOP-VBIOB4B | GPO `DeploySetup` triggers Startup script `\\WIN-499DAFSKAR7\Data\scripts\setup.bat` | Registry (`Group Policy\Scripts\Startup`) |
| 16:04:16 | DESKTOP-VBIOB4B | `gpscript.exe` spawns `cmd.exe` (PID 4600); deletes scheduled task `AnalyzeAll`; queries `hostname` | Sysmon Event ID 1 |
| 16:04:17 | DESKTOP-VBIOB4B | `expand` decompressing `env.cab` into `C:\ProgramData\Microsoft\env` | Sysmon Event ID 1 |
| 16:04:18 | DESKTOP-VBIOB4B | `Rar.exe` extracts `programs.rar` using password `hackemall` | Sysmon Event ID 1 |
| 16:04:18 | DESKTOP-VBIOB4B | Executes `ipconfig /release` and PowerShell adapter disable commands to sever network access | Sysmon Event ID 1 |
| 16:04:23 | DESKTOP-VBIOB4B | Registry queried to enumerate presence of Kaspersky antivirus | Sysmon Event ID 1 |
| 16:04:30 | DESKTOP-VBIOB4B | PowerShell `Add-MpPreference` executed to exclude `update.bat`, `Rar.exe`, and staging paths from Defender | Sysmon Event ID 1 |
| 16:04:42 | DESKTOP-VBIOB4B | `Rar.exe` extracts `bcd.rar` and `ms.rar` with password `phackemall`; enumerates BCD GUIDs | Sysmon Event ID 1 |
| 16:04:43 | DESKTOP-VBIOB4B | Lock screen registry modified; task `mstask` scheduled to run `env.exe` after a 210-second delay | Sysmon Event ID 1 |
| 16:07:43 | DESKTOP-VBIOB4B | Task Scheduler launches `env.exe C:\temp\msconf.conf` under `NT AUTHORITY\SYSTEM` | Sysmon Event ID 1 |
| 16:07:44 | DESKTOP-VBIOB4B | `env.exe` spawns `WMIC.exe` (PID 7492) to execute `unjoindomainorworkgroup` | Sysmon Event ID 1 |
| 16:07:45 | DESKTOP-VBIOB4B | `bcdedit.exe /delete {9dea862c-5cdd-4e70-acc1-f32b344d4795} /f` wipes the Windows Boot Manager | Sysmon Event ID 1 |
| 16:07:46 | DESKTOP-VBIOB4B | Persistence task `Aa153!EGzN` registered to execute on startup (`/SC ONSTART`) | Sysmon Event ID 1 |
| 16:07:47 | DESKTOP-VBIOB4B | Screen locker component `"C:\temp\mssetup.exe" /LOCK` (**BreakWin**) executed | Sysmon Event ID 1 |
| 16:08:41 | DESKTOP-VBIOB4B | Wiper routine overwrites and deletes files, recorded with USN `11721008` for `msuser.reg` | NTFS `$UsnJrnl` |

### Indicators of Compromise

| Type | Value | Description / Context |
| --- | --- | --- |
| GPO Name | `DeploySetup` | Weaponized Group Policy Object initiating Startup script |
| Network Path | `\\WIN-499DAFSKAR7\Data\scripts\setup.bat` | Staging script hosted on domain controller share |
| File Path | `C:\ProgramData\Microsoft\env\env.cab` | Compressed cabinet file staging wiper components |
| File Path | `C:\ProgramData\Microsoft\env\env.exe` | Core Meteor wiper executable |
| File Path | `C:\temp\mssetup.exe` | BreakWin screen locker utility (`/LOCK`) |
| File Path | `C:\temp\msconf.conf` | Configuration file ingested by `env.exe` |
| SHA256 | `074BCC51B77D8E35B96ED444DC479B2878BF61BF7B07E4D7BD4CF136CC3C0DCE` | SHA256 of `mssetup.exe` (Trojan.BreakWin) |
| MD5 | `9A49102F53291A644BD14C8202D8FBE3` | MD5 of `mssetup.exe` |
| Scheduled Task | `mstask` | One-time task scheduled 210s post-staging to launch `env.exe` |
| Scheduled Task | `Aa153!EGzN` | Startup persistence task (`/SC ONSTART`) running under `SYSTEM` |
| Archive Password | `hackemall` | Password for `programs.rar` |
| Archive Password | `phackemall` | Password for `bcd.rar` and `ms.rar` |
| BCD GUID | `{9dea862c-5cdd-4e70-acc1-f32b344d4795}` | Windows Boot Manager identifier targeted for deletion |

### MITRE ATT&CK Mapping

| Tactic | Technique | Evidence |
| --- | --- | --- |
| Initial Access | Group Policy Modification (T1484.001) | Attackers weaponized domain GPO `DeploySetup` to push `setup.bat` to domain endpoints. |
| Execution | Command and Scripting Interpreter: Windows Command Shell (T1059.003) | Startup script executed via `gpscript.exe` calling `cmd.exe` (PID 4600). |
| Execution | Scheduled Task/Job: Scheduled Task (T1053.005) | Scheduled tasks `mstask` and `Aa153!EGzN` utilized for delayed execution and persistence. |
| Defense Evasion | Impair Defenses: Disable or Modify Tools (T1562.001) | Invoked PowerShell `Add-MpPreference` to exclude malware paths from Windows Defender. |
| Defense Evasion | Masquerading (T1036) | Malware components staged under legitimate paths like `C:\ProgramData\Microsoft\env`. |
| Defense Evasion | File Deletion (T1070.004) | Deleted scheduled tasks (`AnalyzeAll`) and systematically wiped user files. |
| Discovery | System Information Discovery (T1082) | Executed `hostname` to verify host identity. |
| Discovery | Security Software Discovery (T1518.001) | Queried registry to detect presence of antivirus solutions (e.g. Kaspersky). |
| Impact | Inhibit System Recovery (T1490) | Executed `bcdedit.exe /delete` to destroy Windows Boot Manager and boot configuration data. |
| Impact | Data Destruction (T1485) | Overwrote and deleted files across NTFS partitions, tracked via `$UsnJrnl`. |
| Impact | Defacement (T1491) | Reconfigured lock screen registry settings (`PersonalizationCSP`) to display politically charged images. |

### Assessment and Recommendations

Immediate Mitigation:

- Isolate all machines in the Active Directory domain immediately by severing physical and logical switch ports to halt lateral propagation of the GPO.
- Power down endpoints where wiper activity is detected to prevent in-progress disk overwriting.
- On Domain Controllers, immediately disable or unlink the malicious GPO `DeploySetup` and revoke share access to `\\WIN-499DAFSKAR7\Data\scripts\setup.bat`.

Remediation:

- Endpoints with deleted Boot Configuration Data (`bcdedit /delete {9dea862c-5cdd-4e70-acc1-f32b344d4795}`) must be booted via Windows PE / Recovery Environment to rebuild the BCD using `bootrec /rebuildbcd` and `bcdboot`.
- Remove persistent malicious scheduled tasks: `schtasks /delete /tn "Aa153!EGzN" /f` and `schtasks /delete /tn "mstask" /f`.
- Purge malware staging directories: delete `C:\ProgramData\Microsoft\env\` and `C:\temp\`.
- Remove Windows Defender exclusions added via PowerShell by reviewing `Get-MpPreference` and executing `Remove-MpPreference -ExclusionPath ...`.
- Re-enable network adapters and restore standard DHCP configurations.

Prevention:

- Restrict Active Directory Group Policy administrative access: implement strict Tiering (Tier 0 / Tier 1 / Tier 2) and require dual-custody or change approval for GPO modifications.
- Implement Centralized Auditing for GPO changes (Event IDs 5136, 5137, 5141) and alert on new startup scripts referencing network shares.
- Enforce AppLocker or Windows Defender Application Control (WDAC) in script-enforcement mode (Constrained Language Mode) to block unsigned batch/PowerShell scripts and unauthorized binaries executing from `C:\ProgramData` and `C:\temp`.
- Deploy resilient, immutable offline backups of endpoints and Domain Controllers to ensure rapid recovery from destructive wiper incidents.
