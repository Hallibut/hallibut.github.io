import re

with open('2026-06-08-soc-htb-sec6-windows-attacks-defense.md', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "Trước tiên mình cần thực hiện Kerberoasting trên AD Domain này": "First, I need to perform Kerberoasting on this AD Domain",
    "Chuyển nội dung này sang Kali, mình sử dụng Hash Cat để giải mã.": "Transferring this content to Kali, I used Hashcat to crack the hash.",
    "Đề bài muốn mình perform a AS-REP Roasting với Rubeus": "The task requires me to perform AS-REP Roasting with Rubeus",
    "Truy cập vào Event Viewer": "Accessing Event Viewer",
    "- Thư mục này chứa hai thành phần đặc biệt quan trọng để quản trị hệ thống mạng:": "- This folder contains two critical components for network administration:",
    "Phải có hệ thống tự động giám sát liên tục.": "There must be an automated continuous monitoring system.",
    "Mở toang quyền truy cập thư mục tạm thời để chuyển file cho nhanh nhưng sau đó lại quên khóa lại.": "Opening up folder access temporarily to quickly transfer files but then forgetting to lock it down again.",
    "- Search for the NetBIOS name of the domain bởi vì attacker thường sẽ dùng cái này để search mật khẩu.": "- Search for the NetBIOS name of the domain because attackers often use this to search for passwords.",
    "there are two files: **connect.ps1** và **connect2.ps1**. Using the cat command to view their contents, I found the password for the **Administrator2**": "there are two files: **connect.ps1** and **connect2.ps1**. Using the cat command to view their contents, I found the password for the **Administrator2**",
    "Để đăng nhập bằng tài khoản này vào DC01, mình dùng Remote Desktop Connection": "To log in with this account into DC01, I used Remote Desktop Connection",
    "Truy cập vào thư mục để sử dụng **mimikatz.exe**": "Navigate to the folder to use **mimikatz.exe**",
    "Truy cập Event ID 4622 **(An operation was performed on an object)**, để xem hành vi truy cập mới nhất vào DC": "Access Event ID 4622 **(An operation was performed on an object)** to see the latest access behavior to the DC",
    "**Dấu hiệu Tấn công cốt lõi:**": "**Core Attack Indicators:**",
    "- **AccessMask:** `0x100` tương ứng với quyền *Control Access*.": "- **AccessMask:** `0x100` corresponding to *Control Access* permission.",
    "- **Properties:** Chứa GUID `{1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}`. Chi tiết đại diện cho quyền **DS-Replication-Get-Changes-All**.": "- **Properties:** Contains GUID `{1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}`, which represents the **DS-Replication-Get-Changes-All** permission.",
    "To create a ticket, I need the hash of **krbtgt** và **SID** of the entire domain. First, retrieve the hash of the **krbtgt** using the DCSync technique**:**": "To create a ticket, I need the hash of **krbtgt** and the **SID** of the entire domain. First, retrieve the hash of the **krbtgt** using the DCSync technique**:**",
    "Truy cập vào thư mục để sử dụng mimikatz.exe": "Navigate to the folder to use mimikatz.exe",
    "We got fully access now, mặc dù chỉ hỏi phần mã hash nhưng t đã tìm full luôn rồi, kkk": "We got full access now, even though it only asked for the hash, I went ahead and found everything, lol"
}

for vi, en in replacements.items():
    content = content.replace(vi, en)

with open('2026-06-08-soc-htb-sec6-windows-attacks-defense.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Remaining translations complete.")
