---
title: "SOC HTB - Section 4: Introduction to Threat Hunting & Hunting With Elastic"
date: 2026-06-07 00:00:00 +0700
categories: [HTB SOC Jobpath]
tags: [cdsa, study-notes, htb-soc-jobpath, threat-hunting, elastic]
---

# Introduction to Threat Hunting & Hunting With Elastic

# Threat Hunting Fundamentals

## Threat Hunting Definition

- The average time from when a system is compromised until it is detected is called **dwell time**, which often lasts from a few weeks to several months.
- The core objective of the Threat Hunting process is to minimize **dwell time** by detecting threats at an early stage of the **cyber kill chain**, preventing attackers from establishing a foothold in the infrastructure.
- The nature of this activity is a proactive, human-led, and **hypothesis-driven** process aimed at hunting down sophisticated threats that bypass automated security systems.
- The fundamental process always begins with identifying high-value assets, followed by analyzing the attacker's **TTPs (Tactics, Techniques, and Procedures)** to proactively detect and isolate anomalies compared to standard baselines.
- Experts consistently leverage **Threat Intelligence** as an essential component to build hypotheses, counter-tactics, and preventative measures.
- Practitioners must possess **cognitive empathy** with attackers to understand their mindset, along with a deep understanding of the organization's network topology and digital assets.
- This activity strictly requires using highly reliable data sources combined with advanced tactical analysis platforms.

## The Relationship Between Incident Handling & Threat Hunting

- The **Preparation Phase** requires establishing clear **Rules of Engagement** to determine whether to build an independent operational process or integrate it directly into existing incident response policies.
- During the **Detection & Analysis Phase**, the hunting team uses an offensive mindset to help verify **Indicators of Compromise (IoCs)** and uncover artifacts that might have been missed.
- In the **Containment, Eradication, & Recovery Phase**, team members may directly participate in incident response or continue monitoring the network surface depending on the organization's internal regulations.
- During the **Post-Incident Activity Phase**, experts contribute their technical expertise to propose improvements and comprehensively strengthen the system's **security posture**.
- The decision to merge or separate these two processes depends entirely on the specific risk context and resources of each organization.

## A Threat Hunting Team's Structure

### Core & Analytical Roles

- The core force of the team consists of **Threat Hunters** who deeply understand **TTPs** and proactively hunt for **IoCs** through specialized platforms.
- The task of gathering intelligence from open-source resources or the dark web to forecast attack trends is handled by the **Threat Intelligence Analyst**.
- Processing massive datasets using statistical models and Machine Learning to uncover hidden patterns is the responsibility of **Data Analysts/Scientists**.

### Response & Forensics Roles

- **Incident Responders** will immediately take over upon detecting a threat to investigate, contain, eradicate, and recover the system.
- **Forensics Experts** specializing in **DFIR (Digital Forensics and Incident Response)** will directly analyze malware, reverse-engineer code, and draft detailed technical reports.

### Engineering & Management Roles

- The entire security infrastructure and defensive tools aligned with the kill-chain are designed and operated by **Security Engineers/Architects**.
- Monitoring behavior and rapidly detecting anomalies in network traffic falls under the expertise of the **Network Security Analyst**.
- Overseeing operations, coordinating team members, and ensuring seamless communication within the security operations center is the responsibility of the **SOC Manager**.

## When Should We Hunt?

- A hunting campaign should be triggered immediately whenever there is **new intelligence** regarding an attack group or vulnerabilities directly related to the systems currently in use.
- The security team must act when there are **new IoCs** belonging to APT groups with a history of targeting the organization or similar targets in the same industry.
- The occurrence of **multiple consecutive anomalies** in network traffic is a clear warning signal of an organized attack that requires immediate investigation.
- The hunting process must always run concurrently with **incident response (IR) activities** to determine the full scope of infection and any hiding threats.
- Organizations need to maintain **periodic and continuous hunting** campaigns to proactively detect hidden risks that slip through standard security filters.

## The Relationship Between Risk Assessment & Threat Hunting

- The **Risk Assessment** process provides a comprehensive view of attack vectors, helping organizations allocate hunting efforts towards the most critical areas.
- Risk assessment data helps direct security resources to the most important assets, also known as the **crown jewels** of the system.
- Security teams utilize assessment results to grasp the attacker's **TTPs**, creating a solid foundation for building accurate hunting hypotheses.
- Known application vulnerabilities are used as leads to guide the hunt in searching for signs of privilege escalation or exploit attempts.
- Risk assessment also helps precisely identify the threat actors with the highest attack likelihood, enabling the effective application of **Threat Intelligence**.
- The results of risk analysis play a backbone role in improving incident response plans (**IR plans**) and upgrading cybersecurity control measures.
- Hunting activities are often optimized by integrating vulnerability scanning platforms and **SIEM (Security Information and Event Management)** systems for centralized event correlation.

# The Threat Hunting Process

- The initial **Setting the Stage** phase requires enabling comprehensive logging systems across **SIEM**, **EDR**, and **IDS** tools, along with thoroughly analyzing intelligence reports to grasp the attacker's **TTPs** to pinpoint the critical assets that must be protected.
- The next step is **Formulating Hypotheses** by constructing practical and testable hypotheses based on intelligence information, security alerts, or professional experience to guide the areas that need to be swept.
- During the **Designing the Hunt** phase, the security team bounds the necessary data sources, builds custom queries, and maps out specific **IoCs** to hunt for.
- **Data Gathering and Examination** occurs through the continuous collection and analysis of log files, network traffic, and endpoint data using statistical methods or behavioral analysis to find conclusive evidence to validate or refute the initial hypothesis.
- In the **Evaluating Findings** step, experts interpret the analysis results to confirm the threat, analyze infection behaviors, and determine the full scope of impact on the network infrastructure.
- When an attack is confirmed, the **Mitigating Threats** process is immediately triggered to isolate affected systems, eradicate malware, patch vulnerabilities, and fine-tune security configurations.
- The **After the Hunt** phase requires documenting the entire process, updating newly discovered **IoCs** into the intelligence platform, and optimizing **incident response playbooks**.
- The essence of hunting activities is a cycle of **Continuous Learning and Enhancement**, constantly refining tools, machine learning algorithms, and methodologies based on learned lessons and the ever-changing risk landscape.

# Threat Hunting Glossary

## Threat Actors & Core Concepts

- An **Adversary** in **Cyber Threat Intelligence (CTI)** is an unauthorized entity seeking to infiltrate the infrastructure for financial gain, stealing internal information, or intellectual property.
- These threat actors are classified into various specific groups such as cybercriminals, insider threats, hacktivists, or government-sponsored espionage units.
- The concept of **Advanced Persistent Threat (APT)** generally refers to highly organized groups backed by massive resources to maintain long-term, entrenched campaigns aimed at high-value targets like governments, healthcare, or defense.
- The "Advanced" factor in **APT** does not necessarily mean using complex techniques but implies a sophisticated planning strategy, while "Persistent" demonstrates the endurance to maintain a foothold thanks to strong financial and personnel capabilities.
- A **Campaign** is a collection of security incidents sharing common attack methods and collection goals, requiring defensive teams substantial time and effort to cross-reference data.
- The concept of a **Threat** is constituted by three core elements: **intent** (the motive to attack), **capability** (technical prowess, tools, finance), and **opportunity** (the chance or favorable vulnerability to exploit).

![image.png](/assets/img/cdsa/sec4-intro-to-threat-hunting-elastic/image.png)

## Tactics, Techniques, and Procedures (TTPs)

- The term **TTPs** represents distinctive activity patterns, acting as a campaign "signature" of a specific attack group.
- **Tactics** describe strategic objectives and high-level operational concepts, answering "why" the attacker performs that action.
- The specific methods used to achieve tactical goals are called **Techniques**, providing an overview of "how" it is executed.
- The most detailed, step-by-step, and micro-level instructions to execute a technique are defined as **Procedures**.

## Indicators of Compromise & The Pyramid of Pain

![image.png](/assets/img/cdsa/sec4-intro-to-threat-hunting-elastic/image%201.png)

- An **Indicator** in **CTI** analysis must include both technical data and contextual information, helping defenders accurately assess severity rather than merely looking at lifeless numbers.
- Digital traces or **artifacts** extracted from intrusions are called **Indicators of Compromise (IOCs)**, acting as "signposts" that aid in the early detection of malicious activity.
- The **Pyramid of Pain** model illustrates the hierarchy of infection indicators, representing the level of difficulty for an attacker when they are forced to change tactics due to being detected.

![image.png](/assets/img/cdsa/sec4-intro-to-threat-hunting-elastic/image%202.png)

- At the bottom of the pyramid are **Hash Values** (digital fingerprints of files), which are the least reliable indicators because attackers can easily alter a hash just by adding or removing a single byte of data.
- **IP Addresses** are also an easily bypassed group of indicators as attackers frequently hide their real IPs via spoofing, VPNs, proxies, or TOR networks.
- Blocking **Domain Names** is slightly more difficult, but hackers can still generate bulk random domains via DGA algorithms or use Dynamic DNS to evade detection.
- Traces left on the infrastructure (like traffic patterns, packet headers) are called **Network Artifacts**, whereas changes on the server (like registry keys, background processes) are termed **Host Artifacts**; both are very difficult for an attacker to hide without breaking their campaign.
- The **Tools** group includes software, malware, or C2 frameworks used by the attacker; detecting a tool forces them to rewrite their code at a high cost.
- At the top of the pyramid are **TTPs**, which are the most valuable indicators and cost the attacker the most time and effort to completely change their operational methods if exposed.

## The Diamond Model of Intrusion Analysis

![image.png](/assets/img/cdsa/sec4-intro-to-threat-hunting-elastic/image%203.png)

- The **Diamond Model** provides a structured approach to analyzing an intrusion, comprising 4 vertices that possess a two-way interactive relationship with one another.
- The **Adversary** vertex represents the individual or organization behind the attack, requiring defenders to clearly understand their capabilities and motives.
- The **Capability** vertex encompasses all the tools, malware, and **TTPs** the attacker utilizes to execute the intrusion.
- The **Infrastructure** vertex represents physical and virtual resources (such as servers, domains, botnets) used to distribute malware or remotely control systems.
- The **Victim** vertex is the targeted objective, requiring the organization to re-evaluate existing vulnerabilities and core asset values.
- Compared to the Cyber Kill Chain, which solely focuses on linear attack phases, the **Diamond Model** offers a more comprehensive view of the intrusion ecosystem and its tightly knit interactive links.
- In practice, when analyzing a phishing campaign distributing a banking trojan, the financial institution is the **Victim**, the criminal group is the **Adversary**, the fraudulent email acts as the **Capability**, and the intermediary botnet is the **Infrastructure**.

# Threat Intelligence Fundamentals

## Cyber Threat Intelligence Definition

- The core objective of **Cyber Threat Intelligence (CTI)** is to transition an organization's defensive strategy from a passive state to proactive forecasting, thereby providing essential intelligence for the **Security Operations Center (SOC)**.
- Intelligence information only truly delivers value when it ensures **Relevance**, preventing the waste of resources on risks that do not affect the current infrastructure.
- The speed of information delivery, or **Timeliness**, determines defense efficacy, as analytical data rapidly loses value when an attacker shifts tactics or a vulnerability is patched.
- All analytical data must generate **Actionability**, meaning it provides clear and practical operational guidelines for network defense teams rather than generic information.
- Prior to distribution, intelligence must be rigorously verified for **Accuracy** along with specific confidence levels to avoid false alarms or wasting resources on misleading tactics.
- The convergence of these four elements helps an organization understand attack campaigns, unmask an adversary's **TTPs**, and support leadership in making effective strategic business decisions.

## The Difference Between Threat Intelligence & Threat Hunting

- **Threat Intelligence** activities are predictive, focusing on anticipating the location, time, operational strategy, and ultimate goal of the attacker.
- Conversely, **Threat Hunting** combines both **Reactive and Proactive** aspects, typically triggered by a suspicious sign to determine whether an attacker is lurking or has previously been present in the network.
- These two fields share a tight symbiotic relationship; intelligence profiles help steer hunting campaigns, while results from hunting provide factual data to refine the accuracy of intelligence reports.

## Criteria Of Cyber Threat Intelligence & Intelligence Types

- The collection and analysis of high-quality **CTI** helps leadership understand risks, build incident response plans, and is categorized into three closely intersecting levels.
- **Strategic Intelligence** is tailored specifically for senior leadership (C-suite), focusing on answering the **Who?** and **Why?** by linking intelligence with enterprise risks and outlining long-term attack trends.
- **Operational Intelligence** primarily serves middle management, delving deep into answering **How?** and **Where?** through detailed analysis of attack campaigns and an adversary's operational methods.
- **Tactical Intelligence** provides immediate technical data such as **Indicators of Compromise (IOCs)** to network defense teams to rapidly detect and prevent specific technical threats.
- These three types of intelligence do not operate independently; tactical information constantly contributes to shaping the operational campaign picture and vice versa, forming a comprehensive intelligence ecosystem.

## How To Go Through A Tactical Threat Intelligence Report

- The first step is **Comprehending the Report's Scope and Narrative** to grasp the macro context, the attacker's objective, and to evaluate the campaign's relevance to the organization's industry.
- Next is **Spotting and Classifying the IOCs** into distinct groups such as Network-based (IP, domain), Host-based (hash, registry), and Email-based for easy systematization and defense implementation.
- **Comprehending the Attack's Lifecycle** requires mapping the TTPs from the report into the **MITRE ATT&CK** framework to accurately forecast the attacker's moves from the intrusion phase until gaining administrative control.
- The **Analysis and Validation of IOCs** phase strictly necessitates cross-referencing data against reputable sources (like VirusTotal) to discard outdated indicators and minimize the **false positive rate**.
- After validation, the **Incorporating the IOCs** process integrates the data into firewall, **EDR**, and **IDS/IPS** systems, while simultaneously requiring a careful assessment of operational impacts on the business before setting up automatic block rules.
- Based on the report, the team will conduct **Proactive Threat Hunting** not only to sweep for static IOC sets but also to expand the search for anomalies based on broader TTPs, such as the abuse of PowerShell.
- This cycle concludes with **Continuous Monitoring and Learning**, consistently monitoring the system, adjusting detection rulesets, and actively contributing newly discovered IOCs back to the community via specialized intelligence platforms.