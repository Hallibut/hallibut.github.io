---
title: "SOC HTB - Section 6: Windows Attacks & Defense"
date: 2026-06-08 00:00:00 +0700
categories: [HTB SOC Jobpath]
tags: [cdsa, study-notes, htb-soc-jobpath, windows, active-directory, defense]
---




## Windows Attacks & Defense

## Setting the stage

### Introduction and Terminology

#### **What is Active Directory?**

**Active Directory** (also called `AD`), release in 2000, is a directory service for windows enterprise enviroments.

Base on the protocols `x.500` and `LDAP`.

A distributed, hierarchical structure that allows
centralized management of an organization's resources, including:

- users
- computers
- groups
- network devices
- file shares, group policies, devices, and trusts.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image.png)

The most apparent practice to keep Active Directory secure is ensuring that proper **Patch Management** is in place, as patch management is currently posing challenges to organizations worldwide.

### Setup

For user Windows Machine:

```bash
xfreerdp /u:eagle\\bob /p:Slavi123 /v:TARGET_IP /dynamic-resolution
```

For Kali Machine:

```bash
xfreerdp /v:TARGET_IP /u:kali /p:kali /dynamic-resolution
```

Other Machine:

- **DC1: 172.16.18.3**
- **DC2: 172.16.18.4**
- **Server01: 172.16.18.10**
- **PKI: 172.16.18.15**
- Connect to the target as bob (as described for the first task (bob is a jump box))
- Go to ‘Start → Remote Desktop Connection’ and login with the creds from htb-student
- Type in ip address and username

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%201.png)

- Type in password

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%202.png)

Hint: the keyboard is in Danish so change it back to US

## Attacks & Defense

### Kerberoasting

#### Description

- **Service Principal Name (SPN)** is a value use by Kerberos authentication to verify whenever client application **request service authentication** for an account.
    - Format: *ServiceClass/Host:Port/ServiceName*.
        - ServiceClass (Must have) is for type of service.
        - Host (Must have) is for FQDN.
        - Port (Optional) specific irregular port.
        - ServiceName (Optionnal) specific name for that service.
- SPN used in step 3 and 4 of Kerberos operation:

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%203.png)

- **Kerberoasting** is a **post-exploitation attack** that attempts to exploit this behavior by obtaining a ticket and performing offline password cracking to open.
    - An attacker uses a low-privileged account to request an **encrypted service ticket (TGS) associated with an SPN** (contain password hash for a specific service inside AD).
    - This ticket is then subjected to offline password cracking to reveal the password without triggering account lockouts.
- A factor that has some impact is the encryption algorithm used when the ticket is created, with the likely options being:
    - `AES`, `RC4`, `DES`
    - Security best practices recommend disabling `RC4` and `DES`
    - But attacker can still trick **Key Distribution Center** to send TGS Ticket using RC4 encryption.

#### Attack path

{% include_relative windows-attack-diagrams/kerberoasting_animation.html %}

- **Rubeus** is an exploit tool that allow you to perform Kerberoasting
- **Hashcat** or **John The Ripper** are tools that you can use for offline cracking the *Kerberoastable TGS*

#### Prevention

- Use stronger password (100+ random characters) →  ensures that cracking the password is practically impossible.
- Use **Group Managed Service Accounts (GMSA)**

#### Detection

- Inspect **EventID 4769** (Whenever a Kerberos service ticket was requested). Work best on environment where all applications support AES and only AES genarated → In an AES-only environment, any Event ID 4769 logging a request for an RC4 ticket is a guaranteed red flag that an attacker is trying to downgrade the encryption to crack passwords faster.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%204.png)

- Detect noise in TGS request
    - **By User:** Which account sending TGS request rapidly?
    - **By Machine:** Detect the requests originated (IP Address)?

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%205.png)

- Use **Honey pot**

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%206.png)

#### Labs

I was provided with 2 machines, one belonging to the user Bob which appears to already be in the active directory, and the other is Kali Linux, which I will use to crack passwords offline

First, I need to perform Kerberoasting on this AD Domain

```python
C:\Users\bob\Downloads>Rubeus.exe Kerberoast /outfile:spn.txt
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%207.png)

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%208.png)

Transferring this content to Kali, I used Hashcat to crack the hash.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%209.png)

On Kali, create a txt file and paste the hash. Run the following hashcat command using the rockyou.txt wordlist, a famous dictionary specialized for cracking weak passwords. (you can find it at /usr/share/wordlists/rockyou.txt.gz in Kali)

```python
hashcat -m 13100 -a 0 spn.txt rockyou.txt --force
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2010.png)

**Answer: mariposa**

### AS-REProasting

#### Description

- The AS-REPRoast technique was introduced for attacking user accounts that don't require Kerberos preauthentication. Here is a wonderfully detal [post](https://blog.harmj0y.net/activedirectory/roasting-as-reps/) about this exploit.
- AS-REPRoast technique is aiming for step 1 and 2 in Kerberos exchange.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%203.png)

- An attacker uses a **misconfigured account (Pre-Authentication disabled)** to request an **AS-REP message (containing a session key encrypted with the user's password hash)**.

#### Attack path

{% include_relative windows-attack-diagrams/asreproasting_animation.html %}

- To obtain crackable hashes, we can use **Rubeus** again with the **asreproast** action
- **Hashcat** or **John The Ripper** are tools that you can use for offline cracking the *AS-REP hashes*.

#### Prevention

- Don’t **misconfigured**

#### Detection

- Inspect **EventID 4768** (Whenever a Kerberos Authentication ticket was generated).

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2011.png)

- **Pre-Authentication Type** is a specific data field found in Kerberos authentication logs. By default, Kerberos requires a user to prove they actually know their password *before* KDC responds with anything useful.
    - So when an AS-REQ comes in that completely skips that initial proof of identity, the system records the Pre-Authentication Type as **`0`**
    - If a defender sees a Pre-Authentication Type of **`0`** in the logs, it means the server just handed over a piece of data encrypted with a user's password without verifying who was asking for it

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2012.png)

- Use **Honey pot,** follow these mindsets when setup:
    - **Account Age:** Target older, potentially inactive accounts. Avoid new ones, as they likely have strong passwords or are honeypots (traps).
    - **Password Age:** Over 2 years old for service accounts; under 1 year old for regular users.
    - **Login History:** Must have logged in *after* the last password change to avoid looking suspicious.
    - **Value:** Must have elevated privileges to make cracking the hash worthwhile.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%206.png)

#### Labs

> **Connect to the target and perform an AS-REProasting attack. What is the password for the user anni?**
> 

The task requires me to perform AS-REP Roasting with Rubeus

```bash
C:\Users\bob\Downloads>Rubeus.exe asreproast /outfile:asroast.txt
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2013.png)

Copy, paste and crack it on Kali with Hashcat (I have to add “$23” before “anni” to tell hashcat it was RC4 encryption and crack it with the right format) 

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2014.png)

```bash
hashcat -m 18200 -a 0 asreproast.txt rockyou.txt --force
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2015.png)

**Answer: shadow**

> **After performing the AS-REProasting attack, connect to DC1 (172.16.18.3) as 'htb-student:HTB_@cademy_stdnt!' and look at the logs in Event Viewer. What is the TargetSid of the svc-iam user?**
> 

Accessing Event Viewer

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2016.png)

**Answer: S-1-5-21-1518138621-4282902758-752445584-3103**

### GPP Passwords

#### Description

- **SYSVOL (System Volume)** is a special shared folder, automatically created on all **DCs** in a Windows Server AD network.
- This folder contains two critical components for network administration:
    - **Group Policy Objects (GPO):** Contains policy configuration files, including templates, registry files (registry.pol), and security configuration files used to enforce rules on workstations and user accounts.
    - **Logon/Startup Scripts:** Contains scripts (batch, PowerShell...) that run automatically when the computer starts up, shuts down, or when a user logs in/out.
- Location and mechanism
    - Installed at the path **C:\Windows\SYSVOL**.
    - Shared by the system to the internal network via the path **\\<domain-name>\SYSVOL** so client machines can access and download policies.
    - **Replication:** To ensure all DCs apply the same set of policies, Windows Server uses the **DFS-R (Distributed File System Replication)** service to continuously synchronize changes in SYSVOL. *(Note: In older Windows Server versions from 2003 and earlier, this mechanism was handled by the FRS - File Replication Service)*.
- Key point of this attack:
    - 2008, they introduced **Group Policy Preferences (GPP),** a collection of Group Policy extensions
    - One of them include the ability to store and use credentials.
    - Microsoft encrypted the password of the Administrator account and stored it in SYSVOL, but they used **a single static decryption key** across all systems worldwide.
    - The fatal mistake was that they **publicly published** this key on the internet, allowing anyone to copy it, decrypt the password themselves, and gain full system control.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2017.png)

#### Attack path

{% include_relative windows-attack-diagrams/gpp_password_animation.html %}

- Use the [Get-GPPPassword](https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1) function from **PowerSploit**
- It will automatically parses all XML files in the Policies folder in SYSVOL, picking up those with the cpassword property and decrypting them once detected.

#### Prevention

- Microsoft have already released patch, but lot of system still haven’t have that.
- It is recommend that you patch the system.

#### Detection

- Inspect **EventID 4663 (An attempt was made to access an object),** use a Dummy File containing a fake configuration and don't link it to any actual policy. A normal computer will never touch it. If the system logs that an account is intentionally trying to open and read this file, it is almost certainly a hacker's behavior.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2018.png)

- Inspect **EventID** **4624 (successful logon), EventID 4625 (failed logon)** or  **EventID 4768 (TGT requested).** Focus on activities of a account and compare it with baseline of your enviroment.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2019.png)

- Use **Honey pot,** follow these mindsets when setup:
    - Create a account which provide semi-privileged, ideally a **Service Account**, then save the password (wrong password) of this account into an XML file in the SYSVOL directory.
    - Service accounts rarely have their passwords changed. Set it up so the last password change time for this account is older than the creation date of the XML file.
    - Setup a dummy task to occasionally log in using this account.
        
        ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2020.png)
        
    - **EventID 4771 (Kerberos pre-authentication failed)**
        
        ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2021.png)
        
    - **EventID 4776 (The domain controller attempted to validate the credentials for an account)**
        
        ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2022.png)
        

#### Labs

> **Connect to the target and run the Powersploit Get-GPPPassword function. What is the password of the svc-iis user?**
> 

To perform the attack, first i have to access Powersploit script “**Get-GPPPassword.ps1**”.

Luckily, they already put it inside Download folder, so everything that i have to do now is to access it with PowerShell and run the script.

By default, Windows sets its PowerShell **Execution Policy** to Restricted, protecting the system from malicious code. To turn is off easily, I run this command

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

And then run the script:

```bash
Import_Module .\Get-GPPPassword.ps1
Get-GPPPassword
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2023.png)

One this script get the password, it will automatically use the unwanted leak key provide by Microsoft to decrypt it

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2024.png)

**Answer: abcd@123**

> **After running the previous attack, connect to 
DC1 (172.16.18.3) as 'htb-student:HTB_@cademy_stdnt!' and look at the 
logs in Event Viewer. What is the Access Mask of the generated events?**
> 

Read **EventID 4663** and sort time column to get the latest event (the one that we just generate in the previous question).

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2025.png)

The file being read is Groups.xml and Access Mask **0x80** (**ReadAttributes)** mean some read the attribute inside.

**Answer: 0x80**

### GPO Permissions/GPO Files

#### Description

- **Group Policy Object** contained **Group Policy settings**.
- A GPO can represent policy settings in the file system and in the Active Directory.
- They are linked to an *Organizational Unit* in the AD structure for their settings to be applied to objects that reside in the OU or any child OU of the one to which the GPO is linked.
- Policy settings are divided into "policy settings that affect a computer” and “policy settings that affect an user”

#### Attack path

{% include_relative windows-attack-diagrams/gpo_abuse_animation.html %}

- If standard user groups (like *Domain Users* or *Authenticated Users*) are mistakenly given permission to edit a GPO, attackers can modify it to deploy malicious scripts or scheduled tasks to all linked computers.
    
    ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2026.png)
    
- Even if the GPO itself is secure, if it executes scripts or installs software from a poorly secured network share, an attacker can simply replace the legitimate files with malware.

#### Prevention

- One way to prevent this attack is to lock down the GPO permissions to be modified by a particular group of users only or by a specific account
- never deploy files stored in network locations so that many users can modify the share permissions.

#### Detection

- Inspect **EventID** **5136 (A directory service object was modified)**

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2027.png)

- Use **Honey pot,** follow these mindsets when setup:
    - Only link the honeypot GPO to **non-critical**.
    - There must be an automated continuous monitoring system.
    - Automatically unlink the honeypot GPO and immediately disable the user responsible for modifying it if tampering is detected.
    
    ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2028.png)
    

#### Labs

> **From WS001 RDP again into DC1 (172.16.18.3) as 'htb-student:HTB_@cademy_stdnt!' and abuse GPO directly. Once completed type DONE as the answer**
> 

**Answer: DONE**

### Credentials in Shares

#### Description

- **Credentials exposed in network shares** mean leave unencrypted credentials and authorization tokens scattered everywhere.
    - **Credentials in network** shares within scripts and configuration files (batch, cmd, PowerShell, conf, ini, and config).
    - **Credentials on a user's local machine** primarily reside in text files, Excel sheets, or Word documents.
- Reason why shares folder accidentally open for everyone
    - Provide privillege to Users group not knowing is include every users inside domain
    - Storing code files containing passwords on a local hard drive but forgetting that the folder is publicly shared on the network.
    - Opening up folder access temporarily to quickly transfer files but then forgetting to lock it down again.
    - Append $ to the folder name to hide it on Windows, but hacker scanning tools will still clearly see it.

#### Attack path

{% include_relative windows-attack-diagrams/share_creds_animation.html %}

- Identifying what shares exist in a domain.
- Use **Invoke-ShareFinder** to search for all shares folder

#### Prevention

- For users,  lock down every share in the domain so there are no loose permissions.
- For administrators, performing regular scans (e.g., weekly) on AD environments

#### Detection

- Inspect **EventID** **4624 (An account was successfully logged on)**,   **EventID** **4625 (An account failed to log on).** Analyzing users' behavior



- Search for the NetBIOS name of the domain because attackers often use this to search for passwords.
- Use **Honey pot,** follow these mindsets when setup:
    - A service account that was created **2+ years ago**. The last password change should be at least one year ago.
    - The last modification time of the file containing the fake password must be after the last password change of the account. Because it is a fake password, there is no risk of a threat agent compromising the account.
    - The account is still active in the environment.
    - The script containing the credentials should be realistic. (For example, if we choose an MSSQL service account, a connection string can expose the credentials.)

#### Labs

> **Connect to the target and enumerate the available network shares. What is the password of the Administrator2 user?**
> 

To perform the attack, first i have to access Powersploit script “**PowerView.ps1**”.

Luckily, they already put it inside Download folder, so everything that i have to do now is to access it with PowerShell and run the script.

By default, Windows sets its PowerShell **Execution Policy** to Restricted, protecting the system from malicious code. To turn is off easily, I run this command

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

And then run the script:

```bash
Import_Module .\PowerView.ps1
Invoke-ShareFinder
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2029.png)

Navigating to this directory using cd, I tried searching for **files containing the NetBIOS name of the domain.**

```bash
findstr /s /i /m "eagle" *
```

there are two files: **connect.ps1** and **connect2.ps1**. Using the cat command to view their contents, I found the password for the **Administrator2**

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2030.png)

**Answer: Slavi920**

### Credentials in Object Properties

#### Description

- Every object, like a user account, a computer, or a group, has a set of fields called **properties.**
- One of them is the **Description** property, a free-text field intended for administrators to add a helpful note or comment about the object.
- Password can be accidentally stored here

#### Attack path

{% include_relative windows-attack-diagrams/object_creds_animation.html %}

- Easily write a script to get this
- Use **PowerView**, **BloodHound** or **LDAP Query Tools**

#### Prevention

- **Perform continuous assessments** and **Educate employees**

#### Detection

- Inspect **Event ID** **4624 (An account was successfully logged on)**,   **Event ID** **4625 (An account failed to log on)** or **Event ID 4768 (A Kerberos Ticket Granting Ticket (TGT) was requested).** Analyzing users' behavior

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2031.png)

- Use **Honey pot,** follow these mindsets when setup:
    - A service account that was created **2+ years ago**. The last password change should be at least one year ago.
    - The account is still active in the environment.
    - The object containing the credentials should be realistic.

#### Labs

> **Connect to the target and use a script to enumerate object property fields. What password can be found in the Description field of the bonni user?**
> 

I rewrote the script to understand it better

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2032.png)

Then I ran this file to scan for Objects.

By default, Windows sets its PowerShell **Execution Policy** to Restricted, protecting the system from malicious code. To turn is off easily, I run this command

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

And then run the script:

```bash
Import_Module .\ObjectDiscover.ps1
SearchUserClearTextInformation
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2033.png)

**Answer: Slavi1234**

> **Using the password discovered in the previous question, try to authenticate to DC1 as the bonni user. Is the password valid?No**
> 

To log in with this account into DC01, I used Remote Desktop Connection

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2034.png)

The result is that it cannot be used to log in

**Answer: No**

> **Connect to DC1 as 'htb-student:HTB_@cademy_stdnt!' and look at the logs in Event Viewer. What is the TargetSid of the bonni user?**
> 

To confirm the failed login attempt and extract the TargetSid of the bonni user, I RDP’d into **DC1** as **htb-student.**

From **Event Viewer**, I filtered for logs with **Event ID 4771** (Kerberos Pre-Authentication failures). Searching these logs, I found an entry for bonni, which included the SID.

**Answer: S-1-5-21-1518138621-4282902758-752445584-3102**

### DCSync

#### Description

**DCSync** is an attack that threat agents utilize to **impersonate a Domain Controller** and perform **replication** with a targeted Domain Controller to extract password hashes from Active Directory. The attack can be performed both from the perspective of *a user account* or *a computer*, as long as they have the necessary permissions assigned, which are:

- Replicating Directory Changes
- Replicating Directory Changes All

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2035.png)

#### Attack path

{% include_relative windows-attack-diagrams/dcsync_animation.html %}

- Start a new command shell running as the user account that have 2 configurations on

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2036.png)

```bash
runas /user:eagle\rocky cmd.exe
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2037.png)

- Use **Mimikatz**, one of the tools with an implementation for performing DCSync

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2038.png)

- Perform **pass-the-hash** with the obtained hash and authenticate against any Domain Controller.

#### Prevention

- Using solutions such as the [RPC Firewall](https://github.com/zeronetworks/rpcfirewall), a third-party product that can block or allow specific RPC calls with robust granularity

#### Detection

- Inspect **Event ID 4662 (An operation was performed on an object)**

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2039.png)

#### Labs

> **Connect to the target and perform a DCSync attack as the user rocky (password:Slavi123). What is the NTLM hash of the Administrator user?**
> 

Change user to get the necessary permissions (password is `Slavi123`)

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2040.png)

Navigate to the folder to use **mimikatz.exe**

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2041.png)

Dump it out

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2042.png)

**Answer: fcdc65703dd2b0bd789977f1f3eeaecf**

> **After performing the DCSync attack, connect to DC1 as 'htb-student:HTB_@cademy_stdnt!' and look at the logs in Event Viewer. What is the Task Category of the events generated by the attack?**
> 

Access Event ID 4622 **(An operation was performed on an object)** to see the latest access behavior to the DC

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2043.png)

You can see there is 1 regular user (which is Rocky) who directly accessed the root object of the Domain

**Core Attack Indicators:**

- **AccessMask:** `0x100` corresponding to *Control Access* permission.
- **Properties:** Contains GUID `{1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}`, which represents the **DS-Replication-Get-Changes-All** permission.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2044.png)

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2045.png)

**Answer: Directory Service Access**

### Golden Ticket

#### Description

- A forged Kerberos TGT created by an attacker. It allows them to impersonate any user and gain privileges, effectively acting as a Domain Controller.
- **krbtgt Account:** A special, built-in account whose password hash is used by the KDC to sign all Kerberos tickets, making its hash the most critical secret in the domain.
- This is a post-exploitation technique used for persistence. An attacker must first gain high-level privileges (like Domain Admin) to steal the `krbtgt` hash.
- An attacker with the `krbtgt` hash can create a Golden Ticket to regain Domain Admin access at any time, even if their initial compromised account is discovered and removed. It also allows escalating privileges from a compromised child domain to its parent domain within a forest.

#### Attack path

{% include_relative windows-attack-diagrams/golden_ticket_animation.html %}

- The attacker uses **Mimikatz** with **DCSync** privileges to request the password hash for the **krbtgt** account from the Domain Controller

```bash
lsadump::dcsync /domain:eagle.local /user:krbtgt
```

- The attacker needs the Security Identifier (SID) of the entire domain. This is a unique value that identifies the domain.

```bash
Get-DomainSID (from the PowerView script).
```

- Create a valid ticket for any user, including a highly privileged one.

```bash
kerberos::golden /domain:eagle.local /sid:[Domain SID] /rc4:[krbtgt hash] /user:Administrator /id:500 /ptt
```

- The `/ptt` (Pass-the-Ticket) argument tells `Mimikatz` to inject the newly created Golden Ticket directly into the current user's session memory
- Verify that by running the command `klist`
- Verify that by list the content of the `C$` share of `DC1` using it

#### Prevention

#### Detection

- Inspect **Event ID 4624 (An account was successfully logged on).** An attacker using a Golden Ticket will generate logon events that *don't fit the normal pattern* of behavior for that account. Monitor for privileged accounts (like Administrator or other Domain Admins) logging on from unexpected places.
- Inspect **Event ID 4769 (A Kerberos service ticket was requested)** Look for anomalous behavior where an account requests a specific service access ticket (TGS) while skipping the mandatory step of obtaining an overall identity verification ticket (TGT) first.

#### Labs

> **Practice the techniques shown in this section. What is the NTLM hash of the krbtgt user?**
> 

To create a ticket, I need the hash of **krbtgt** and the **SID** of the entire domain. First, retrieve the hash of the **krbtgt** using the DCSync technique**:**

Change user to get the necessary permissions (password is `Slavi123`)

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2040.png)

Navigate to the folder to use mimikatz.exe

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2041.png)

Dump the hash credential of the krbtgt user

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2046.png)

Next, to get the SID, first i have to access Powersploit script “**PowerView.ps1**”.

Luckily, they already put it inside Download folder, so everything that i have to do now is to access it with PowerShell and run the script.

By default, Windows sets its PowerShell **Execution Policy** to Restricted, protecting the system from malicious code. To turn is off easily, I run this command

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

And then run the script:

```bash
Import-Module .\PowerView.ps1
Get-DomainSID
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2047.png)

Ok now, let cook the ticket and pass it to the current session

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2048.png)

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2049.png)

We got full access now, even though it only asked for the hash, I went ahead and found everything, lol

**Answer: db0d0630064747072a7da3f7c3b4069e**

### Kerberos Constrained Delegation

#### Description

- **Kerberos Delegation** enables a frontend application to access resources hosted on a backend server on behalf of a user, preventing the need to grant direct backend access to the service account itself.
- Active Directory supports three types of delegations: **Unconstrained**, **Constrained**, and **Resource-based Delegation**.
    - **Unconstrained delegation** is the most permissive type, allowing an account to delegate to any service.
    
    ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2050.png)
    
    - **Constrained delegation** requires a user account to have its properties configured to specify the exact service(s) it is permitted to delegate.
    
    ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2051.png)
    
    - **Resource-based delegation** is configured within the target computer object to explicitly specify which accounts it trusts.
    
    ![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2052.png)
    
- All forms of delegation represent a **potential security risk** and should be avoided unless strictly necessary.

#### Attack Path

{% include_relative windows-attack-diagrams/kcd_animation.html %}

- In a **constrained delegation attack**, a compromised trusted account sends a request to the **Key Distribution Center (KDC)** to generate a Kerberos ticket for a target user without needing that user's password.
- Threat actors can perform **protocol transition** to obtain access to services not explicitly configured in the user's delegation properties.
    - Enumerate domain accounts trusted for constrained delegation using enumeration tools (e.g., querying for the `TRUSTED_TO_AUTH_FOR_DELEGATION` flag).
    - Convert the compromised delegation account's plaintext password into an **NTLM hash** to prepare for ticket requests.
    - Utilize the **S4U (Service for User) extension** to request a forged ticket for a **highly privileged user** and inject it directly into memory.
    - Verify the successful injection of the ticket into the current session using native ticket-listing commands.
    - Impersonate the privileged user to establish a remote session and connect to the target server.

#### Prevention

- Configure the specific property **Account is sensitive and cannot be delegated** for all privileged user accounts.
- Add privileged users to the **Protected Users** group, which automatically enforces protection against account delegation.
- Treat any account configured for delegation as **extremely privileged**, regardless of its standard Active Directory group memberships.
- Enforce **cryptographically secure passwords** for all delegated accounts to ensure threat actors cannot obtain these privileges via offline password cracking.

#### Detection

- Inspect **EventID 4624 (Successful Logon)** to proactively monitor and alert on privileged users authenticating from unauthorized or unexpected workstations.

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2053.png)

- Correlate **user behavior** (including standard login times, locations, and origins) to identify anomalous activities indicating **constrained delegation abuse**.
- Inspect the **Transited Services** attribute within event logs for successful logon attempts.
- The **Transited Services** attribute is populated with the ticket issuer's information when a logon results from an **S4U (Service For User)** logon process.

#### Labs

> **Use the techniques shown in this section to gain access to the DC1 domain controller and submit the contents of the flag.txt file.**
> 

By default, Windows sets its PowerShell **Execution Policy** to Restricted, protecting the system from malicious code. To turn is off easily, I run this command

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

And then run the script in Downloads folder:

```bash
Import-Module .\PowerView-main.ps1
Get-NetUser -TrustedToAuth # find user accounts configured for Constrained Delegation with Protocol Transition
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2054.png)

```bash
.\Rubeus.exe hash /password:Slavi123
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2055.png)

```bash
.\Rubeus.exe s4u /user:webservice /rc4:FCDC65703DD2B0BD789977F1F3EEAECF /domain:eagle.local /impersonateuser:Administrator /msdsspn:"http/dc1" /dc:dc1.eagle.local /ptt
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2056.png)

With the ticket being available, we can connect to the Domain Controller impersonating the account `Administrator` 

```bash
Enter-PSSession dc1
```

![image.png](/assets/img/cdsa/sec6-windows-attacks-defense/image%2057.png)

**Answer: C0nsTr@in3D_F1@G_Dc01!**

### Print Spooler & NTLM Relaying

#### Description

- The **Print Spooler** is a legacy service enabled by default on most Windows Desktop and Server versions.
- **The PrinterBug:** Discovered in 2018, this "by-design" vulnerability allows attackers to abuse the `RpcRemoteFindFirstPrinterChangeNotification` and `RpcRemoteFindFirstPrinterChangeNotificationEx` functions.
- Exploiting this forces a remote machine to initiate a connection to any other reachable machine. This reverse connection carries authentication information (such as a TGT), effectively coercing the remote server to authenticate to the attacker.
- **Impact on Domain Controllers (DCs):** If the Print Spooler is enabled on a DC, it can be compromised in several ways:
    - **DCSync:** Relay the connection to another DC to extract password hashes (requires SMB Signing to be disabled).
    - **Unconstrained Delegation (UD):** Force the DC to connect to a UD-configured machine, caching the DC's TGT in memory for extraction via tools like Rubeus or Mimikatz.
    - **AD CS Relay:** Relay the connection to Active Directory Certificate Services to obtain a certificate and impersonate the DC.
    - **Resource-Based Constrained Delegation:** Relay the connection to configure delegation settings, allowing the attacker to authenticate as an Administrator to that machine.

#### Attack Path

{% include_relative windows-attack-diagrams/print_spooler_animation.html %}

- This specific path focuses on relaying the connection to another DC to perform a **DCSync** attack. **SMB Signing must be disabled** on the target Domain Controller for this to succeed.
    - The attacker configures a relay tool (e.g., **NTLMRelayx**) to listen for incoming connections and forward them to the target Domain Controller using the DCSync protocol.
    - The attacker utilizes an exploitation tool (e.g., **Dementor**) to trigger the PrinterBug on the victim machine. This requires valid domain user credentials.
    - The victim machine is coerced into authenticating back to the attacker's listening server.
    - The relay tool captures the authentication attempt, forwards it to the target DC, and successfully executes the DCSync attack, dumping domain credentials.

#### Prevention

- **Disable the Service:** The Print Spooler service should be completely disabled on all servers that do not explicitly require printing capabilities, especially Domain Controllers and core Active Directory infrastructure.
- **Registry Mitigation:** If the service must remain running, prevent remote abuse by modifying the registry to block incoming remote requests.
    - Modify the registry key: `RegisterSpoolerRemoteRpcEndPoint`
    - Set the value to **2** (Disables remote clients).

#### Detection

- Inspect **EventID 4624 (Successful Logon)** to identify authentication events for core infrastructure servers originating from unexpected, non-static IP addresses.
- **Correlate logon attempts** from Domain Controllers to ensure they match their respective, known IP addresses, as relay attacks will show the successful logon originating from the attacker's machine rather than the actual DC.
- **Note on DCSync Logging:** Relying on standard directory service access events is ineffective for this specific relayed attack path, as no standard DCSync event flags are generated.
- **Honeypot & Network Monitoring:** Monitor for blocked outbound connections on **ports 139 and 445** from servers. If strict firewall rules are implemented to block outbound SMB traffic, any blocked reverse connections act as immediate, high-fidelity indicators of compromise.

#### Labs

> **What is Kerberos des-cbc-md5 key for user Administrator?**
> 

**Answer:**

> **After performing the previous attack, connect  to DC1 (172.16.18.3) as 'htb-student:HTB_@cademy_stdnt!' and make the 
appropriate change to the registry to prevent the PrinterBug attack. 
Then, restart DC1 and try the same attack again. What is the error 
message seen when running dementor.py?**
> 

**Answer:**

### Coercing Attacks & Unconstrained Delegation

#### Description

- **Coercing attacks** provide a direct path for escalating privileges from a standard domain user to Domain Administrator, affecting nearly all default Active Directory infrastructures.
- Attackers abuse various **RPC functions** to coerce a target server (like a Domain Controller) into authenticating to an attacker-controlled machine.
- The **Coercer** tool automates this by systematically exploiting all known vulnerable RPC functions simultaneously.
- **Exploitation Impact:** Once the target is coerced into connecting, attackers can perform several follow-up attacks:
    - Perform a **DCSync** attack via relay (if SMB Signing is disabled).
    - Force the connection to a machine with **Unconstrained Delegation (UD)** to capture the target's Ticket Granting Ticket (TGT).
    - Relay to **Active Directory Certificate Services (AD CS)** to impersonate the Domain Controller.
    - Configure **Resource-Based Kerberos Delegation** for the relayed machine.

#### Attack Path

{% include_relative windows-attack-diagrams/ud_coercion_animation.html %}

- This path focuses on forcing a Domain Controller to authenticate to a compromised server configured with **Unconstrained Delegation**.
    - Enumerate the domain to identify servers trusted for Unconstrained Delegation using Active Directory enumeration tools.
    - Execute a monitoring tool (e.g., **Rubeus**) on the compromised UD server to continuously listen for and capture new incoming TGTs.
    - Trigger the coercing tool from the attacker's machine, targeting the Domain Controller and forcing it to authenticate to the compromised UD server.
    - Extract the Domain Controller's base64-encoded TGT that was cached in the UD server's memory.
    - Perform a **Pass-the-Ticket (PTT)** attack to inject the stolen TGT into the current session, effectively impersonating the Domain Controller.
    - Leverage the elevated privileges to execute a **DCSync** attack and dump domain credentials.

#### Prevention

- Windows does not offer native, granular visibility or control over specific RPC calls out-of-the-box.
- **RPC Firewalls:** Implement third-party RPC firewalls to monitor, audit, and explicitly block dangerous RPC functions or specific **OPNUMs** associated with coercing.
- **Outbound Traffic Restriction:** Block Domain Controllers and core infrastructure servers from initiating **outbound connections on ports 139 and 445**, except to strictly required infrastructure (e.g., other DCs for replication). This prevents the required reverse connection from succeeding, regardless of the RPC vulnerability used.

#### Detection

- Inspect **EventID 5156 / 5157 (Windows Filtering Platform Connection Allowed / Blocked)** within host firewall logs to identify anomalous network connection sequences.
- Correlate **incoming connections** to a Domain Controller with immediate **outbound connections** directed back to the requesting IP address on **port 445**.
- Monitor for **dropped outbound traffic** directed toward ports 139 or 445 from core servers; unexpected drops often indicate a coercing attempt that was successfully blocked by network policies.
- Monitor **third-party RPC firewall logs** (if deployed) for the specific abuse of known dangerous RPC functions.

#### Labs

> **Repeat the example shown in the section, and type DONE as the answer when you are finished**
> 

**Answer:**

### Object ACLs

#### Description

- **Access Control Lists (ACLs)** define which security principals (trustees such as users, groups, or sessions) have access to a securable object and specify their exact level of access.
- Each ACL is composed of multiple **Access Control Entries (ACEs)**, allowing multiple trustees to hold different permissions on the same object.
- Permissions can be delegated to standard accounts to execute specific actions on other objects (e.g., password resets, modifying group memberships, or object deletion).
- Over-permissive environments frequently suffer from excessive rights, such as domain users having administrative rights over servers, full write permissions to sensitive objects, or read access to extended properties storing **LAPS passwords**.

#### Attack Path

{% include_relative windows-attack-diagrams/object_acls_animation.html %}

- Attackers run ingestion tools (e.g., **SharpHound**) to collect domain relationships, group memberships, sessions, and ACLs across the directory.
- The collected data is visualized in **BloodHound** to reveal hidden privilege escalation paths based on misconfigured object permissions.
- **Abusing User Object Rights:**
    - *Password Reset:* If the attacker has write access or reset permissions over a privileged account, they can directly overwrite the target's password and inherit their permissions.
    - *Targeted Kerberoasting:* The attacker can write an arbitrary **Service Principal Name (SPN)** to a target user object and subsequently request and crack a Kerberos TGS ticket offline.
- **Abusing Computer Object Rights:**
    - *Credential Access:* The attacker can read protected attributes containing the local administrator credentials (such as **LAPS** attributes).
    - *Resource-Based Constrained Delegation (RBCD):* The attacker writes to the target computer's `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute to configure delegation and impersonate an administrative session to that machine.

#### Prevention

- Conduct **continuous security assessments** using auditing tools (e.g., **ADACLScanner**) to discover and map discretionary access control lists (DACLs) and system access control lists (SACLs).
- Enforce the **Principle of Least Privilege** and eliminate manual privilege granting by automating identity and access management workflows.
- Limit administrative and delegation rights strictly to designated administrative accounts rather than standard user accounts.
- Establish strict offboarding and departmental transfer processes to immediately revoke residual access and delegated rights.

#### Detection

- Inspect **EventID 4738 (A user account was changed)** to monitor modifications to user objects, alerting when non-administrative accounts perform modifications or attempt unauthorized SPN additions.
- Inspect **EventID 4724 (An attempt was made to reset an account's password)** to catch unauthorized password resets executed through delegated ACL rights.
- Inspect **EventID 4742 (A computer account was changed)** to detect modifications made directly to computer object attributes (such as RBCD configurations).
- **Baseline Account Behavior:** Correlate user modification events against designated administrative naming conventions or Privileged Access Workstations to identify anomalous modification sources.
- Use **Honey pot**, follow these mindsets when setup:
    - Create a decoy account/object (e.g., assign high ACLs or grant broad modification permissions to multiple users) while simulating realistic user activity.
    - Ensure an automated system continuously monitors all interactions with the decoy object.
    - If unauthorized tampering is detected (**EventID 4738**), immediately disable the user account responsible for the modification (**EventID 4725**) and isolate the system for investigation.

#### Labs

> **Repeat the example in the section and type DONE as the answer when you are finished**
> 

**Answer:**

### PKI - ESC1

#### Description

- **Active Directory Certificate Services (AD CS)** is a critical public key infrastructure (PKI) component widely targeted for privilege escalation and long-term persistence due to prevalent template misconfigurations.
- **Advantages of Certificate Abuse:**
    - Certificates are typically valid for extended durations (often 1+ years).
    - **Password resets do not invalidate certificates**, allowing continued access regardless of account credential updates until the certificate explicitly expires or is revoked.
    - Compromise of the Certificate Authority (CA) private key enables the forging of Golden Certificates.
- **ESC1 Misconfiguration Profile:**
    - **No Issuance Requirements:** Manager approval is not required, and authorized signatures are set to 0.
    - **Enrollable Client Authentication:** The template contains Extended Key Usage (EKU) flags supporting authentication (e.g., Client Authentication, Smart Card Logon).
    - **CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT:** The template allows the requester to supply their own Subject Alternative Name (SAN), permitting any user with enrollment rights to request a certificate impersonating arbitrary domain identities (including Domain Administrators).

#### Attack Path

{% include_relative windows-attack-diagrams/pki_esc1_animation.html %}

- Attackers scan the PKI environment using auditing tools (e.g., **Certify**) to locate misconfigured certificate templates matching the ESC1 pattern.
- The attacker requests a certificate from the CA under the vulnerable template while supplying an alternate identity (e.g., Domain Administrator) in the **SAN** parameter.
- The CA signs and returns the requested certificate containing the requested high-privilege SAN.
- The returned certificate is converted into a standard usable format (e.g., PFX) with local cryptographic utilities.
- The attacker uses authentication tools (e.g., **Rubeus**) to initiate Kerberos PKINIT pre-authentication against the Domain Controller, exchanging the certificate for a valid Kerberos **Ticket Granting Ticket (TGT)** for the impersonated identity.
- The forged TGT is passed into memory to access administrative network resources (e.g., remote administrative file shares or interactive shells).

#### Prevention

- **Disable SAN Specification:** Remove the `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` flag on sensitive or client-authenticating certificate templates to prevent requesters from specifying custom SAN values.
- **Require Manager Approval:** Enforce **CA Certificate Manager Approval** on certificate templates so requests require manual verification before issuance.
- **Restrict Enrollment Rights:** Strictly limit enrollment permissions to only the specific user and computer groups that strictly require the template, removing default broad groups like `Domain Users` or `Authenticated Users`.
- **Routine Environment Audits:** Regularly scan the AD CS infrastructure using tools like **Certify** to identify newly introduced template misconfigurations.

#### Detection

- Inspect **EventID 4886 (Certificate Services received a certificate request)** on the Certificate Authority server to monitor incoming enrollment requests and examine the requested template name and requester identity.
- Inspect **EventID 4887 (Certificate Services approved a certificate request and issued a certificate)** on the Certificate Authority server to identify when certificates associated with high-risk templates are issued.
- Inspect **EventID 4768 (A Kerberos authentication ticket (TGT) was requested)** on Domain Controllers to detect authentication utilizing certificates via **PKINIT**, noting certificate-based logon attributes and mismatches between enrollment context and account identity.
- **Automate CA Audit Queries:** Periodically query the CA database (e.g., via `certutil -view` or dedicated PowerShell scripts) to inspect the **Subject Alternative Name (SAN)** extensions of recently issued certificates for administrative impersonation.

#### Labs

> **Connect to the Kali host first, then RDP to WS001 as 'bob:Slavi123' and practice the techniques shown in this section. What is the flag value located at \\dc1\c$\scripts?**
> 

**Answer:**

> **After performing the ESC1 attack, connect to PKI (172.16.18.15) as 'htb-student:HTB_@cademy_stdnt!' and look at the logs. On what date was the very first certificate requested and issued?**
> 

**Answer:**