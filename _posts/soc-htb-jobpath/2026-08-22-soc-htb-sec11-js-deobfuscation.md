---
layout: post
title: "SOC HTB - Section 11: JavaScript Deobfuscation"
date: 2026-08-22 00:00:00 +0700
categories: [HTB SOC Jobpath]
tags: [cdsa, study-notes, htb-soc-jobpath, javascript, deobfuscation, reverse-engineering]
---

# **Obfuscation**

## **Code Obfuscation**

- Obfuscation is a technique to re-write the code in a way that make a script more difficult to read by humans but allows it to function the same from a technical point of view, though performance may be slower.
- A common obfuscation technique involves breaking the code into individual words and assigning numbers to them (creating a dictionary). Then, the words in the code are replaced with these numbers so that others cannot understand it. When executed, the system automatically pieces the numbers back together into a text string containing the original code.
    - **The `eval()` function:** In JavaScript, its job is to take the text string that was just pieced together and turn it into **actual code**, forcing the computer to run it.
    - **Example:** You have the original code: `alert("Hi")`
        - **Step 1: Create a dictionary.** `0 = alert`, `1 = "Hi"`
        - **Step 2: Hide the code.** The encoded string will be: `alert("Hi")` → `0(1)`
        - **Step 3: Reverse the process.** The computer looks up the dictionary and translates `0(1)` back into text: `"alert('Hi')"`
        - **Step 4: Execute.** The command `eval("alert('Hi')")` receives this text, turns it into a real command, and displays the "Hi" dialog box on the screen.

[[https://beautifytools.com/javascript-obfuscator.php](https://beautifytools.com/javascript-obfuscator.php)]

![image.png](/assets/img/cdsa/sec11-js-deobfuscation/image.png)

- Another type of obfuscation is **code minification,** means having the entire code in a single (often very long) line, Usually, minified JavaScript code is saved with the extension `.min.js`

[[https://www.toptal.com/developers/javascript-minifier](https://www.toptal.com/developers/javascript-minifier)]

![image.png](/assets/img/cdsa/sec11-js-deobfuscation/image%201.png)

## **Advanced Obfuscation**

- [[https://obfuscator.io](https://obfuscator.io/)]
- [[https://jsfuck.com/](https://jsfuck.com/)]

![image.png](/assets/img/cdsa/sec11-js-deobfuscation/image%202.png)

![image.png](/assets/img/cdsa/sec11-js-deobfuscation/image%203.png)

- [[https://utf-8.jp/public/jjencode.html](https://utf-8.jp/public/jjencode.html)]
- [[https://utf-8.jp/public/aaencode.html](https://utf-8.jp/public/aaencode.html)]

# **Deobfuscation**

## **Beautify**

![image.png](/assets/img/cdsa/sec11-js-deobfuscation/image%204.png)

## **Deobfuscate**

[[https://matthewfl.com/unPacker.html](https://matthewfl.com/unPacker.html)]

- Some script use method of obfuscation is **packing**. Another way of **unpacking** such code is to find the return value at the end and use **console.log** to print it instead of executing it.

## **Reverse Engineering**

- We would need to manually reverse engineer the code to understand how it was obfuscated and its functionality for harder cases
