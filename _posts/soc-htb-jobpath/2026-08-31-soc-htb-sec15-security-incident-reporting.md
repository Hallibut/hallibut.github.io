---
title: "SOC HTB - Section 15: Security Incident Reporting"
date: 2026-08-31 00:00:00 +0700
categories: [HTB SOC Jobpath]
tags: [cdsa, study-notes, htb-soc-jobpath, incident-reporting]
---

## **Incident Report, Incident Identification and Categorisation**

### Purpose of an Incident Report

- **The Bridge:** Connects the initial threat identification to the final remediation steps.
- **The Archive:** Documents lessons learned to prevent future attacks.
- **Multi-Audience:** Must balance technical details with plain language to serve different stakeholders:
    - *Legal:* Regulatory compliance.
    - *Executives:* Risk profile assessment.
    - *Finance (CFO):* Financial impact evaluation.

### Threat Identification Sources

Incidents usually manifest as anomalies or deviations from a baseline. They are identified through three main channels:

- **Security Tooling:** Alerts from SIEM, EDR/XDR, IDS/IPS, NetFlow, or Anti-Virus.
- **Human Observation:** Internal staff reporting unusual system behavior or suspicious emails.
- **Third-Party Notifications:** External partners, vendors, or customers reporting a breach or vulnerability.

### Incident Categories

Categorizing an incident helps allocate the right resources quickly.

- **Malware:** Viruses, worms, ransomware.
- **Phishing:** Fraudulent attempts to steal data, usually via email.
- **DDoS:** Flooding networks to disrupt availability.
- **Unauthorized Access:** Intruders bypassing access controls.
- **Data Leakage:** Accidental or intentional exposure of confidential data.
- **Physical Breach:** Unauthorized entry into physical secure locations.

### Severity Levels

*Note: Severity and categories are **fluid** and can change dynamically as you gather more intelligence during your investigation.*

| **Level** | **Severity** | **Definition** | **Required Action** |
| --- | --- | --- | --- |
| **P1** | **Critical** | Imminent threat to core business functions or sensitive data. | Immediate intervention. |
| **P2** | **High** | Latent threats to business operations. | Elevated priority response. |
| **P3** | **Medium** | Does not pose an immediate threat to core operations. | Timely attention. |
| **P4** | **Low** | Trivial incidents or routine anomalies. | Manage within standard workflows. |

## **The Incident Reporting Process**

{% include_relative incident_reporting_process_diagram.html %}

## **Elements of a Proper Incident Report**

### The Executive Summary

This section is for a *broad, non-technical audience*. Many stakeholders will only read this part, so it must be clear.

- **Incident ID** - Always include a unique tracking number.
- **Incident Overview** - Explain what happened, the date and time, the duration, and if it is ongoing or resolved.
- **Key Findings** - State the root cause, any specific CVE exploited, and exactly what data was jeopardized.
- **Immediate Actions Taken** - Outline how systems were isolated and if third-party services were brought in.
- **Stakeholder Impact** - Translate the technical breach into business terms like financial loss, downtime, or exposed proprietary information.

### Technical Analysis

This is the most voluminous part of the report, detailing exactly how the attack unfolded.

- **Affected Systems and Data** - List compromised nodes and specify the exact volume of exfiltrated data.
- **Evidence Sources** - Document how you found the breach. You must *hash files* to maintain strict evidence integrity for legal cases.
- **Indicators of Compromise (IoCs)** - List the artifacts used to hunt for further infections and identify the threat actor.
- **Root Cause Analysis** - Detail the exact vulnerability or failure point that allowed the breach.
- **Technical Timeline** - Track the exact sequence of events from initial *reconnaissance* and *C2 communications* through *lateral movement*, *exfiltration*, and final *containment*.

### Response, Recovery, and Impact

This section proves what you did to stop the bleeding and restore the network.

- **Impact Analysis** - Quantify the operational damage, regulatory penalties, and reputational harm.
- **Immediate Response** - Detail exactly how and when you revoked access for compromised accounts.
- **Containment Strategy** - Explain short-term isolation tactics and long-term architectural fixes like network segmentation.
- **Eradication Measures** - Document your malware removal tools, how you verified the removal, and your step-by-step patch management process.
- **Recovery Steps** - Prove that you validated backups *before* restoration and ran security checks before bringing systems back online.
- **Post-Incident Actions** - Establish enhanced monitoring plans and conduct a gap analysis for *lessons learned*.

### Diagrams and Visuals

Complex narratives require visual aids to help the reader understand the flow.

- **Incident Flowchart** - Illustrates the overall progression of the attack.
- **Affected Systems Map** - Shows your network topology. Use color-coding to highlight the severity of compromised nodes.

![image.png](/assets/img/cdsa/sec15-security-incident-reporting/image.png)

- **Attack Vector Diagram** - Uses arrows and annotations to visually trace the attacker's path through your defenses.

![image.png](/assets/img/cdsa/sec15-security-incident-reporting/image%201.png)

### The Appendices

This repository holds the raw data that gives your report credibility.

- Include verifiable artifacts like **log files**, **forensic evidence** (disk and memory dumps), *code snippets*, and **network diagrams**.
- Store administrative records like communication logs, signed NDAs, and a glossary of terms.

### Core Best Practices

- Always hunt for the absolute **root cause** rather than just treating symptoms.
- Keep stakeholders looped in with **regular updates** throughout the entire process.
- Consider hiring **external specialists** to validate your team's findings.
- Share non-sensitive details with the *wider cybersecurity community* to improve collective defense.

## **Communications**

### The "Why" of Incident Communications

Handling a crisis requires more than just technical fixes. Effective communication is the glue that holds the response together.

- **Stakeholder Trust** - Transparent messaging proves your organization has *command over the situation*.
- **Coordination** - Keeps the technical responders and the broader organization perfectly *aligned*.
- **Compliance** - Ensures you follow the legal mandates explicitly documented in your **Incident Response Plan (IRP)**.

### Internal vs. External Messaging

You must segment how you talk to your own team versus how you talk to the outside world.

**Internal Communications**

- **Immediate Notification** - Alert internal stakeholders the moment an incident is acknowledged to prevent rumors or leaks.
- **Regular Updates** - Disseminate periodic briefings so all departments share the exact same status and understanding.
- **Feedback Loop** - Create a dedicated conduit for teams to exchange findings, voice concerns, or offer technical suggestions.

**External Communications**

- **Affected Parties** - Reach out directly to impacted customers, clients, or business partners.
- **Public Statements** - Keep the language lucid and *steer clear of technical jargon* to prevent public confusion.
- **Regulatory Bodies** - Notify oversight entities within their strictly stipulated timeframes.

### Securing Your Channels (Technical Dimensions)

When discussing the *nitty-gritty* of an incident, your communication methods must be bulletproof.

- **Encryption** - Wrap all sensitive incident discussions in robust **end-to-end encryption**.
- **Strict Access** - Enforce **Multi-Factor Authentication (MFA)** to lock down who can join the channel.
- **Data Integrity** - Use *cryptographic hashing* to guarantee messages remain unaltered in transit.
- **Ephemeral Messaging** - Utilize auto-destructing platforms for *top-secret* discussions to minimize future exposure risks.
- **Air-Gapped Systems** - Resort to completely isolated, offline networks if you suspect your primary communication backbone is compromised.

### Navigating the Law (Regulatory Dimensions)

Security must be balanced with strict legal and regulatory mandates.

- **Data Privacy** - Adhere rigidly to frameworks like **GDPR** whenever personal data is involved.
- **Breach Notifications** - Abide by specific legal timelines and content guidelines mandated by your jurisdiction.
- **Record-Keeping** - Walk the tightrope between using secure *ephemeral messages* and laws that mandate a permanent record of all communications.
- **Cross-Border Rules** - Respect *data sovereignty laws* that dictate how data is transmitted when an incident spills over national borders.
- **Chain of Custody** - Maintain an unbroken trail of communications so your evidence remains legally *admissible in court*.