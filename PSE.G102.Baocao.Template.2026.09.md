##  **CHÚ Ý:**

1. Mỗi nhóm  soạn thảo báo cáo trực tiếp vào tệp văn bản (docx, edit online bằng Google Docs) theo cấu trúc dưới đây, đặt trong thư mục online của nhóm và đó.   
2. Quy tắc trình bày quyển báo cáo phải tuân thủ Quy định của khoa/trường  
3. Báo cáo môn này được phép in 2 mặt (do số trang rất nhiều)  
4. **Yêu cầu về Bài toán**  
* Đa người dùng.  
* Đa thiết bị/phương tiện (máy tính, điện thoại, máy in...).  
* Có nghiệp vụ (yêu cầu, quy trình, mẫu biểu) thực tế.  
* Sử dụng UML để mô hình hoá các kết quả khảo sát, phân tích, thiết kế  
* Sử dụng Git (hoặc công cụ tương đương khác) để quản lý mã nguồn của dự án  
5. Mọi nhận định trong báo cáo này phải được chứng minh hoặc dẫn nguồn nếu trích từ tài liệu khác (tài liệu đó phải được liệt kê trong phần TÀI LIỆU THAM KHẢO)  
6. Mọi bảng biểu (Table) phải được thiết lập để tiêu đề in lặp lại ở trang thứ 2 trở đi (nếu bảng trải dài nhiều trang)  
7. Tài liệu tham khảo được chấp nhận gồm:  
   1. Sách về CNPM   
   2. Bài báo khoa học về CNPM  
   3. Các chuẩn đã được công bố về CNPM  
8. Mẫu báo cáo này được cập nhật lần cuối ngày 10/09/2026

| HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG KHOA VIỄN THÔNG 1 \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  BÁO CÁO  MÔN: CÔNG NGHỆ PHẦN MỀM   ĐỀ TÀI: PHÁT TRIỂN PHẦN MỀM QUẢN LÝ HOẠT ĐỘNG BẢO HÀNH CỦA TRUNG TÂM HỖ TRỢ KỸ THUẬT TẠI CÔNG TY MÁY TÍNH HƯNG THIỆN THEO CÔNG NGHỆ PHẦN MỀM  Nhóm thực hiện:  PSE.G102   Giảng viên hướng dẫn:                                                     	 Hà Nội 10/2026 |
| ----- |

## **LỜI NÓI ĐẦU**

...

## **MỤC LỤC**

...

## 

## **CÁC DANH MỤC**

...

## 

## **CHƯƠNG 1\. GIỚI THIỆU**

1. ### **Giới thiệu bài toán**

	Trong bối cảnh công nghệ thông tin và các thiết bị điện tử phát triển mạnh mẽ, nhu cầu sử dụng dịch vụ bảo hành và hỗ trợ kỹ thuật của người dùng ngày càng gia tăng. Đối với các doanh nghiệp phân phối và bán lẻ, trung tâm bảo hành không chỉ là nơi khắc phục sự cố mà còn là điểm chạm quan trọng để duy trì uy tín thương hiệu và giữ chân khách hàng. Tuy nhiên, khi quy mô tiếp nhận ngày một lớn, mô hình quản lý truyền thống tại nhiều trung tâm đang dần bộc lộ những hạn chế trong việc theo dõi tiến độ và điều phối công việc sửa chữa. Hệ quả là hiệu suất vận hành tổng thể bị suy giảm, gây khó khăn cho công tác quản lý và ảnh hưởng đến chất lượng dịch vụ khách hàng.

	Đi sâu vào quá trình vận hành thực tế, vấn đề đầu tiên nằm ở việc thiếu một cái nhìn tổng quan về tình trạng sửa chữa của các thiết bị. Mỗi ngày, trung tâm phải tiếp nhận và xử lý nhiều thiết bị với các loại sự cố, mức độ phức tạp và tiến độ sửa chữa khác nhau. Các thiết bị được phân bổ cho nhiều kỹ thuật viên, khiến thông tin về tình trạng xử lý nằm rải rác ở từng bộ phận hoặc cá nhân phụ trách. Trong khi đó, người quản lý chưa có một công cụ tập trung để theo dõi toàn bộ danh sách thiết bị đang sửa chữa, xác định những thiết bị sắp đến hạn bàn giao hoặc nhận biết kịp thời các trường hợp có nguy cơ chậm tiến độ. Việc thiếu thông tin tổng hợp khiến công tác giám sát và điều phối trở nên bị động, đặc biệt khi số lượng thiết bị cần xử lý tăng cao.

	Vấn đề thứ hai liên quan trực tiếp đến phương thức kiểm tra và cập nhật tiến độ sửa chữa. Khi cần xác định tình trạng của một thiết bị, người quản lý thường phải tra cứu thông tin từ các nguồn ghi chép riêng lẻ hoặc liên hệ trực tiếp với kỹ thuật viên đang phụ trách. Quá trình này không chỉ tiêu tốn thời gian, công sức mà còn dễ dẫn đến tình trạng bỏ sót thông tin khi số lượng yêu cầu bảo hành tăng lên. Đặc biệt, trong những trường hợp khách hàng liên hệ để hỏi về tiến độ hoặc thời gian dự kiến nhận lại thiết bị, nhân viên tiếp nhận có thể không nắm được tình trạng sửa chữa mới nhất và phải mất thêm thời gian xác minh. Sự thiếu đồng bộ trong việc cập nhật thông tin khiến quá trình phản hồi khách hàng bị chậm trễ, đồng thời làm giảm hiệu quả phối hợp giữa các bộ phận trong trung tâm.

	Vấn đề thứ ba phát sinh trong quá trình bàn giao công việc giữa các kỹ thuật viên. Trên thực tế, việc sửa chữa một thiết bị không phải lúc nào cũng được hoàn thành bởi một kỹ thuật viên trong một ca làm việc. Một thiết bị có thể được kỹ thuật viên đầu tiên tiến hành kiểm tra, xác định nguyên nhân và thực hiện một phần công việc sửa chữa, sau đó được chuyển giao cho kỹ thuật viên khác tiếp tục xử lý vào ngày hôm sau. Tuy nhiên, nếu quá trình sửa chữa không được ghi nhận đầy đủ và thống nhất, kỹ thuật viên tiếp nhận sẽ gặp khó khăn trong việc xác định những thao tác đã thực hiện, kết quả kiểm tra trước đó cũng như các công việc còn tồn đọng. Điều này có thể dẫn đến việc phải kiểm tra lại từ đầu, thực hiện trùng lặp thao tác hoặc bỏ sót những vấn đề chưa được khắc phục. Bên cạnh việc kéo dài thời gian sửa chữa, sự thiếu minh bạch trong lịch sử xử lý còn gây khó khăn cho người quản lý khi theo dõi quá trình thực hiện và xác định trách nhiệm của từng kỹ thuật viên.

	Tổng hợp lại những bất cập trên, bài toán đặt ra là cần xây dựng một hệ thống phần mềm quản lý trung tâm bảo hành và hỗ trợ kỹ thuật có khả năng theo dõi tập trung tình trạng thiết bị và tiến độ sửa chữa. Dự án này được thực hiện nhằm mục tiêu cung cấp cho người quản lý cái nhìn tổng quan về toàn bộ thiết bị đang được xử lý, hỗ trợ theo dõi thời hạn hoàn thành, cập nhật tiến độ theo từng giai đoạn và ghi nhận lịch sử sửa chữa của từng kỹ thuật viên. Đồng thời, hệ thống cần hỗ trợ việc bàn giao công việc giữa các kỹ thuật viên một cách rõ ràng, bảo đảm thông tin được kế thừa xuyên suốt quá trình xử lý thiết bị. Việc xây dựng hệ thống sẽ góp phần giảm thiểu các thao tác kiểm tra thủ công, hạn chế tình trạng bỏ sót công việc, nâng cao hiệu quả điều phối nhân sự và cải thiện chất lượng dịch vụ bảo hành.

2. ### **Mục tiêu của đề tài**

	Mục tiêu tổng quát của dự án là nghiên cứu và phát triển một hệ thống phần mềm quản lý trung tâm bảo hành và hỗ trợ kỹ thuật nhằm số hóa các nghiệp vụ cốt lõi, khắc phục những hạn chế trong việc theo dõi tiến độ và điều phối công việc sửa chữa. Trọng tâm của hệ thống là xây dựng một nền tảng quản lý tập trung, cho phép lưu trữ và cập nhật thông tin thiết bị, tình trạng xử lý và thời hạn hoàn thành của từng yêu cầu bảo hành. Thông qua việc cung cấp cái nhìn tổng quan về toàn bộ thiết bị đang được sửa chữa, hệ thống giúp người quản lý nắm bắt kịp thời khối lượng công việc, xác định những thiết bị sắp đến hạn bàn giao hoặc có nguy cơ chậm tiến độ, từ đó chủ động hơn trong công tác giám sát và điều phối nhân sự.

	Bên cạnh việc nâng cao khả năng giám sát, dự án hướng tới mục tiêu giảm thiểu thời gian và công sức dành cho các thao tác kiểm tra tiến độ thủ công. Hệ thống cho phép kỹ thuật viên trực tiếp cập nhật trạng thái sửa chữa, kết quả kiểm tra và các công việc đã thực hiện trong quá trình xử lý thiết bị. Những thông tin này được lưu trữ tập trung và đồng bộ, giúp nhân viên tiếp nhận cũng như người quản lý có thể nhanh chóng tra cứu tình trạng mới nhất của từng thiết bị mà không cần liên hệ trực tiếp với kỹ thuật viên phụ trách. Qua đó, hệ thống góp phần hạn chế tình trạng bỏ sót thông tin, nâng cao hiệu quả phối hợp giữa các bộ phận và rút ngắn thời gian phản hồi khi khách hàng có nhu cầu tìm hiểu về tiến độ bảo hành.

	Một mục tiêu quan trọng khác của dự án là hỗ trợ quản lý quá trình sửa chữa liên tục trong những trường hợp một thiết bị được xử lý bởi nhiều kỹ thuật viên ở các thời điểm khác nhau. Hệ thống sẽ cung cấp chức năng ghi nhận nhật ký sửa chữa, lưu trữ lịch sử thao tác, kết quả kiểm tra và những công việc chưa hoàn thành của từng kỹ thuật viên. Khi phát sinh nhu cầu chuyển giao thiết bị, kỹ thuật viên tiếp nhận có thể kế thừa đầy đủ thông tin từ người phụ trách trước đó để tiếp tục quá trình sửa chữa mà không phải thực hiện lại những thao tác không cần thiết. Đồng thời, việc lưu trữ lịch sử xử lý theo từng cá nhân giúp người quản lý theo dõi quá trình thực hiện công việc, xác định trách nhiệm của các kỹ thuật viên và hạn chế những sai sót phát sinh trong quá trình bàn giao.

	Tổng thể, dự án hướng tới xây dựng một hệ thống quản lý có khả năng hỗ trợ xuyên suốt quá trình tiếp nhận, theo dõi, sửa chữa và hoàn tất yêu cầu bảo hành. Thông qua việc tập trung hóa dữ liệu, chuẩn hóa quy trình cập nhật tiến độ và quản lý lịch sử bàn giao công việc, hệ thống được kỳ vọng sẽ giảm bớt các thao tác quản lý thủ công, nâng cao hiệu quả sử dụng nguồn lực kỹ thuật và cải thiện chất lượng phục vụ khách hàng. Đây cũng là cơ sở để trung tâm từng bước hoàn thiện quy trình vận hành và mở rộng các chức năng quản lý trong tương lai.

3. ### **Các đề tài/hệ thống liên quan** 

	Trên thị trường hiện nay, việc quản lý bảo hành và hỗ trợ kỹ thuật thường được tích hợp như một phân hệ chức năng bên trong các hệ thống quản trị nguồn lực doanh nghiệp hoặc phần mềm quản trị quan hệ khách hàng quy mô lớn. Tiêu biểu có thể kể đến các giải pháp phần mềm thương mại toàn cầu như nền tảng quản trị Odoo hay hệ thống Salesforce. Ưu điểm của những hệ thống này là khả năng lưu trữ dữ liệu khổng lồ, tính bảo mật cao và tích hợp sẵn nhiều công cụ phân tích dữ liệu đa chiều. Tuy nhiên, nhược điểm cốt lõi là chi phí triển khai và duy trì bản quyền vô cùng đắt đỏ, đòi hỏi cấu hình máy chủ mạnh mẽ và thời gian chuyển giao công nghệ kéo dài. Đối với các trung tâm hỗ trợ kỹ thuật tầm trung, việc áp dụng các hệ thống đồ sộ này thường dẫn đến tình trạng lãng phí tài nguyên hệ thống do có quá nhiều tính năng dư thừa không được sử dụng trong luồng nghiệp vụ thực tế.

	Bên cạnh các phần mềm thương mại đa chức năng, một số tập đoàn bán lẻ lớn tại Việt Nam đã đầu tư ngân sách để tự xây dựng các hệ thống quản lý dịch vụ hậu mãi nội bộ chuyên biệt. Điển hình như hệ thống điều phối dịch vụ kỹ thuật Tận Tâm của Thế Giới Di Động hay cổng thông tin bảo hành Dcare của hệ thống Digiworld. Các nền tảng này giải quyết rất xuất sắc bài toán vận hành đặc thù của chính doanh nghiệp chủ quản, từ việc theo dõi luồng trung chuyển thiết bị qua lại giữa các đại lý đến trạm bảo hành trung tâm, cho đến việc quản lý xuất nhập kho linh kiện nội bộ theo thời gian thực. Mặc dù sở hữu quy trình vận hành tối ưu và tính tự động hóa cao, đây lại là các giải pháp công nghệ đóng và mang tính độc quyền. Các trung tâm sửa chữa và hỗ trợ kỹ thuật độc lập bên ngoài hoàn toàn không có khả năng tiếp cận, thuê lại máy chủ hay mua bản quyền để áp dụng cho mô hình kinh doanh của riêng họ.

	Ngược lại với các tập đoàn lớn, ở phân khúc các cửa hàng sửa chữa và trung tâm hỗ trợ kỹ thuật quy mô nhỏ, phương thức phổ biến nhất hiện nay vẫn là sử dụng phần mềm bảng tính đơn giản hoặc biên nhận giấy thủ công. Phương thức quản lý truyền thống này có lợi thế lớn về mặt chi phí đầu tư ban đầu và nhân viên có thể sử dụng ngay lập tức mà không cần qua đào tạo. Đổi lại, rủi ro phân mảnh dữ liệu và sai sót nhập liệu là rất lớn. Quan trọng hơn, phương thức thủ công hoàn toàn không có khả năng cung cấp một cổng thông tin trực tuyến minh bạch để khách hàng tự tra cứu tiến độ, dẫn đến việc liên lạc bị gián đoạn và làm suy giảm chất lượng dịch vụ.

Từ việc phân tích ưu điểm và nhược điểm của các giải pháp hiện có, nhóm phát triển nhận thấy một khoảng trống lớn về mặt công nghệ đối với các trung tâm bảo hành tầm trung. Việc nghiên cứu và xây dựng một hệ thống phần mềm quản lý bảo hành độc lập, lược bỏ các module dư thừa để tập trung tối ưu hóa các nghiệp vụ cốt lõi như quản lý phiếu tiếp nhận, kiểm soát vật tư và tích hợp cổng tra cứu trực tuyến là một hướng đi hoàn toàn cấp thiết. Giải pháp này không chỉ khắc phục được nhược điểm chi phí cao của các phần mềm doanh nghiệp lớn mà còn giải quyết triệt để sự yếu kém trong khâu quản lý thủ công hiện tại.

4. ### Phương pháp phát triển

Trong lĩnh vực công nghệ phần mềm, việc lựa chọn một phương pháp phát triển phù hợp đóng vai trò quyết định đến sự thành bại và tiến độ của toàn bộ dự án. Hiện nay, có nhiều mô hình phát triển được áp dụng rộng rãi với những đặc điểm quản trị riêng biệt. Điển hình như mô hình Thác nước truyền thống nổi bật với quy trình tuần tự chặt chẽ từ khâu lấy yêu cầu đến khâu bảo trì, nhưng lại bộc lộ điểm yếu là thiếu tính linh hoạt khi yêu cầu hệ thống thay đổi giữa chừng. Ngược lại, các phương pháp linh hoạt như Agile hay Scrum lại đề cao sự tương tác liên tục và khả năng thích ứng nhanh thông qua các chu kỳ phát triển ngắn, rất phù hợp cho các dự án khởi nghiệp có yêu cầu biến động liên tục. Nằm giữa hai thái cực này, mô hình phát triển Tăng dần nổi lên như một giải pháp dung hòa hiệu quả, cho phép chia nhỏ hệ thống thành các phần hành độc lập và chuyển giao từng phần một cách có hệ thống.

Sau khi phân tích kỹ lưỡng đặc thù của bài toán quản lý trung tâm bảo hành và cấu trúc nhân sự của nhóm, dự án quyết định lựa chọn mô hình phát triển Tăng dần làm kim chỉ nam xuyên suốt quá trình thực hiện. Theo phương pháp này, hệ thống quản lý bảo hành sẽ không được xây dựng và bàn giao cùng một lúc vào giai đoạn cuối cùng. Thay vào đó, toàn bộ khối lượng công việc sẽ được chia nhỏ thành các gói chức năng độc lập hay còn gọi là các phần tăng trưởng. Nhóm sẽ ưu tiên phân tích, lập trình và kiểm thử các phân hệ cốt lõi nhất trước, điển hình như module quản lý hồ sơ tiếp nhận và kiểm soát kho linh kiện. Sau khi các module nền tảng này hoạt động ổn định, dự án mới tiếp tục mở rộng sang các tính năng phụ trợ như cổng tra cứu trực tuyến cho khách hàng và bảng điều khiển thống kê cho ban quản lý.

Việc áp dụng mô hình Tăng dần mang lại nhiều ưu điểm vượt trội và đặc biệt phù hợp với định hướng tổ chức của đồ án môn học. Thứ nhất, phương pháp này giúp giảm thiểu rủi ro kỹ thuật ở mức thấp nhất vì mỗi module sau khi lập trình xong đều được đội ngũ chuyên trách thiết kế và kiểm thử đánh giá ngay lập tức, đảm bảo lỗi không bị tích tụ. Thứ hai, mô hình này cho phép nhóm sớm nhìn thấy các chức năng chạy thực tế ở ngay những giai đoạn đầu, từ đó dễ dàng thu thập phản hồi, đánh giá lại mục tiêu và điều chỉnh kịp thời nếu có sai lệch so với đặc tả ban đầu. Hơn nữa, việc chia nhỏ khối lượng công việc theo từng giai đoạn tăng trưởng giúp hai bộ phận phân tích yêu cầu và kiểm thử phối hợp nhịp nhàng hơn, tránh tình trạng dồn ứ công việc vào cuối kỳ và đảm bảo tiến độ bàn giao sản phẩm luôn được kiểm soát chặt chẽ.

5. ### Vai trò của thành viên dự án

| STT | Họ và tên | Mã SV | rAI | DT |
| ----- | :---- | :---- | :---- | :---- |
| 1 | Nguyễn Hoàng Thiện Anh | B23DCKD003 |  | x |
| 2 | Vũ Hữu Thịnh | B23DCKD066 |  | x |
| 3 | Hà Thanh Tùng | B23DCKD078 |  | x |
| 4 | Nguyễn Quốc Việt | B23DCKD081 |  | x |
| 5 | Nguyễn Thị Ngọc Hà | B23DCKD021 | x |  |
| 6 | Nguyễn Việt Hoàng | B23DCKD025 | x |  |
| 7 | Phạm Duy Tuấn Hùng | B23DCKD028 | x |  |
| 8 | Mai Công Vượng | B23DCKD083 | x |  |
| 9 | Lê Thuần Trường | B23DCKD075 | x |  |

   6. ### Phân công nhiệm vụ

   

| STT | Họ và tên | MSV | Nhiệm vụ |
| :---- | :---- | :---- | :---- |
| 1 | Nguyễn Hoàng Thiện Anh | B23DCKD003 | Thiết kế kiến trúc tổng thể, quy tắc đặt tên và thiết kế chi tiết luồng dữ liệu bảo hành.  |
| 2 | Vũ Hữu Thịnh | B23DCKD066 | Xác định mục tiêu chất lượng đo lường được, thực thi test chức năng và viết báo cáo lỗi  |
| 3 | Hà Thanh Tùng | B23DCKD078 | Thiết kế cơ sở dữ liệu và lưu trữ dữ liệu |
| 4 | Nguyễn Quốc Việt | B23DCKD081 | Xác định tiêu chuẩn kiểm thử, lập kế hoạch và viết kịch bản kiểm thử  |
| 5 | Nguyễn Thị Ngọc Hà | B23DCKD021 | Khảo sát hiện trạng, giới thiệu bài toán và đặc tả danh sách yêu cầu hệ thống.  |
| 6 | Nguyễn Việt Hoàng | B23DCKD025 | Lập kế hoạch dự án, thiết lập công nghệ và lập trình module Quản lý Ticket tiếp nhận.  |
| 7 | Phạm Duy Tuấn Hùng | B23DCKD028 | Phân tích và viết đặc tả Usecase cùng các workflow  |
| 8 | Mai Công Vượng | B23DCKD083 | Lập trình chức năng Dashboard báo cáo thống kê cho admin. Đánh giá ưu nhược điểm |
| 9 | Lê Thuần Trường | B23DCKD075 | Đánh giá chất lượng các yêu cầu và lập trình cổng tra cứu trực tuyến về tiến độ bảo hành cho khách hàng.  |

   

   7. ### Kế hoạch triển khai chi tiết

	Dự án được thực hiện trong 6 tuần, theo mô hình Tăng dần đã lựa chọn tại Mục 1.4, và chia thành ba giai đoạn:

Dự án được thực hiện trong 6 tuần, áp dụng mô hình phát triển tăng dần (Incremental Model) đã lựa chọn tại Mục 1.4, với ba giai đoạn chính:

* **Giai đoạn chuẩn bị và thiết kế tổng thể (P1–P3, tuần 1–3):** Khảo sát quy trình nghiệp vụ, thu thập và đặc tả yêu cầu, xác định phạm vi hệ thống, thiết kế kiến trúc và cơ sở dữ liệu tổng thể. Kết quả của giai đoạn này là cơ sở để triển khai các phần tăng trưởng tiếp theo.  
* **Giai đoạn phát triển tăng dần (P4–P5, tuần 4–5):** Hệ thống được xây dựng thông qua ba phần tăng trưởng, lần lượt tập trung vào quản lý tiếp nhận và phân công sửa chữa, theo dõi tiến độ và cảnh báo thời hạn, quản lý nhật ký sửa chữa và bàn giao giữa các kỹ thuật viên. Mỗi phần tăng trưởng thực hiện thiết kế chi tiết, lập trình, tích hợp và kiểm thử, tạo ra một phiên bản phần mềm hoạt động được, kế thừa và mở rộng các chức năng đã hoàn thành trước đó.  
* **Giai đoạn hoàn thiện và nghiệm thu (P6, tuần 6):** Thực hiện kiểm thử tổng thể, khắc phục các lỗi còn tồn đọng, đóng gói hệ thống, tổ chức nghiệm thu người dùng và hoàn thiện báo cáo, tài liệu bàn giao.  
  1.7.1 Phân chia các phần tăng trưởng 

Các phân hệ (mã theo Mục 2.2.3) được phân bổ theo mức độ ưu tiên nghiệp vụ và quan hệ phụ thuộc dữ liệu. Phần tạo ra dữ liệu gốc làm trước, phần chỉ đọc và tổng hợp dữ liệu làm sau.

| Mã | Phần tăng trưởng | Phân hệ | Nội dung chính | Căn cứ xếp thứ tự |
| :---- | :---- | :---- | :---- | :---- |
| INC1 | Tiếp nhận và kho linh kiện | TKT, WAR, INV | Lập phiếu tiếp nhận với mã TKT\_YYYYMMDD\_x; kiểm tra chính sách bảo hành; lịch sử trạng thái phiếu; quản lý linh kiện, nhập/xuất, cảnh báo ngưỡng tồn kho; đăng nhập và phân quyền | Đây là các module nền tảng ưu tiên đầu tiên theo Mục 1.4 và tạo ra dữ liệu gốc (phiếu, linh kiện) cho mọi phân hệ khác. |
| INC2 | Sửa chữa và kiểm soát tiến độ | REP, SLA | Phân công kỹ thuật viên; cập nhật quá trình sửa chữa; sử dụng linh kiện từ kho; tính ngày hẹn trả; cảnh báo đến hạn/quá hạn; email điểm tin 8:00 | Phụ thuộc vào cả phiếu và kho của INC1. Có rủi ro kỹ thuật cao (lập lịch, gửi email), nên làm ở giữa để còn thời gian sửa lỗi. |
| INC3 | Tra cứu và thống kê | PORTAL, DASH | Cổng tra cứu tiến độ cho khách hàng; dashboard thống kê, bộ lọc, xuất báo cáo Excel/PDF | Đây là tính năng phụ trợ theo Mục 1.4. Hai phân hệ chỉ đọc dữ liệu của INC1 và INC2 nên có thể phát triển độc lập, song song. |

 

**1.7.2. Kế hoạch theo thời gian**

| STT | Giai đoạn / Công việc chính | Phạm vi | Thời gian dự kiến | Sản phẩm bàn giao |
| :---- | :---- | :---- | :---- | :---- |
| 1 | **Khảo sát và khởi tạo (P1):** tìm hiểu quy trình bảo hành thực tế, xác định phạm vi dự án, lập kế hoạch dự án. | Toàn dự án | Tuần 1 | PMP, BRD, StRS (bản đầu) |
| 2 | **Phân tích và đặc tả yêu cầu (P2):** thu thập yêu cầu bên liên quan, xây dựng StRS và SRS; gán mã FR/NFR và xếp từng yêu cầu vào INC1, INC2 hoặc INC3. | Toàn dự án | Tuần 2 | StRS, SRS v1.0 |
| 3 | **Thiết kế hệ thống và CSDL (P3):** thiết kế kiến trúc tổng thể, CSDL chuẩn 3NF, giao diện UI; phác thảo kế hoạch và kịch bản kiểm thử. | Toàn dự án | Tuần 3 | SAD v1.0, kế hoạch kiểm thử (bản phác thảo) |
| 4 | **INC1:** lập trình TKT, WAR, INV (P4), sau đó kiểm thử tích hợp và đối chiếu TB.01-TB.10 (P5). Quản lý mã bằng Git, kiểm thử đơn vị sau từng chức năng. | INC1 | Tuần 4 | Mã nguồn tag INC1-v1.0, báo cáo kiểm thử INC1 |
| 5 | **INC2:** lập trình REP, SLA (P4); kiểm thử INC2 và hồi quy INC1, gồm kịch bản SLA theo SRS (P5). | INC2 \+ hồi quy INC1 | Tuần 5 (đầu-giữa) | Mã nguồn tag INC2-v1.0, báo cáo kiểm thử INC2 |
| 6 | **INC3:** lập trình PORTAL, DASH (P4); kiểm thử INC3, hồi quy INC1-INC2, đo hiệu năng và hiển thị Dashboard (P5). | INC3 \+ hồi quy INC1-2 | Tuần 5 (giữa) \- đầu tuần 6 | Mã nguồn tag INC3-v1.0, báo cáo kiểm thử INC3 |
| 7 | **Đóng gói, nghiệm thu và báo cáo (P6):** đóng gói hệ thống Docker, nghiệm thu UAT trên hệ thống tích hợp, hoàn thiện báo cáo và biên bản nghiệm thu. | Toàn hệ thống | Tuần 6 | Gói Docker, biên bản nghiệm thu, báo cáo hoàn chỉnh |

**1.7.3. Nguyên tắc vận hành mỗi phần tăng trưởng**

* **Phối hợp giữa hai nhóm:** khi nhóm DT kiểm thử INC(n), nhóm rAI đã bắt đầu lập trình INC(n+1). Cách này tránh dồn việc về cuối kỳ như đã nêu ở Mục 1.4. Kịch bản kiểm thử chi tiết của mỗi phần tăng trưởng được hoàn thiện trước khi kiểm thử phần đó.  
* **Điều kiện chuyển sang kiểm thử (P5):** phần tăng trưởng đạt các mục TB.01-TB.10 trong danh sách kiểm tra tại Mục 2.4. TB.11 và TB.12 (dữ liệu 5.000 phiếu, tách logic thống kê khỏi biểu đồ) chỉ áp dụng cho INC3.  
* **Điều kiện bàn giao một phần tăng trưởng:** các độ đo tại Mục 2.3 gắn với phần đó đạt ngưỡng đặt ra, không còn lỗi nghiêm trọng chưa xử lý, và mã nguồn được gắn nhãn trên Git:

| Phần tăng trưởng | Độ đo cần đạt |
| :---- | :---- |
| INC1 | T02, T03, T06, T07, T10 |
| INC2 | T04, T07, T09 (kèm hồi quy các độ đo của INC1) |
| INC3 | T11, T12, T13 |

* **Độ đo dùng chung:** T01 (tỷ lệ test chức năng đạt), T05 (thời gian phản hồi) và T06 (kiểm soát truy cập) được đo ở mỗi phần tăng trưởng cho các chức năng của phần đó. T08 (hoàn thành tác vụ người dùng) được đánh giá khi nghiệm thu UAT ở P6.  
* **Vòng phản hồi:** kết quả kiểm thử và nhận xét sau mỗi phần tăng trưởng được dùng để điều chỉnh yêu cầu và thiết kế cho phần kế tiếp. Mọi thay đổi tài liệu cập nhật phiên bản theo Mục 2.2.6 (ví dụ SRS v1.0 lên v1.1).  
* **Phạm vi xây dựng và kiểm thử trong Chương 5:** Chương 5 trình bày tối thiểu 20% yêu cầu quan trọng nhất, được chọn từ các chức năng đã lập trình ở INC1-INC3.

  8. ### Quy tắc sử dụng công cụ AI hỗ trợ trong dự án

(*Nếu dự án không sử dụng công cụ AI thì ghi rõ “Không sử dụng”.*  
*nếu dự án có sử dụng các công cụ AI thì phải trình bày mục này như sau*)

Trong dự án này, chúng em có sử dụng các công cụ AI hỗ trợ như sau:

| Pha | Tên công cụ | Mục đích sử dụng |
| :---- | :---- | :---- |
| Khảo sát & Phân tích  | Gemini  | Gợi ý quy trình nghiệp vụ, sinh User Story, rà soát tính nhất quán của tài liệu yêu cầu.  |
|  |  |  |
|  |  |  |

Việc sử dụng sẽ tuân thủ theo các quy tắc như sau:  
**AUR.01:** AI chỉ đóng vai trò là công cụ hỗ trợ, gợi ý và tăng tốc độ phát triển. Mọi quyết định cuối cùng về nghiệp vụ, thiết kế kiến trúc và chất lượng mã nguồn phải do thành viên nhóm xem xét, phê duyệt và chịu hoàn toàn trách nhiệm. *(Căn cứ: tham khảo ISO/IEC 42001:2023 về quản lý việc sử dụng AI ).*  
   
**AUR.02:** Tuyệt đối không sao chép (copy-paste) nguyên văn mã nguồn hoặc văn bản từ AI mà không hiểu rõ bản chất. Thành viên sử dụng bắt buộc phải rà soát (review), chỉnh sửa và chú thích để đảm bảo phù hợp với ngữ cảnh thực tế của đề tài. (Căn cứ: *tham khảo ISO/IEC 23894:2023* ). 

**AUR.03:** Không được đưa các thông tin mật, dữ liệu thật của khách hàng hoặc thông tin cá nhân nhạy cảm lên các công cụ AI công cộng để đảm bảo an toàn thông tin và quyền riêng tư. (Căn cứ: *tham khảo ISO/IEC 27001:2022 về quản lý an toàn thông tin* ). 

**AUR.99**: Mỗi sản phẩm trong báo cáo này nếu sử dụng sự hỗ trợ của AI thì phải được ghi chú tại nơi trình bày sản phẩm đó bằng footnote dẫn chiếu tới mục tương ứng trong PHỤ LỤC Z.

## **CHƯƠNG 2\. SẢN PHẨM CHUYỂN GIAO GIỮA CÁC PHA**  **VÀ TIÊU CHUẨN ĐÁNH GIÁ**

1. ### **Danh mục tài liệu, sản phẩm**

| STT | Loại tài liệu / Sản phẩm chuyển giao | Biểu mẫu quy chuẩn | Tiêu chuẩn đánh giá | P1  | P2  | P3  | INC1  | INC2  | INC3 | P6  |
| :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Kế hoạch quản trị dự án (PMP) |  |  | **O** | I | I | I | I | I | I |
| **2** | Tài liệu yêu cầu nghiệp vụ (BRD) |  |  | **O** | I |  |  |  |  |  |
| **3** | Đặc tả yêu cầu bên liên quan (StRS) |  |  | **O** | **I/O** | I | I |  |  |  |
| **4** | Đặc tả yêu cầu phần mềm (SRS) |  |  |  | **O** | I | **I/O** | **I/O** | I | I |
| **5** | Thiết kế kiến trúc & CSDL tổng thể (SAD) |  |  |  |  | **O** | I | I | I | I |
| **6** | Kế hoạch & Kịch bản kiểm thử  |  |  |  |  | **O** | **I/O** | **I/O** | **I/O** | I |
| **7** | Mã nguồn tăng dần INC1  |  |  |  |  |  | **O** | I | I | I |
| **8** | Báo cáo kiểm thử tăng dần INC1  |  |  |  |  |  | **O** | I |  |  |
| **9** | Mã nguồn tăng dần INC2  |  |  |  |  |  |  | **O** | I | I |
| **10** | Báo cáo kiểm thử tăng dần INC2 |  |  |  |  |  |  | **O** | I |  |
| **11** | Mã nguồn tăng dần INC3  |  |  |  |  |  |  |  | **O** | I |
| **12** | Báo cáo kiểm thử tăng dần INC3  |  |  |  |  |  |  |  | **O** | I |
| **13** | Gói triển khai hệ thống  |  |  |  |  |  |  |  |  | **O** |
| **14** | Biên bản nghiệm thu người dùng  |  |  |  |  |  |  |  |  | **O** |
| **15** | Báo cáo tổng kết đồ án hoàn chỉnh  |  |  |  |  |  |  |  |  | **O** |
| **16** | Nhật ký sử dụng công cụ AI (Phụ lục Z) |  |  | **I/O** | **I/O** | **I/O** | **I/O** | **I/O** | **I/O** | **O** |

2. ### **Quy tắc đặt tên (naming convention)**

	Trong quá trình phát triển phần mềm quản lý hoạt động bảo hành của trung tâm hỗ trợ kỹ thuật, việc thống nhất cách đặt tên là cần thiết nhằm đảm bảo tính nhất quán giữa các tài liệu phân tích, thiết kế, mã nguồn và cơ sở dữ liệu. Quy tắc này giúp các thành viên dễ dàng nhận biết, tra cứu, quản lý phiên bản và phối hợp trong quá trình thực hiện dự án.  
	Dự án áp dụng mô hình phát triển Tăng dần, các tài liệu và sản phẩm phần mềm có thể được tạo mới hoặc cập nhật qua nhiều lần phát triển. Từ đó, nhóm vừa có thể theo dõi kịp thời tiến độ công việc dự án

1. #### **Nguyên tắc đặt tên chung**

	Các tài liệu, thư mục và thành phần của hệ thống cần tuân thủ những nguyên tắc sau: 

- Tên của tài liệu, thư mục hay thành phần phải ngắn gọi, rõ ràng và phản ảnh được đúng chức năng, nội dung.  
- Sử dụng tiếng Anh hoặc các chữ cái viết tắt được thống nhất khi đặt tên các thành phần kỹ thuật    
- Không sử dụng dấu tiếng Việt, dấu cách và ký tự đặc biệt trong tệp tin, thư mục hoặc mã định danh, ngoại trừ các ký tự phân tách được quy định  
- Thống nhất cách viết chữ hoa, chữ thường và ký tự phân tách cho từng loại đối tượng.  
- Các tài liệu chính thức cần được quản lý phiên bản nhằm phân biệt các lần cập nhật.  
- Không đặt tên tùy ý gây trùng lặp hoặc khó hiểu, khó xác định chức năng giữa các chức năng công việc

	Nhóm sử dụng mã dự án PSE.G102 để định danh các tài liệu và sản phẩm phát triển 

2. **Quy tắc đặt tên tài liệu**

	Các tài liệu được đặt tên theo cấu trúc:  
PSE.G102\_\[Increment\]\_\[DocumentType\]\_\[Description\]\_\[Version\].\[Extension\]  
	Trong đó:

| Thành phần | Ý nghĩa |
| :---- | :---- |
| PSE.G102 | Mã định danh của dự án |
| Increment | Mã phần tăng trưởng |
| DocumentType | Loại tài liệu |
| Description | Nội dung hoặc chức năng được mô tả |
| Version | Phiên bản tài liệu |
| Extension | Định dạng tệp |

	  
	Đối với những tài liệu sử dụng chung cho toàn bộ dự án, nhóm có thể bỏ thành phần Increment và sử dụng mã PSE.G102 để định danh.

3. **Quy tắc đặt tên yêu cầu và chức năng hệ thống**

	Mỗi yêu cầu và chức năng được gán một mã định danh duy nhất để thuận tiện cho việc liên kết giữa các tài liệu đặc tả, thiết kế và kiểm thử. Cấu trúc mã yêu cầu chức năng:  
FR\_\[Module\]\_\[Number\]  
	Cấu trúc mã yêu cầu phi chức năng:  
NFR\_\[Category\]\_\[Number\]  
	Trong đó:

- FR ( Functional Requirement): Yêu cầu chức năng  
- NFR (Non-Functional Requirement): Yêu cầu phi chức năng  
- Module: Mã chức năng  
- Category: Nhóm yêu cầu phi chức năng  
- Number: Số thứ tự tăng dần

	Các phân hệ của hệ thống được quy ước như sau:

| Mã | Chức năng |
| ----- | ----- |
| TKT | Quản lý phiếu tiếp nhận bảo hành |
| WAR | Kiểm tra và xử lý chính sách bảo hành |
| REP | Quản lý quá trình sửa chữa |
| INV | Quản lý kho linh kiện |
| SLA | Theo dõi thời hạn và cảnh báo tiến độ |
| PORTAL | Cổng tra cứu dành cho khách hàng |
| DASH | Dashboard thống kê và báo cáo |

	Đối với yêu cầu phi chức năng, sử dụng các nhóm như PERF (hiệu năng), SEC (bảo mật), REL (độ tin cậy)

4. **Quy tắc đặt tên mã nguồn và cơ sở dữ liệu**  
1. **Quy tắc đặt tên mã nguồn**

	Các thành phần mã nguồn được đặt tên theo chức năng và thống nhất cách viết

| Đối tượng | Quy tắc | Ví dụ |
| ----- | ----- | ----- |
| Tên lớp | PascalCase | WarrantyTicket |
| Tên hàm/phương thức | camelCase | createWarrantyTicket |
| Tên biến | camelCase | warrantyStatus |
| Hằng số | UPPER\_SNAKE\_CASE | MAX\_REPAIRS\_DAYS |
| Tên thư mục module | lowercase | tickets, reports |
| Tên tệp cấu hình | lowercase | appconfig |

	Các quy tắc trên là quy ước chung; khi triển khai có thể cần điều chỉnh cho phù hợp với ngôn ngữ lập trình và framework

2. **Quy tắc đặt tên cơ sở dữ liệu**

	Các bảng và trường dữ liệu thường sử dụng kiểu chữ thường, các từ được phân tách bằng dấu gạch dưới hoặc theo quy tắc PascalCase

| Đối tượng | Tên đề xuất |
| ----- | ----- |
| Bảng khách hàng | Customers |
| Bảng thiết bị | Devices |
| Bảng phiếu bảo hành | WarrantyTickets |
| Bảng lịch sử trạng thái | TicketStatusHistory |
| Bảng linh kiện | SpareParts |
| Bảng sử dụng linh kiện | RepairTicketParts |
| Bảng nhật ký gửi email | SlaEmailLogs |

	  
	Các trường dữ liệu được đặt tên rõ nghĩa, tránh sử dụng các từ viết tắt không thống nhất và theo PascalCase. Đặc biệt, các trường phải được sử dụng thống nhất trong nhiều cơ chế phải thống nhất với nhau

5. **Quy tắc đặt tên mã phiếu nghiệp vụ**

	Để hỗ trợ việc quản lý và tra cứu thông tin trong quá trình bảo hành, mỗi phiếu tiếp nhận thiết bị được cấp một mã duy nhất  
	Cấu trúc đề xuất:  
TKT\_YYYYMMDD\_x  
	Trong đó:

- TKT: Mã phiếu tiếp nhận thiết bị  
- YYYYMMDD: Ngày tạo phiếu theo định dạng năm, tháng, ngày  
- x: Số thứ tự của phiếu trong ngày, được hệ thống tự động cấp theo thứ tự tăng dần

	Mã phiếu được sử dụng xuyên suốt các công đoạn tiếp nhận, kiểm tra bảo hành, sửa chữa, theo dõi tiến độ và bàn giao thiết bị. Việc thống nhất mã phiếu giúp hạn chế nhầm lẫn giữa các thiết bị và đảm bảo khả năng truy xuất lịch sử xử lý 

6. **Quy tắc quản lý phiên bản và mã nguồn**

	Do dự án sử dụng mô hình phát triển Tăng dần, mỗi phần tăng trưởng được gán mã riêng để phân biệt các đợt phát triển. Đối với tài liệu, nhóm sử dụng quy tắc đánh số phiên bản:

| Phiên bản | Ý nghĩa |
| ----- | ----- |
| v1.0 | Phiên bản chính thức đầu tiên |
| v1.1 | Cập nhật hoặc bổ sung nội dung nhỏ |
| v2.0 | Thay đổi lớn về chức năng, nội dung, cấu trúc |

	Mỗi lần cập nhật mã nguồn cần có một đoạn note hoặc logs để mô tả ngắn gọn sự thay đổi về nội dung, chức năng. Việc tuân thủ các quy tắc này tạo điều kiện thuận lợi cho nhóm trong việc theo dõi lịch sử thay đổi, phối hợp phát triển các chức năng  
	Tóm lại, hệ thống quy tắc đặt tên được xây dựng nhằm chuẩn hóa cách quản lý tài liệu, mã nguồn và dữ liệu trong dự án. Đây được coi là cơ sở nhưng mới chỉ là những đề xuất để đảm bảo tính nhất quán, khả năng truy xuất và thuận tiện trong quá trình phát triển, kiểm thử, bảo trì phần mềm quản lý hoạt động bảo hành.

3. ### Xác định mục tiêu chất lượng của dự án

Trong quá trình phát triển phần mềm quản lý hoạt động bảo hành của trung tâm kỹ thuật thì việc xác định mục tiêu chất lượng là cần thiết nhằm đảm bảo hệ thống đáp ứng được các nhu cầu nghiệp vụ và hoạt động thường ngày ổn định. Dựa trên quy trình nhóm thu thập được, đồng thời tham khảo mô hình chất lượng sản phẩm phần mềm ISO/IEC 25010:2023, nhóm tập trung vào các đặc tính: tính phù hợp chức năng, hiệu năng, độ tin cậy, độ an toàn và khả năng tương tác. Các mục tiêu được cụ thể thông qua những độ đo và ngưỡng đánh giá để làm cơ sở.

| Mã | Tên độ đo | Ý nghĩa | Cách đo |
| ----- | :---: | :---: | :---: |
| T01 | Tỷ lệ kiểm thử chức năng đạt | Đánh giá mức độ hoàn thiện các yêu cầu chức năng của hệ thống. | Số testcase đạt/ tổng số testcase thực thi.( ≥ 95% ) |
| T02 | Tỷ lệ xử lý đúng quy tắc bảo hành | Đảm bảo hệ thống phân loại đúng trường hợp. | Số trường hợp xử lý đúng/ tổng trường hợp (100%) |
| T03 | Tỷ lệ lưu trữ hồ sơ chính xác | Đảm bảo thông tin khách hàng, thiết bị, phiếu yêu cầu được lưu trữ đầy đủ. | Số lưu trữ đúng/ tổng hồ sơ kiểm tra (100%)  |
| T04 | Cảnh báo hạn trả chính xác | Đảm bảo hệ thống xác định đúng các thiết bị đến hạn hoặc quá hạn. | Số phiếu đúng/ tổng kiểm thử (100%) |
| T05 | Thời gian phản hồi | Đánh giá tốc độ khi tiếp nhận, tra cứu và cập nhật. | Gửi nhiều yêu cầu,ghi lại thời gian phản hồi (\< 3s) |
| T06 | Kiểm soát truy cập đúng | Đảm bảo đối tượng phân quyền có thể sử dụng đúng chức năng. | Số yêu cầu trái quyền bị từ chối đúng/ tổng số yêu cầu trái quyền (100%) |
| T07 | Cập nhật trạng thái chính xác | Đảm bảo tiến độ xử lý thiết bị được cập nhật đúng theo quy trình. | Số lần cập nhật xử lý đúng/ tổng lần cập nhật kiểm thử (100%) |
| T08 | Hoàn thành tác vụ người dùng | Giao các tác vụ thực tế, ghi nhận tỷ lệ hoàn thành. | Số tác vụ hoàn thành đúng/ tổng tác vụ được giao (\> 90%) |
| T09 | Gửi email cảnh báo thành công | Đánh giá độ tin cậy của chức năng email điểm tin 8:00 sáng cho quản lý. | Số lần gửi được chấp nhận/ tổng lần gửi hợp lệ được thử ( ≥ 95%) |
| T10 | Cập nhật tồn kho chính xác | Đảm bảo linh kiện được cập nhật đúng sau khi nhập/xuất và đã sử dụng. | Số trường hợp cập nhật đúng/ tổng trường hợp cập nhật (100%) |
| T11  | Độ chính xác số liệu tổng hợp trên Dashboard  | Đảm bảo các chỉ số thống kê hiển thị cho Admin khớp tuyệt đối với dữ liệu gốc.  | Đối chiếu trực tiếp số liệu trên Dashboard với câu lệnh truy vấn SQL độc lập (COUNT, SUM). Đạt 100%.  |
| T12  | Thời gian tải biểu đồ và xuất tệp báo cáo  | Đảm bảo Admin lọc báo cáo theo khoảng thời gian, kỹ thuật viên hoặc dòng máy và xuất file Excel/PDF nhanh chóng khi dữ liệu lớn.  | Đo bằng Chrome DevTools trên tập dữ liệu $\geq 5.000$ phiếu bảo hành. Mục tiêu: tải biểu đồ $\leq 2s$, xuất báo cáo $\leq 3s$.  |
| T13  | Tương thích hiển thị Dashboard đa thiết bị và in ấn  | Đảm bảo các biểu đồ thống kê hiển thị rõ nét, không vỡ bố cục trên cả máy tính lẫn điện thoại và in ấn chuẩn khổ A4.  | Kiểm tra giao diện thực tế trên màn hình Desktop ($1920\times 1080$), Mobile ($375\times 812$) và bản xuất PDF khổ A4 (100% đạt chuẩn).  |

Các độ đo này là cơ sở để xây dựng các giai đoạn kiểm thử, xác định tiêu chí chấp nhận và đánh giá mức độ hoàn thiện của phần mềm. 

4. ### Xác định tiêu chuẩn Kiểm thử được (Testability) cho dự án

   1. #### Khái niệm, ý nghĩa của đặc tính Kiểm thử được

Theo mô hình chất lượng sản phẩm phần mềm ISO/IEC 25010:2023, Kiểm thử được (Testability) là một đặc tính con của nhóm Khả năng bảo trì (Maintainability), được định nghĩa là mức độ hiệu quả và hiệu suất mà các tiêu chí kiểm thử có thể được thiết lập cho một hệ thống, sản phẩm hoặc thành phần, và các phép kiểm thử có thể được thực hiện để xác định xem các tiêu chí đó đã được đáp ứng hay chưa. Nói cách khác, đây là khả năng của phần mềm hỗ trợ việc thiết kế và thực hiện các phép kiểm tra khách quan, khả thi nhằm xác định yêu cầu đã được đáp ứng hay chưa. Đặc tính này được thể hiện qua khả năng thiết lập dữ liệu đầu vào, điều khiển điều kiện thực hiện, quan sát kết quả và lặp lại phép kiểm tra.

Trong lý thuyết kiểm thử phần mềm, R. V. Binder đã khái quát hoá tính kiểm thử được thành hai nhóm nhân tố cơ bản là tính điều khiển được (controllability) và tính quan sát được (observability): một thành phần chỉ có thể kiểm thử được khi kiểm thử viên vừa đưa được hệ thống về trạng thái mong muốn, vừa nhìn thấy được kết quả mà hệ thống tạo ra. Đây chính là cơ sở lý thuyết để nhóm cụ thể hoá các tiêu chí ở Mục 2.4.2.

Đối với hệ thống quản lý hoạt động bảo hành của trung tâm hỗ trợ kỹ thuật, nhiều chức năng phụ thuộc vào thời gian, trạng thái thiết bị và dịch vụ bên ngoài. Chẳng hạn, việc phân loại máy hẹn trả hôm nay hoặc ngày mai phụ thuộc vào ngày hiện tại; chức năng báo cáo điểm tin phụ thuộc vào lịch chạy lúc 8 giờ sáng và dịch vụ gửi email bên ngoài. Vì vậy, hệ thống cần cho phép giả lập thời gian, chuẩn bị dữ liệu mẫu và kiểm tra riêng từng thành phần mà không phải chờ đến thời điểm vận hành thực tế.

Bên cạnh các nghiệp vụ phụ thuộc mốc thời gian thực, đối với phân hệ Dashboard báo cáo thống kê dành cho Admin, tính kiểm thử được còn thể hiện ở khả năng tách biệt logic tính toán tổng hợp số liệu khỏi giao diện biểu đồ. Điều này cho phép nhóm nạp các bộ dữ liệu giả lập có quy mô lớn, đa dạng trạng thái phiếu bảo hành để kiểm chứng nhanh độ chính xác của các chỉ số thống kê và tệp báo cáo xuất ra.

Ý nghĩa của việc xác định và tuân thủ tiêu chuẩn Kiểm thử được đối với dự án được thể hiện ở bốn khía cạnh chính:

·     Về mặt kỹ thuật: bảo đảm mọi yêu cầu chức năng và phi chức năng trong tài liệu đặc tả (SRS) đều có thể được chuyển thành ít nhất một ca kiểm thử có kết quả mong đợi xác định, không mơ hồ; nhờ đó nhóm phát hiện sai lệch nghiệp vụ, tái hiện lỗi và kiểm tra hồi quy sau khi sửa đổi.

·     Về mặt quy trình: do dự án áp dụng mô hình phát triển Tăng dần, mỗi phần tăng trưởng đều phải được kiểm thử và nghiệm thu ngay khi hoàn thành. Nếu phần mềm không kiểm thử được, chi phí kiểm thử hồi quy ở các vòng lặp sau sẽ tăng theo cấp số nhân và lỗi sẽ bị tích tụ sang pha sau.

·     Về mặt chi phí: các nghiên cứu về kinh tế phần mềm (B. Boehm) cho thấy chi phí khắc phục một lỗi tăng lên nhiều lần theo từng pha phát hiện muộn. Thiết kế hệ thống có tính kiểm thử được cao giúp dịch chuyển việc phát hiện lỗi về phía trái của vòng đời (shift-left), qua đó giảm chi phí sửa lỗi.

·     Về mặt nghiệm thu: tính kiểm thử được là điều kiện cần để đo lường khách quan các độ đo chất lượng T01–T13 đã nêu tại Mục 2.3; nếu không điều khiển và quan sát được hệ thống thì các tỷ lệ như “tỷ lệ cảnh báo hạn trả chính xác 100%” hay “thời gian phản hồi dưới 3 giây” không thể chứng minh được bằng số liệu.

Vì vậy, nhóm xác định tính kiểm thử được vừa là một ràng buộc thiết kế bắt buộc đối với nhóm Thiết kế – Lập trình, vừa là tiêu chuẩn đầu vào (entry criteria) mà sản phẩm của pha P4 phải thoả mãn trước khi được chuyển giao sang pha kiểm thử P5.

2. #### Chi tiết hóa các tiêu chí của đặc tính Kiểm thử được

Căn cứ định nghĩa của ISO/IEC 25010:2023 và các nhân tố kiểm thử được của Binder, nhóm cụ thể hoá đặc tính Kiểm thử được thành sáu tiêu chí. Mỗi tiêu chí được mô tả kèm yêu cầu cụ thể, có thể kiểm chứng được, đối với hệ thống quản lý bảo hành của đề tài.

| STT | Tiêu chí | Yêu cầu cụ thể đối với dự án |
| ----- | :---- | :---- |
| 1 | **Tính điều khiển được (Controllability)** Khái niệm: Mức độ hệ thống cho phép kiểm thử viên chủ động thiết lập dữ liệu đầu vào và trạng thái môi trường thực thi. Mô tả: Khả năng đưa các biến số, tham số cấu hình và trạng thái dữ liệu về đúng kịch bản mong muốn trước khi chạy kiểm thử. | • Hệ thống phải cung cấp bộ dữ liệu mẫu (seed data) nạp được bằng một lệnh duy nhất, gồm đầy đủ các vai trò người dùng (Admin, Nhân viên tiếp nhận, Kỹ thuật viên, Thủ kho, Khách hàng) và các phiếu bảo hành ở mọi trạng thái của vòng đời. • Thời gian hệ thống phải lấy qua một thành phần trừu tượng (service lấy ngày giờ) thay vì gọi trực tiếp hàm ngày giờ của hệ điều hành, để kiểm thử viên giả lập được mốc thời gian khi kiểm thử cảnh báo hạn trả và báo cáo điểm tin 8:00. • Tác vụ chạy theo lịch (gửi email điểm tin) phải có điểm kích hoạt thủ công dành cho môi trường kiểm thử, không bắt buộc chờ đến đúng 8 giờ sáng. • Phân hệ Dashboard Admin và cơ sở dữ liệu dự án phải hỗ trợ cơ chế nạp nhanh bộ dữ liệu mẫu đa trạng thái để kiểm thử biểu đồ tổng hợp mà không cần chờ dữ liệu phát sinh thực tế. • Giao diện và API thống kê phải cho phép thiết lập độc lập các tham số bộ lọc đầu vào (khoảng thời gian, kỹ thuật viên, trạng thái phiếu) để kiểm thử từng kịch bản riêng biệt. |
| 2 | **Tính quan sát được (Observability)** Khái niệm: Mức độ dễ dàng theo dõi trạng thái xử lý bên trong và kết quả đầu ra của phần mềm sau mỗi thao tác. Mô tả: Hệ thống cung cấp đầy đủ phản hồi trực quan, nhật ký thực thi và mã trạng thái giúp nhận diện chính xác dữ liệu đúng hay sai. | • Mọi thao tác thay đổi dữ liệu (tạo phiếu, phân công, đổi trạng thái, xuất/nhập linh kiện) phải trả về thông báo rõ ràng trên giao diện: thành công hoặc nội dung lỗi cụ thể, không dừng ở thông báo chung chung. • Toàn bộ API phải trả về mã trạng thái HTTP đúng ngữ nghĩa (200/201 khi thành công, 400 khi dữ liệu sai, 401/403 khi sai quyền, 404 khi không tìm thấy) kèm thân phản hồi có cấu trúc thống nhất để kiểm thử viên đối chiếu tự động. • Hệ thống phải ghi nhật ký (log) các sự kiện quan trọng: đăng nhập, đổi trạng thái phiếu, xuất kho linh kiện, gửi email cảnh báo – kèm mốc thời gian và tài khoản thực hiện, phục vụ đối chiếu khi kiểm thử độ đo T07 và T09. • Mỗi phiếu bảo hành phải có màn hình lịch sử thay đổi trạng thái, cho phép quan sát trực tiếp kết quả nghiệp vụ mà không cần truy vấn thủ công vào cơ sở dữ liệu. • Kết quả gửi email phải được lưu lại trạng thái (đã gửi / thất bại / lý do) để kiểm chứng được mà không phụ thuộc vào hộp thư người nhận. |
| 3 | **Tính tách biệt được (Isolateability)** Khái niệm: Mức độ một thành phần có thể được kiểm thử độc lập với các thành phần còn lại của hệ thống. Mô tả: Các module có ranh giới rõ ràng, phụ thuộc được tiêm vào từ bên ngoài nên có thể thay thế bằng đối tượng giả lập khi kiểm thử. | • Kiến trúc phải tách rõ ba lớp: giao diện, nghiệp vụ và truy cập dữ liệu; logic nghiệp vụ không được viết lẫn trong mã giao diện để có thể kiểm thử đơn vị. • Các dịch vụ bên ngoài (gửi email, đồng hồ hệ thống, lưu trữ tệp) phải được truy cập qua giao diện trừu tượng, cho phép thay bằng đối tượng giả lập (mock/stub) khi chạy kiểm thử tự động, tránh gửi email thật ra ngoài. • Logic tính toán số liệu của Dashboard phải tách khỏi phần vẽ biểu đồ để kiểm thử riêng độ chính xác của con số thống kê. • Mỗi module (Tiếp nhận phiếu, Điều phối kỹ thuật, Kho linh kiện, Cổng tra cứu, Dashboard) phải kiểm thử được độc lập ngay khi hoàn thành phần tăng trưởng tương ứng, không phải chờ toàn bộ hệ thống hoàn thiện. |
| 4 | **Tính dễ hiểu (Understandability)** Khái niệm: Mức độ kiểm thử viên hiểu đúng và đủ hành vi mong đợi của hệ thống để thiết kế ca kiểm thử. Mô tả: Yêu cầu, quy tắc nghiệp vụ và tài liệu kỹ thuật được mô tả rõ ràng, nhất quán, có thể truy vết từ yêu cầu tới ca kiểm thử. | • Mỗi yêu cầu trong tài liệu SRS phải có mã định danh duy nhất và kết quả mong đợi có thể phán định đúng/sai, không chứa các từ mơ hồ như “nhanh”, “thân thiện”, “hợp lý”. • Các quy tắc nghiệp vụ bảo hành (điều kiện còn hạn bảo hành, phân loại lỗi do nhà sản xuất hay do người dùng, cách tính ngày hẹn trả, ngưỡng tồn kho an toàn) phải được phát biểu tường minh dưới dạng điều kiện – hành động làm cơ sở thiết kế ca kiểm thử. • Vòng đời trạng thái của phiếu bảo hành phải được mô hình hoá bằng biểu đồ trạng thái UML, chỉ rõ các chuyển trạng thái hợp lệ và không hợp lệ. • Phải duy trì ma trận truy vết yêu cầu – ca kiểm thử (RTM) để chứng minh mọi yêu cầu đều được phủ bởi ít nhất một ca kiểm thử. |
| 5 | **Khả năng tự động hoá (Automatability)** Khái niệm: Mức độ các phép kiểm thử có thể được thực hiện lại bằng công cụ mà không cần thao tác thủ công. Mô tả: Hệ thống cung cấp giao diện lập trình ổn định và các phần tử giao diện có định danh bền vững để công cụ kiểm thử truy cập. | • Toàn bộ nghiệp vụ cốt lõi phải truy cập được qua API có hợp đồng ổn định (đường dẫn, tham số, định dạng dữ liệu) để viết kiểm thử tự động mức tích hợp. • Các phần tử giao diện quan trọng (ô nhập, nút bấm, bảng dữ liệu) phải có thuộc tính định danh cố định, không phụ thuộc vị trí hiển thị hay nhãn tiếng Việt, để kịch bản kiểm thử giao diện không bị hỏng khi thay đổi bố cục. • Hệ thống phải chạy được bằng Docker với cấu hình môi trường tách rời, cho phép dựng lại môi trường kiểm thử sạch và chạy bộ kiểm thử hồi quy tự động sau mỗi lần tích hợp mã nguồn. • Phải có tập dữ liệu kiểm thử chuẩn và lệnh khôi phục cơ sở dữ liệu về trạng thái ban đầu để bộ kiểm thử tự động chạy lặp lại được nhiều lần. |
| 6 | **Tính ổn định và lặp lại được (Stability / Repeatability)** Khái niệm: Mức độ hệ thống cho cùng một kết quả khi lặp lại cùng một phép kiểm thử trong cùng điều kiện. Mô tả: Kết quả kiểm thử không bị ảnh hưởng bởi dữ liệu còn sót lại, thứ tự thực thi hay thay đổi ngoài kiểm soát của phiên bản phần mềm. | • Mỗi ca kiểm thử phải tự chuẩn bị và tự dọn dẹp dữ liệu, bảo đảm kết quả không phụ thuộc vào thứ tự thực thi của các ca kiểm thử khác. • Môi trường kiểm thử phải tách biệt hoàn toàn với môi trường phát triển và dữ liệu thật của khách hàng; cấu hình môi trường được quản lý bằng tệp cấu hình riêng. • Phiên bản mã nguồn đưa vào kiểm thử phải được gắn nhãn (tag) trên Git; mọi lỗi ghi nhận đều phải chỉ rõ phiên bản phát sinh để tái hiện lại được. • Thay đổi mã nguồn chỉ được chấp nhận khi toàn bộ bộ kiểm thử hồi quy đã chạy lại thành công trên phiên bản mới. |

Để bảo đảm các tiêu chí trên thực sự phục vụ việc đo lường chất lượng, nhóm thiết lập ánh xạ giữa sáu tiêu chí kiểm thử được và các độ đo chất lượng T01–T13 đã xác định tại Mục 2.3. Ánh xạ này cho thấy mỗi độ đo đều có điều kiện kỹ thuật tương ứng để đo được trên thực tế.

| Độ đo | Nội dung độ đo (Mục 2.3) | Tiêu chí Kiểm thử được cần thoả mãn |
| :---: | ----- | ----- |
| T01 | Tỷ lệ kiểm thử chức năng đạt (\> 94%) | 4 – Tính dễ hiểu; 5 – Khả năng tự động hoá |
| T02 | Tỷ lệ xử lý đúng quy tắc bảo hành (100%) | 1 – Điều khiển được; 4 – Tính dễ hiểu |
| T03 | Tỷ lệ lưu trữ hồ sơ chính xác (100%) | 2 – Quan sát được; 6 – Lặp lại được |
| T04 | Cảnh báo hạn trả chính xác (100%) | 1 – Điều khiển được (giả lập thời gian); 2 – Quan sát được |
| T05 | Thời gian phản hồi (\< 3s) | 5 – Tự động hoá; 6 – Ổn định, lặp lại được |
| T06 | Kiểm soát truy cập đúng (100%) | 2 – Quan sát được (mã trạng thái 401/403); 3 – Tách biệt được |
| T07 | Cập nhật trạng thái chính xác (100%) | 2 – Quan sát được (nhật ký, lịch sử trạng thái); 4 – Dễ hiểu |
| T08 | Hoàn thành tác vụ người dùng (\> 90%) | 4 – Tính dễ hiểu; 2 – Quan sát được |
| T09 | Gửi email cảnh báo thành công (\> 95%) | 1 – Điều khiển được; 3 – Tách biệt được (giả lập dịch vụ mail) |
| T10 | Cập nhật tồn kho chính xác (100%) | 1 – Điều khiển được; 6 – Ổn định, lặp lại được |
| T11 | Độ chính xác số liệu tổng hợp trên Dashboard (100%) | 1 – Điều khiển được (nạp bộ dữ liệu mẫu đa trạng thái); 3 – Tách biệt được (tách logic tính toán khỏi giao diện biểu đồ) |
| T12 | Thời gian tải biểu đồ (≤ 2s) và xuất tệp báo cáo (≤ 3s) | 1 – Điều khiển được (nạp được tập dữ liệu 5.000 phiếu); 6 – Ổn định, lặp lại được |
| T13 | Tương thích hiển thị Dashboard đa thiết bị và in ấn (100%) | 2 – Quan sát được; 5 – Khả năng tự động hoá (định danh phần tử giao diện bền vững) |

Cuối cùng, nhóm quy ước danh sách kiểm tra (checklist) để đánh giá một phần tăng trưởng có đạt tiêu chuẩn Kiểm thử được hay không trước khi chuyển sang pha kiểm thử P5. Phần tăng trưởng chỉ được chấp nhận khi toàn bộ các mục trong danh sách đều được xác nhận Đạt.

| Mã | Nội dung kiểm tra | Kết quả |
| :---: | ----- | ----- |
| TB.01 | Có bộ dữ liệu mẫu nạp được bằng một lệnh, phủ đủ các vai trò và trạng thái phiếu | Đạt / Không đạt |
| TB.02 | Thời gian hệ thống giả lập được; tác vụ theo lịch kích hoạt thủ công được | Đạt / Không đạt |
| TB.03 | Mọi API trả về mã trạng thái và thông báo lỗi đúng ngữ nghĩa | Đạt / Không đạt |
| TB.04 | Có nhật ký sự kiện và màn hình lịch sử trạng thái phiếu bảo hành | Đạt / Không đạt |
| TB.05 | Dịch vụ email và đồng hồ hệ thống thay thế được bằng đối tượng giả lập | Đạt / Không đạt |
| TB.06 | Mỗi yêu cầu trong SRS có mã định danh và kết quả mong đợi phán định được | Đạt / Không đạt |
| TB.07 | Các phần tử giao diện chính có định danh cố định phục vụ kiểm thử tự động | Đạt / Không đạt |
| TB.08 | Môi trường kiểm thử dựng lại được bằng Docker, tách biệt dữ liệu thật | Đạt / Không đạt |
| TB.09 | Có ma trận truy vết yêu cầu – ca kiểm thử (RTM) | Đạt / Không đạt |
| TB.10 | Phiên bản mã nguồn đưa vào kiểm thử đã được gắn nhãn trên Git | Đạt / Không đạt |
| TB.11 | Nạp được tập dữ liệu quy mô lớn (5.000 phiếu) phục vụ đo hiệu năng Dashboard | Đạt / Không đạt |
| TB.12 | Logic tính toán số liệu thống kê kiểm chứng được độc lập với giao diện biểu đồ | Đạt / Không đạt |

## **CHƯƠNG 3\. XÁC ĐỊNH YÊU CẦU**

1. ### Vai trò của việc Xác định yêu cầu đối với dự án phần mềm

2. ### Phương pháp đánh giá chất lượng của yêu cầu

3. ### Danh sách các yêu cầu của hệ thống

4. ### Kết quả đánh giá chất lượng các yêu cầu

## **CHƯƠNG 4\. KIẾN TRÚC PHẦN MỀM**

1. ### Vai trò của kiến trúc phần mềm với quá trình phát triển dự án phần mềm

   2. ### Một số kiến trúc phần mềm phổ biến 

   3. ### Kiến trúc tổng thể của hệ thống

   4. ### Lựa chọn công nghệ phát triển cho hệ thống

   5. ### Kiến trúc phần mềm của hệ thống

   6. ### Cơ sở dữ liệu mức vật lý của hệ thống

   7. ### Một số thiết kế chi tiết theo kiến trúc được chọn

## 

## **CHƯƠNG 5\. XÂY DỰNG VÀ KIỂM THỬ HỆ THỐNG**

*Lựa chọn xây dựng và kiểm thử các chức năng đáp ứng cho ít nhất 20% yêu cầu quan trọng nhất của hệ thống và phải chỉ rõ Ai-làm gì tương ứng với chương này trong bảng phân công* 

1. ### Kết quả xây dựng module/nhóm chức năng

   1. ….  
      2. ….

   2. ### Kiểm thử hệ thống

      1. Tổng quan về kiểm thử phần mềm  
         1. ….  
         2. ….  
      2. Mô hình kiểm thử được áp dụng trong đề tài  
      3. Kế hoạch kiểm thử  
      4. Kết quả kiểm thử

## 

## **CHƯƠNG 6\. KẾT LUẬN**

1. ### Đánh giá chất lượng phần mềm

2. ### Ưu điểm & Nhược điểm của đề tài

3. ### Hướng phát triển

   ….

## **TÀI LIỆU THAM KHẢO**

## **PHỤ LỤC A: QUY TẮC ĐẶT TÊN**

## **PHỤ LỤC B: CÁC BIỂU MẪU, TÀI LIỆU THU THẬP ĐƯỢC**

## **PHỤ LỤC C: CÁC BIÊN BẢN TIẾN ĐỘ**

## **PHỤ LỤC D: CÁC BIÊN BẢN RÀ SOÁT KỸ THUẬT**

## **PHỤ LỤC E: HỒ SƠ TOÀN BỘ DỰ ÁN**

1. Hồ sơ khảo sát  
2. Hồ sơ phân tích  
3. Hồ sơ thiết kế  
4. Mã nguồn  
5. Hồ sơ kiểm thử

## **PHỤ LỤC Z: NHẬT KÝ SỬ DỤNG AI**

*(Nhật ký phải thể hiện trung thực, rõ ràng, khách quan về quá trình sử dụng AI và vai trò, trách nhiệm của người sử dụng trong việc tuân thủ các quy tắc AUR.xx đã nói ở Mục Quy tắc sử dụng công cụ AI hỗ trợ trong dự án (tại Chương 1); Trình bày thành các mục có đánh STT (numbering).*   
*Trong các chương phía trên, mỗi sản phẩm có liên quan đến mục nào trong phụ lục này phải được ghi chú tại nơi trình bày sản phẩm đó bằng footnote dẫn chiếu tới mục tương ứng trong phụ lục này*)  
…