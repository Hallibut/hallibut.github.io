---
title: "The Threat Intelligence Piece in the Cybersecurity Puzzle"
date: 2026-08-02 19:00:00 +0700
categories: [Personal Share]
tags: [threat-intel, cyber-defenders]
pin: true
image:
  path: /assets/img/personal-share/how-i-make-my-cyber-adversaries-cry/CTIGA.png
---

![Certified Certificate](/assets/img/personal-share/how-i-make-my-cyber-adversaries-cry/certified_certificate.png)

Trước khi tiếp cận đến **Threat Intelligence**, mình chỉ biết rằng nó là một phần của công việc ứng phó sự cố. Mặc dù mới đầu nghe khá là yếu đuối, gì chứ đã nói tới Defenders thì phải gân guốc giáp lá cà, xanh chín với kẻ thù, đánh đâu chặn đó chứ, ai lại đợi người khác gặp chuyện xong xuôi hết rồi mới đi nên mạng để tìm thông tin bao giờ? Vậy mà đó lại là suy nghĩ sai lầm của mình khi đó, vì sau này mình mới hiểu rằng, các đội ngũ bảo mật đã luôn sử dụng phương pháp này để có thể ngăn ngừa sớm hậu họa xảy đến với hệ thống mà mình đang bảo vệ.

Chân ướt chân ráo tìm hiểu, mình cũng tiếp cận như bao người khác, nhất là ở cái thời đại AI này, mình cứ ném tất cả những gì mình biết được lên Gemini và bắt đầu cầu nguyện là nó sẽ cho mình thông tin gì đó hữu ích. Cách này không hẳn là vô giá trị, cái lợi của nó là NHANH, các mô hình ngôn ngữ lớn có thừa sức để tìm kiếm và tổng hợp thông tin hiệu quả hơn một newbie như mình, vậy nhưng điểm bất lợi khi cố chấp như thế đó là các kết quả mình nhận được sẽ không trọng tâm, mình cũng không thể chắc chắn vào kết quả được đưa ra và tệ hơn cả là tin tặc sẽ ngồi đâu đó và cười vào mặt mình. Chúng ta có thể làm tốt hơn thế này mà!

## 1. **Pyramid of Pain**

Trước tiên mình phải hiểu về từ **“Intelligence”**, Ở đây mang nghĩa là một nguồn tri thức hữu ích về đối thủ, kẻ địch hoặc các tổ chức chính phủ bất chính có nguy cơ ảnh hưởng trực tiếp đến hệ thống thông tin của mình. Nguồn tri thức này sẽ được xác định thông qua **các thông tin** mà mình tổng hợp được từ quá trình điều tra trên chính hệ thống của mình, trên các trang tin tức quan trọng, các báo cáo của chuyên gia, thậm chí là các sự thật hiển nhiên mà mình trước giờ không nghĩ tới. Các thông tin này còn có một tên gọi thân thương hơn đó là các **Indicator**.

*Một dinh thự bên nằm bên bờ sông Seine bị đột nhập ngay trong đêm mưa, hiện trường là một tủ nữ trang mở sẵn, không một vết cạy khoét, trong cả tủ đầy trang sức vậy mà chỉ có mặt dây chuyền khảm ngọc quý giá của vị bá tước là mất tích. Hai thanh tra được cử tới điều tra, người thứ nhất đi hỏi han cả buổi thì gom được thông tin về một chiếc xe mới kéng, một biển số quen và một lời khai về một gã đàn ông mặc áo đen. Người thứ hai chẳng hỏi han ai, chỉ đứng quanh hiện trường vụ án rồi lên gác kiểm tra chốt cửa sổ. Tối đó cả hai đến gặp Holmes và cùng đưa ra kết luận về thân phận thực sự của tên trộm. Chứng cứ của người thứ nhất tan tành hết chỉ sau ba câu hỏi của Holmes, hóa ra chiếc xe đã bán và thậm chí đã sang tên hai lần, biển số thì là của hãng cho thuê, còn áo đen thì cả Paris ai mà chẳng mặc. Trong khi đó, người thanh tra thứ hai nói ngắn gọn hơn nhiều, tại của sổ gác xép, chốt bị đẩy từ ngoài bằng một con dao cậy cửa, vết dao đặc trưng vẫn còn trên thành cửa, tên trộm đi ngang phòng có người ngủ mà không ai trở mình, chỉ lấy đúng thứ hắn vẫn lấy và để lại một tấm thiệp nặc danh với chữ viết tay nắn nót. Chỉ cần có thế, Holmes với tay lấy chiếc mũ sờn với một nụ cười đầy thách thức.*

![Pyramid of Pain](/assets/img/personal-share/how-i-make-my-cyber-adversaries-cry/image.png)

Qua câu chuyện ta có thể thấy, mức độ tin tưởng của các bằng chứng ****là rất quan trọng**.** Hình ảnh mình đang cho bạn thấy đây là **Pyramid of Pain**, một mô hình cực kỳ nổi tiếng. Tất cả các thành phần nằm trong tháp này là các **Indicator** **of Compromise - IoCs** được sắp xếp theo mức độ đáng tin cậy.

- **Hash Values:** mình sẽ giả sử bạn đã biết về [phương pháp hash](https://codelearn.io/sharing/hash-la-gi-va-hash-dung-de-lam-gi?srsltid=AfmBOoolAzME3M0aC7Y-heOZnuD-DgFMDtaywuLu44JXUvEXxBkxZOcb), các mã hash cho đến nay luôn là Indicator có độ chính xác cao nhất vì tính chất của chúng. Vậy nhưng về độ tin cậy thì lại khôngI được như vậy vì chúng cực kỳ dễ bị thay đổi (dù là vô tình hay cố ý). Vì vậy mà mã hash có lẽ là loại Indicator ít hữu ích nhất. (chỉ cần thêm một dấu chấm dấu phẩy là có thể thay đổi toàn bộ mã hash rồi!)
- **IP Addresses:** chỉ có mấy tên n00bs mới đi sử dụng địa chỉ IP của chính mình, có vô vàn cách để che dấu địa chỉ IP (mạng TOR, VPN, Proxy, …).
- **Domain Names:** Để sở hữu một tên miền, thường thì mình sẽ phải đăng ký và trả phí với nhà cung cấp tên miền. Hành vi của các tên miền cũng thường được ghi lại. Đương nhiên kẻ tấn công sẽ có cách để vượt qua vấn đề này dễ dàng, vậy nên để nói về mực độ tin cậy so với địa chỉ IP thì cũng chỉ cỡ đốt ngón tay.
- **Network & Host Artifacts:** Khi thực hiện hành vi bất chính trên thiết bị hay trên mạng của người khác, rất khó để bạn không để lại các dấu vết (Artifacts), mọi thứ gần như luôn được ghi lại. Mặc dù đã có những kỹ thuật anti forensics tinh vi, vậy nhưng các dấu vết này vấn là một loại Indicator đáng để tâm.
- **Tools:** Hầu hết các cuộc tấn công sẽ sử dụng các công cụ có sẵn. Nếu mình liên tục bắt gặp cùng một công cụ, cuối cùng mình sẽ trở nên rất giỏi trong việc phát hiện ra nó. Một khi đã bị chặn, để tiếp tục, chúng buộc phải tìm một công cụ mới, từ đó kéo theo là thời gian phải bỏ ra để thử nghiệm và làm quen lại từ đầu.
- **TTPs: là viết tắt cho Tactics, Techniques & Procedures,** là các chiến lược, kỹ thuật và thủ tục mà kẻ tấn công đã dày công nghiên cứu, ngày đêm không ngủ chỉ nhằm một mục đích là tấn công hệ thống của ta. Nếu có thể phát hiện ra chúng đã học những kỹ thuật nào và sau đó chặn nó, thì việc bắt chúng học lại từ đầu một kỹ thuật mới có lẽ là cực hình đối với chúng. Có khi chúng sẽ bỏ đi kiếm một hệ thống khác mà chúng có thể áp dụng những kỹ thuật đó cho nhanh. Vậy là ta thắng!

Tất nhiên các bằng chứng nằm trên các tầng đỉnh của kim tự tháp không dễ gì nắm bắt, vậy nhưng một khi đã nắm bắt được thì hệ thống của ta là bất khả xâm phạm.

## 2. Diamond Model of Intrusion Analysis

Trong quá trình nghiên cứu và tìm kiếm các **Indicator**, không ít thì nhiều mình cũng phát rồ vì quá nhiều thông tin nhiễu và không có hệ thống. Một bài viết lại đẻ ra 3-4 bài viết khác, rồi 3-4 bài viết lại đẻ ra 5-6 trang blog, 7-8 bài research, 9-10 bài post trên Facebook hay X này nọ. Tất cả đều phải đi qua bộ lọc trực giác nghèo nàn của mình. Vậy thì câu hỏi đặt ra là làm thế nào để có thể hệ thống các thông thông tin kia thành một cái khung để giúp mình nhìn vào và đưa ra được các phương hướng tìm kiếm tiếp theo.

Trong quá trình đào sâu và tìm hiểu, mình có đọc qua [bài báo](https://www.researchgate.net/publication/379381999_The_Diamond_Model_of_Intrusion_Analysis) của 3 sư phụ có tên Sergio Caltagirone, Andrew Pendergast, và Christopher Betz. Bài báo có tên "The Diamond Model of Intrusion Analysis". Thực ra bài đó cũng có từ khá lâu rồi, vậy nhưng mô hình này không hề lỗi thời, mình có thể sử dụng nó để bước đầu tiếp cận.

![Diamond Model](/assets/img/personal-share/how-i-make-my-cyber-adversaries-cry/image-1.png)

Bất kỳ một **Sự kiện** nào nằm trong chuỗi tấn công cũng luôn xoay quanh 4 yếu tố cơ bản, tạo thành 4 góc của một hình kim cương (hoặc hình thoi nếu bạn OCD):

- **Adversary (Đối thủ):** Kẻ đứng sau cuộc tấn công là ai? (Ví dụ: Một nhóm APT, một hacker nghiệp dư).
- **Victim (Nạn nhân):** Ai hoặc hệ thống nào đang bị tấn công? (Ví dụ: Máy chủ Web của công ty, hoặc máy tính của nhân viên kế toán).
- **Capability (Kỹ năng/Vũ khí):** Kẻ tấn công sử dụng công cụ hoặc mánh khóe gì? (Ví dụ: Mã độc Ransomware, lỗ hổng SQL Injection, phần mềm keylogger).
- **Infrastructure (Hạ tầng):** Kẻ tấn công dùng phương tiện/hệ thống mạng nào để tấn công? (Ví dụ: Một địa chỉ IP độc hại, một tên miền giả mạo, hoặc một máy chủ Command & Control).

Ví dụ, khi nhận được thông tìn về một chiếc máy tính trong mạng công ty vừa tải về một tệp tin lạ. Mình sẽ chỉ biết 2 góc của sơ đồ kim cương. Đó là **Victim** (máy tính công ty) và **Infrastructure** (có thể là địa chỉ IP hoặc một tên miền lạ nơi ông nhân viên tải file lạ về).

Việc **Pivoting** (di chuyển) qua các đỉnh còn lại chính là công việc điều tra của mình. Từ địa chỉ IP đó, mình sẽ lùng sục để tìm ra **Capability** (tệp tin đó chứa mã độc gì?), rồi từ mã độc đó mình sẽ đối chiếu với các nguồn tình báo để suy ra **Adversary** (nhóm hacker nào hay dùng loại mã độc này?).

Khi tìm đủ 4 góc, mình sẽ có được một **Diamond Event** (Sự kiện kim cương), như game Free Fire luôn.

Ngoài ra trong sơ đồ còn có các **Meta-features**, đơn giản là các thông tin mình sẽ ghi chú thêm vào báo cáo sự cố:

- **Thời gian (Timestamp):** Vụ tấn công bắt đầu và kết thúc lúc mấy giờ? (Để xem hacker hay hoạt động ban ngày hay ban đêm).
- **Giai đoạn (Phase):** Hacker đang ở bước nào rồi? Mới đang đi trinh sát, hay đã chui được vào hệ thống và đang khai thác, hay đang tuồn dữ liệu ra ngoài rồi?
- **Kết quả (Result):** Vụ hack thành công hay thất bại? Dữ liệu đã bị mất chưa hay hệ thống bảo mật của bạn đã chặn được rồi?
- **Hướng (Direction):** Luồng dữ liệu đi từ đâu đến đâu?
- **Phương pháp (Methodology):** Gọi tên chiêu trò của hacker là gì? (Tấn công Phishing, chạy một file Loader, tiêm mã vào tiến trình hay tấn công DDoS).
- **Tài nguyên (Resources):** Hacker cần những công cụ hay chiêu trò gì để thực hiện vụ này? (Ví dụ: Cần tiền mua tên miền giả mạo, cần tool mã độc tải trên mạng về...).

Mô hinh kim cương cũng có một bản cải tiến để thể hiện mọi thứ rõ ràng hơn, gọi là “mô hình kim cương mở rộng”. mô hình này bổ sung thêm 2 thứ đó là:

- **Trục dọc (Nối Đối thủ và Nạn nhân):** Trục này thể hiện cho các đặc điểm về **Social-Political** (Chính trị - Xã hội). Sẽ luôn tồn tại mối quan hệ nào đó giữa nạn nhân và kẻ tấn công, có thể là đối thủ kinh doanh, trả đũa, sĩ diện hay chỉ đơn giản là cần botnet. Kẻ tấn công thì chia thành 2 loại:
    - **Smash and grab:** Đây là những kẻ tấn công mang tính cơ hội. Chúng vơ vét được gì thì vơ, làm thật nhanh và không hề quan tâm đến việc có bị mất quyền truy cập vào hệ thống của bạn hay không.
    - **Persistent:** Những kẻ này bám riết lấy mục tiêu bằng mọi giá. Kể cả khi bạn phát hiện ra và áp dụng các biện pháp phòng thủ mạnh tay, chúng vẫn sẽ tìm cách khác để đục tường chui vào bằng được.

![Extended Diamond Model 1](/assets/img/personal-share/how-i-make-my-cyber-adversaries-cry/image-2.png)

- **Trục ngang (Nối Năng lực/Vũ khí và Hạ tầng):** Trục này thể hiện cho các đặc điểm về **Technology** (Công nghệ). Trục này thể hiện cách thức file mã độc và hạ tầng của kẻ tấn công kết nối với nhau ra sao. Có những lúc hacker thay đổi toàn bộ vũ khí mới, đổi luôn cả hạ tầng, khiến mình mất dấu hoàn toàn. Nhưng có những thói quen công nghệ của chúng lại rất khó đổi, có thể là chúng vẫn quen dùng bồ câu để truyền dữ liệu chẳng hạn.

Ở phần trước mình đã giới thiệu cho các bạn về **Indicator** rồi đúng không? Các Indicator trong phần trước bản chất của chúng chỉ giới hạn ở các chi tiết kỹ thuật (hash hungr rồi địa chỉ IP các thứ), vậy nhưng trong bài báo của 3 sư phụ đây, họ đã đề xuất mở rộng khái niệm về Indicators, gọi chúng là **Contextual Indicators** (các Indicator theo ngữ cảnh). **Contextual Indicators** bản chất vẫn là các Indicator như mình đã nói ở phần trước thôi, nhưng lần này chúng không chỉ đứng độc lập mà sẽ được gắn liền với bức tranh toàn cảnh về chiến dịch của kẻ tấn công (như động cơ của chúng là gì, chúng nhắm vào nhóm nạn nhân nào, loại dữ liệu chúng muốn đánh cắp là gì). Điều này sẽ giúp mình không chỉ đơn thuần là chặn một mối đe dọa trước mắt, mà còn hiểu rõ bản chất kẻ thù để vạch ra chiến lược phòng thủ lâu dài và dự báo các cuộc tấn công trong tương lai nữa.

OK, lại qua lại lúc nãy, mình cũng có nhắc tới **Pivoting** đúng không? Đây là quá trình ghép nối các **Indicator** lại với nhau để ra được một **Diamond Event**. Khi có một vụ xâm nhập xảy ra, mình cũng không cần phải có đủ tất cả các Indicator mới bắt đầu làm việc được. Tùy vào việc đang nắm trong tay phần nào của mô hình kim cương, mình sẽ chọn 1 trong 6 cách sau để bắt đầu Pivot tới những cái còn lại:

- **Cách 1: Lấy Victim làm trung tâm**
Mình không đi tìm hacker, mà sẽ tạo ra một cái bẫy. Bạn dựng lên một máy chủ chứa đầy dữ liệu giả, hớ hênh (Honeypot) rồi ngồi rình. Hacker tưởng mồi ngon sẽ nhảy vào cắn, và thế là chúng tự phơi bày **Capability** và **Infrastructure** cho mình xem.
- **Cách 2: Lấy Capability làm trung tâm**
Mình vô tình bắt được một mẫu mã độc. Đem nó vào phòng lab, dịch ngược mã nguồn để xem nó hoạt động thế nào, xài thuật toán mã hóa gì, và nó báo cáo về cho ai.
- **Cách 3: Lấy Infrastructure làm trung tâm**
Mình phát hiện một địa chỉ IP hoặc một Tên miền có dấu hiệu lừa đảo. Tra cứu thông tin đăng ký của tên miền đó. Từ một tên miền, mình có thể truy ra cả một danh sách hàng chục tên miền khác do cùng một kẻ mua.
- **Cách 4: Lấy Adversary làm trung tâm**
Cách này xịn nhất nhưng khó nhất. Mình biết gã hacker là ai, và mình sẽ theo dõi trực tiếp nhất cử nhất động của hắn (nghe lén điện thoại, theo dõi máy tính, theo dõi hoạt động của hắn trên darkweb). Hắn chế tạo Vũ khí gì, mua Hạ tầng nào mình đều biết.
- **Cách 5: Lấy Social-Political làm trung tâm**
Mình chẳng có manh mối kỹ thuật nào cả. Nhưng đọc lướt facebook thấy CocaCola và Pepsi đang kiện cáo tranh chấp gì đó cực kỳ gay gắt. Mình là nhân viên bảo mật của CocaCola, mình đánh hơi thấy nguy hiểm và lập tức tăng cường phòng thủ, vì kiểu gì đối thủ cũng thuê người hack hệ thống của mình để trộm tài liệu.
- **Cách 6: Lấy Technology làm trung tâm**
Mình không cần biết ai hack ai, mình chỉ là thằng giám sát quèn làm nhiệm vụ hằng ngày. Tự nhiên hôm nay bạn thấy gói tin DNS to bất thường, nhồi nhét đầy dữ liệu mã hóa. Nhờ vậy, mình phát hiện ra một cuộc tấn công mới toanh mà trước đó chưa ai biết.

Một khi thành thục, mình sẽ có trong tay các **Diamond Events**, từ đây mình có thể xây dựng lại được luồng tấn công của kẻ thù dựa trên các Framework nổi tiếng như **Cyber-Kill Chain** hay **Mitre Att&ck**.

![Extended Diamond Model 2](/assets/img/personal-share/how-i-make-my-cyber-adversaries-cry/image-3.png)

## 3. Threat Intelligence Sharing

Coming soon…
