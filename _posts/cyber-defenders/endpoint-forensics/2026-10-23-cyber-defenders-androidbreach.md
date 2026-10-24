---
title: "Cyber Defenders - AndroidBreach Writeup"
date: 2026-10-23 17:00:00 +0700
categories: [Cyber Defenders, Endpoint Forensics]
tags: [cyber-defenders, endpoint-forensics, writeup]
---

**Category**: Endpoint Forensics

**Checkout the lab here**: [https://cyberdefenders.org/blueteam-ctf-challenges/androidbreach/](https://cyberdefenders.org/blueteam-ctf-challenges/androidbreach/)

![image.png](/assets/img/cyber-defenders/androidbreach/image.png)

> **Description**
> 
> At BrightWave Company, a data breach occurred due to an employee's lack of security awareness, compromising his credentials. The attacker used these credentials to gain unauthorized access to the system and exfiltrate sensitive data. During the investigation, the employee revealed two critical points: first, he stores all his credentials in the notes app on his phone, and second, he frequently downloads APK files from untrusted sources. Your task is to analyze the provided Android dump, identify the malware downloaded, and determine its exact functionality.
{: .prompt-info }

This was my first time tackling an Android forensics lab, so let's see what artifacts we were provided with.

I was given a virtual directory containing an extracted `/data` partition dump from a virtualized Android device running on Genymotion.

| Directory | Function | Digital Forensics Significance |
| --- | --- | --- |
| `data/data` or `user/0` | Per-application private app data | Contains SQLite databases (`*.db`), preference files (`shared_prefs`), chat history, cookies, login tokens, and accounts. |
| `app` | Installed APK files | Contains third-party application packages requiring decompilation or malware analysis. |
| `media` | Shared storage (`/sdcard`) | Contains user photos, videos, downloaded documents, `DCIM`, `Download`, and `WhatsApp Media` folders. |
| `system` | Android OS system data | Contains lock screen configurations (`locksettings.db`, `gesture.key`), account lists (`accounts.db`), and package metadata (`packages.xml`). |
| `misc` | Network & system service configurations | Stores saved Wi-Fi networks (`wifi/WifiConfigStore.xml`), VPN profiles, and Bluetooth pairings. |
| `property` | System properties | Contains Android build properties, device model, and OS version info. |
| `anr` & `tombstones` | Application crash & ANR reports | Records crash dumps and traces of running processes prior to an application crash. |

> **Q1: What suspicious link was used to download the malicious APK from your initial investigation?**

To identify the suspicious link used to download the malicious APK, I checked the mobile device's web browsing history. In Android Chrome, browsing history is stored in an SQLite database located at:

```text
C:\Users\Administrator\Desktop\Start Here\Artifacts\data\user\0\com.android.chrome\app_chrome\Default\History
```

Opening this database in an SQLite viewer revealed the user's browsing activity.

![image 1.png](/assets/img/cyber-defenders/androidbreach/image%201.png)

At **2024-08-16 01:58:10 UTC**, the user accessed a file-sharing link purporting to offer a "Discord Nitro" mod package (`https://ufile.io/57rdyncx`).

**Answer: https://ufile.io/57rdyncx**

> **Q2: What is the name of the downloaded APK?**

Knowing the user initiated a download, I inspected the shared download directory where downloaded network resources are stored:

```text
C:\Users\Administrator\Desktop\Start Here\Artifacts\data\media\0\Download
```

![image 2.png](/assets/img/cyber-defenders/androidbreach/image%202.png)

The downloaded file in the folder was named **Discord_nitro_Mod.apk**.

**Answer: Discord_nitro_Mod.apk**

> **Q3: What is the malicious package name found in the APK?**

An APK file is fundamentally a ZIP archive containing DEX bytecode, resources, and manifest metadata. To analyze the contents of the APK, I used **JADX-GUI**, an open-source Android decompiler.

![image 3.png](/assets/img/cyber-defenders/androidbreach/image%203.png)

Under the **Resources** tree, I inspected `AndroidManifest.xml`. This file describes the package name, requested permissions, services, broadcast receivers, and application components.

![image 4.png](/assets/img/cyber-defenders/androidbreach/image%204.png)

Inspecting `AndroidManifest.xml` confirmed that this was a **trojanized legitimate Discord application**. The attacker took the official Discord APK (`version 216.14 - Stable`) and injected an additional spyware/keylogger module into it.

The injected service was registered under `com.example.keylogger.MyService` and required `android.permission.BIND_ACCESSIBILITY_SERVICE`. Accessibility permissions are among the most dangerous permissions on Android: they allow an application to inspect the full view hierarchy, read screen content (including passwords and OTPs), and log keystrokes across all applications.

**Answer: com.example.keylogger**

> **Q4: Which port was used to exfiltrate the data?**

Based on `AndroidManifest.xml`, the malicious component resides in the `com.example.keylogger` package. Expanding **Source code** → **com** → **example.keylogger** revealed the decompiled Java source code of the payload.

![image 5.png](/assets/img/cyber-defenders/androidbreach/image%205.png)

Examining the code, specifically the `openEmailClient` function, revealed that it established a connection over port **465** (SMTPS) to exfiltrate the stolen data.

![image 6.png](/assets/img/cyber-defenders/androidbreach/image%206.png)

**Answer: 465**

> **Q5: What is the service platform name the attacker utilized to receive the data being exfiltrated?**

Right above the port configuration in the email dispatch routine, the attacker specified the SMTP host address: `sandbox.smtp.mailtrap.io`.

![image 7.png](/assets/img/cyber-defenders/androidbreach/image%207.png)

The service platform utilized by the attacker is **mailtrap.io**.

**Answer: mailtrap.io**

> **Q6: What email was used by the attacker when exfiltrating data?**

Searching through the source code for hardcoded email credentials revealed the recipient address used to receive the exfiltrated logs.

![image 8.png](/assets/img/cyber-defenders/androidbreach/image%208.png)

The destination email address is `APThreat@gmail.com`.

**Answer: APThreat@gmail.com**

> **Q7: The attacker has saved a file containing leaked company credentials before attempting to exfiltrate it. Based on the data, can you retrieve the credentials found in the leak?**

The attacker logged keystrokes into a local text file named **`config.txt`** before attempting exfiltration.

![image 9.png](/assets/img/cyber-defenders/androidbreach/image%209.png)

In Android, calling `openFileOutput("config.txt", 0)` (where `0` corresponds to `Context.MODE_PRIVATE`) writes directly to the private application storage directory under `files/`. Because the malicious payload was injected under the guise of the Discord app package, the full filesystem path is `/data/data/com.discord/files/config.txt`.

Navigating to that path within the provided artifacts dump and inspecting `config.txt` revealed the leaked credentials:

![image 10.png](/assets/img/cyber-defenders/androidbreach/image%2010.png)

**Answer: hany.tarek@brightwave.com:HTarek@9711$QTPO309**

> **Q8: The malware altered images stored on the Android phone by encrypting them. What is the encryption key used by the malware to encrypt these images?**

Searching the decompiled source code for the keyword `encrypt` led to an encryption utility class (`AESUtils`).

![image 11.png](/assets/img/cyber-defenders/androidbreach/image%2011.png)

Inside this class, the key generation method **`stringToKey`** is the primary clue. It takes a Base64-encoded string (`keyString`), decodes it via `Base64.getDecoder().decode(keyString)` into raw bytes, and wraps the resulting byte array in a `SecretKeySpec` object configured for AES encryption.

To find the actual key, I searched for calls to `AESUtils.stringToKey(...)`.

![image 12.png](/assets/img/cyber-defenders/androidbreach/image%2012.png)

The call passes the Base64-encoded string `OWJZJFdRNyFjVHo0NjVUWA==`. Decoding this Base64 string yielded the plaintext encryption key:

```bash
echo -n "OWJZJFdRNyFjVHo0NjVUWA==" | base64 -d
# Output: 9bY$wQ7!cTz465TX
```

**Answer: 9bY$wQ7!cTz465TX**

> **Q9: The employee stored sensitive data in their phone's gallery, including credit card information. What is the CVC of the credit card stored?**

The malware encrypted images stored within the user's gallery. Checking the shared media directory:

```text
C:\Users\Administrator\Desktop\Start Here\Artifacts\data\media\0\Pictures
```

![image 13.png](/assets/img/cyber-defenders/androidbreach/image%2013.png)

Inspecting the recovered image of the credit card stored in the Pictures directory reveals the card details, showing a CVC code of **128**.

**Answer: 128**

> **Conclusion**
> 
> Through forensic analysis of the provided Android `/data` partition dump, I reconstructed an incident involving an employee falling victim to a trojanized mobile application. At **01:58:10 UTC** on **2024-08-16**, the user browsed to `https://ufile.io/57rdyncx` and downloaded `Discord_nitro_Mod.apk`. Reverse engineering the APK using JADX revealed that an attacker had repackaged legitimate Discord release `216.14` with a rogue package named `com.example.keylogger`.
> 
> The malware abused Android's `BIND_ACCESSIBILITY_SERVICE` permission to log keystrokes and screen content, staging captured data locally into `/data/data/com.discord/files/config.txt`. Among the logged inputs were corporate credentials for `hany.tarek@brightwave.com`. The malware then utilized port 465 via `sandbox.smtp.mailtrap.io` to exfiltrate the stolen data to `APThreat@gmail.com`. In addition, the malware executed a local ransomware routine using AES encryption with the static key `9bY$wQ7!cTz465TX` to encrypt images in the device's gallery, including a photo of a corporate credit card.

### Summary

| Item | Details |
| --- | --- |
| Incident Type | Sideloaded Trojanized APK leading to keylogger installation, credential exfiltration, and local file encryption |
| Severity | **Critical**: Attacker abused Accessibility Services to capture corporate credentials and encrypted local device storage |
| Timeline | 2024-08-16 **01:58:10 UTC** |
| Attack Source | Payload downloaded from `https://ufile.io/57rdyncx`; exfiltration destination `sandbox.smtp.mailtrap.io` (port 465) forwarding to `APThreat@gmail.com` |
| Affected Systems | Employee Android mobile device |
| Compromised Accounts | Corporate network credentials (`hany.tarek@brightwave.com`) and personal financial information (credit card) |
| No Known Impact | No evidence indicating that the attacker successfully utilized the stolen credentials to access internal systems or move laterally |

### Timeline

| Time (UTC) | Host | Event | Log / Artifact Source |
| --- | --- | --- | --- |
| 2024-08-16 01:58:10 | Android | User navigated to `https://ufile.io/57rdyncx` and downloaded `Discord_nitro_Mod.apk` | Chrome Browser History Database |

### Indicators of Compromise

| Type | Value | Notes |
| --- | --- | --- |
| URL | `https://ufile.io/57rdyncx` | Download link for the malicious APK |
| C2 / Host | `sandbox.smtp.mailtrap.io` | Intermediate SMTP server used for exfiltration |
| Port | `465` | SMTPS network port used to connect to the exfiltration server |
| Email | `APThreat@gmail.com` | Attacker email address configured to receive exfiltrated logs |
| Encryption Key | `9bY$wQ7!cTz465TX` | Hardcoded static AES key used to encrypt gallery images |

### MITRE ATT&CK Mapping

| Tactic | Technique | Evidence |
| --- | --- | --- |
| Discovery | File and Directory Discovery (T1420) | Malware enumerated device directories targeting image files (`.jpg`). |
| Credential Access | Input Capture: Keylogging (T1417) | Abused `BIND_ACCESSIBILITY_SERVICE` via `com.example.keylogger.MyService` to intercept keystrokes and screen content. |
| Initial Access, Persistence | Malicious Application (T1479) | User was lured into downloading and installing a malicious APK from `https://ufile.io/57rdyncx`. |
| Execution | User Execution (T1624) | Required user interaction to sideload the APK and grant accessibility permissions. |
| Execution | Scheduled Task/Job (T1614) | Declared `BroadcastForAlarm` and utilized `AlarmManager` to maintain persistent background execution. |
| Defense Evasion | Masquerading (T1444) | Masqueraded as a legitimate Discord app using the package name `com.discord` and file name `Discord_nitro_Mod.apk`. |
| Defense Evasion | Obfuscated Files or Information (T1406) | Base64-encoded secret keys and AES encryption to obfuscate functionality and encrypt files. |
| Persistence | Boot or Logon Initialization (T1401) | Requested `RECEIVE_BOOT_COMPLETED` permission to automatically restart the keylogger service upon device boot. |

### Assessment and Recommendations

Immediate Mitigation:

- Immediately isolate the infected Android device from company Wi-Fi and VPN access to sever exfiltration channels.
- Configure corporate firewalls and DNS resolvers to block outbound connections to `sandbox.smtp.mailtrap.io` (port 465) and the hosting domain `ufile.io`.
- Revoke and reset the compromised credentials for `hany.tarek@brightwave.com` across all enterprise services and directory systems.
- Instruct the employee to immediately freeze and reissue the compromised corporate credit card.

Remediation:

- Uninstall the malicious trojanized application (`Discord_nitro_Mod.apk` / package `com.discord`) from the mobile device.
- Remove the local staging log file containing stolen credentials at `/data/data/com.discord/files/config.txt`.
- Decrypt encrypted pictures using the recovered AES key `9bY$wQ7!cTz465TX`.

Prevention:

- Enforce Mobile Device Management (MDM) policies restricting third-party application sideloading (Unknown Sources) on all devices accessing corporate assets.
- Mandate Phishing-Resistant Multi-Factor Authentication (MFA/2FA) for all corporate logins to prevent unauthorized access via stolen passwords.
- Deliver security awareness training highlighting the risks of cracked/modded applications.
- Deploy Mobile Threat Defense (MTD) solutions to detect unauthorized accessibility service usage and known malicious packages.
