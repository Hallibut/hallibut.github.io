import re

with open('2026-06-08-soc-htb-sec6-windows-attacks-defense.md', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "Mình được cung cấp 2 máy, 1 là máy của người dùng Bob có vẻ đã nằm sẵn trong active directory và máy còn lại là Kali Linux, mình sẽ sử dụng để crack mật khẩu offline": "I was provided with 2 machines, one belonging to the user Bob which appears to already be in the active directory, and the other is Kali Linux, which I will use to crack passwords offline",
    "Trên Kali tạo một file txt và paste đoạn hash vừa rồi vào. Chạy câu lệnh hashcat sau sử dụng từ điển rockyou,txt, một từ điển nổi tiếng chuyên phá các mật khẩu yếu. (bạn có thể tìm thấy nó ở /usr/share/wordlists/rockyou.txt.gz trong máy kali)": "On Kali, create a txt file and paste the hash. Run the following hashcat command using the rockyou.txt wordlist, a famous dictionary specialized for cracking weak passwords. (you can find it at /usr/share/wordlists/rockyou.txt.gz in Kali)",
    "được tự động tạo ra trên tất cả các **DC** trong hệ thống mạng AD của Windows Server.": "automatically created on all **DCs** in a Windows Server AD network.",
    "Chứa các file cấu hình chính sách, bao gồm các template, file registry (registry.pol), và các file cấu hình bảo mật được dùng để áp đặt quy định xuống các máy trạm và tài khoản người dùng.": "Contains policy configuration files, including templates, registry files (registry.pol), and security configuration files used to enforce rules on workstations and user accounts.",
    "Chứa các tập lệnh (batch, PowerShell...) chạy tự động khi máy tính khởi động, tắt máy, hoặc khi người dùng đăng nhập/đăng xuất.": "Contains scripts (batch, PowerShell...) that run automatically when the computer starts up, shuts down, or when a user logs in/out.",
    "- Vị trí và cơ chế": "- Location and mechanism",
    "Được cài đặt ở đường dẫn": "Installed at the path",
    "Được hệ thống chia sẻ ra mạng nội bộ với đường dẫn": "Shared by the system to the internal network via the path",
    "để các máy client có thể truy cập và tải policy về.": "so client machines can access and download policies.",
    "Để đảm bảo mọi DC đều áp dụng chung một tập hợp chính sách giống nhau, Windows Server sử dụng dịch vụ": "To ensure all DCs apply the same set of policies, Windows Server uses the",
    "để liên tục đồng bộ các thay đổi trong SYSVOL. *(Lưu ý: Ở các phiên bản Windows Server cũ từ 2003 trở về trước, cơ chế này được đảm nhiệm bởi dịch vụ FRS - File Replication Service)*.": "service to continuously synchronize changes in SYSVOL. *(Note: In older Windows Server versions from 2003 and earlier, this mechanism was handled by the FRS - File Replication Service)*.",
    "- Điểm quan trong của hình thứ tấn công này:": "- Key point of this attack:",
    "một tập hợp các extensions của Group Policy": "a collection of Group Policy extensions",
    "Microsoft mã hóa mật khẩu của tài khoản có quyền Administrator và lưu trong SYSVOL nhưng lại dùng chung": "Microsoft encrypted the password of the Administrator account and stored it in SYSVOL, but they used",
    "cho tất cả các hệ thống trên thế giới.": "across all systems worldwide.",
    "Sai lầm chí mạng hơn nữa là họ đã": "The fatal mistake was that they",
    "chìa khóa này lên mạng, cho phép bất kỳ ai cũng có thể copy về để tự giải mã và chiếm toàn quyền hệ thống.": "this key on the internet, allowing anyone to copy it, decrypt the password themselves, and gain full system control.",
    "sử dụng Dummy File chứa cấu hình giả mạo và không gắn nó với bất kỳ chính sách thực tế nào. Máy tính bình thường sẽ không bao giờ đụng đến nó. Nếu hệ thống ghi nhận có một tài khoản đang cố tình mở và đọc file này, đó gần như chắc chắn là hành vi của hacker.": "use a Dummy File containing a fake configuration and don't link it to any actual policy. A normal computer will never touch it. If the system logs that an account is intentionally trying to open and read this file, it is almost certainly a hacker's behavior.",
    "tốt nhất là": "ideally a",
    "sau đó lưu mật khẩu (wrong password) của tài khoản này vào file XML trong thư mục SYSVOL.": "then save the password (wrong password) of this account into an XML file in the SYSVOL directory.",
    "Các tài khoản dịch vụ thường rất hiếm khi bị đổi mật khẩu. Hayx thiết lập sao cho thời gian đổi mật khẩu cuối cùng của tài khoản này cũ hơn ngày tạo file XML.": "Service accounts rarely have their passwords changed. Set it up so the last password change time for this account is older than the creation date of the XML file.",
    "Cài đặt một dummy task thỉnh thoảng dùng tài khoản này để đăng nhập.": "Setup a dummy task to occasionally log in using this account.",
    "File bị đọc là Groups.xml và Access Mask": "The file being read is Groups.xml and Access Mask",
    "Chỉ link GPO mồi nhử với các máy chủ": "Only link the honeypot GPO to",
    "Tự động gỡ unlink GPO mồi nhử và disable user responsible for modified it immediate nếu phát hiện nó bị sửa đổi.": "Automatically unlink the honeypot GPO and immediately disable the user responsible for modifying it if tampering is detected.",
    "Đặt tên thư mục có đuôi $ để làm ẩn trên Windows, nhưng các phần mềm dò quét của hacker vẫn nhìn thấy rõ mồn một.": "Append $ to the folder name to hide it on Windows, but hacker scanning tools will still clearly see it.",
    "Di chuyển vào thư mục này bằng lệnh cd, mình đã thử tìm": "Navigating to this directory using cd, I tried searching for",
    "các file có chứa": "files containing the",
    "có hai file": "there are two files:",
    "dùng lệnh cat để Dxem nội dung 2 file, mình đã tìm thấy mật khẩu cho người dùng": "Using the cat command to view their contents, I found the password for the",
    "Mình đã viết lại đoạn script để có thể hiểu nó rõ hơn": "I rewrote the script to understand it better",
    "Sau đó mình chạy file này để dò các Object.": "Then I ran this file to scan for Objects.",
    "Kết quả là không thể dùng để đăng nhập được": "The result is that it cannot be used to log in",
    "Có thể thấy có 1 người dùng thông thường (chính là Rocky) đã truy cập thẳng vào root object của Domain": "You can see there is 1 regular user (which is Rocky) who directly accessed the root object of the Domain",
    "Tìm kiếm hành vi bất thường khi một tài khoản xin cấp vé truy cập dịch vụ cụ thể (TGS) mà bỏ qua bước bắt buộc là phải lấy vé xác thực danh tính tổng thể (TGT) trước đó.": "Look for anomalous behavior where an account requests a specific service access ticket (TGS) while skipping the mandatory step of obtaining an overall identity verification ticket (TGT) first.",
    "Để tạo một vé, mình cần hash của": "To create a ticket, I need the hash of",
    "Đầu tiên là lấy mã hash của tài khoản": "First, retrieve the hash of the",
    "sử dụng kỹ thuật DCSync**:**": "using the DCSync technique**:**",
    "Dump hash credential của người dùng krbtgt": "Dump the hash credential of the krbtgt user",
    "**đăng công khai**": "**publicly published**",
    "**một chìa khóa giải mã duy nhất**": "**a single static decryption key**",
    "**không quan trọng**": "**non-critical**"
}

for vi, en in replacements.items():
    content = content.replace(vi, en)

css_block = """
<style>
  img {
    max-width: 700px !important;
    height: auto;
    display: block;
    margin: 2rem auto;
    border-radius: 8px;
  }
</style>
"""

# Insert CSS block after frontmatter
content = re.sub(r'(---.*?---)', r'\1\n' + css_block, content, flags=re.DOTALL)

with open('2026-06-08-soc-htb-sec6-windows-attacks-defense.md', 'w', encoding='utf-8') as f:
    f.write(content)

