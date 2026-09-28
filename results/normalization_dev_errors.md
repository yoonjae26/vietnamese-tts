## vitts (ours): 0 wrong

| id | input | output | reference |
|---|---|---|---|

## vitts + translit (ours): 0 wrong

| id | input | output | reference |
|---|---|---|---|

## vinorm: 17 wrong

| id | input | output | reference |
|---|---|---|---|
| dev-currency-001 | Giá 100k. | giá một trăm ca | giá một trăm nghìn |
| dev-currency-005 | Chiếc máy có giá $999. | chiếc máy có giá chín trăm chín mươi chín | chiếc máy có giá chín trăm chín mươi chín đô la |
| dev-currency-006 | Chi phí 20 USD. | chi phí hai mươi usd | chi phí hai mươi đô la |
| dev-currency-008 | Quà tặng trị giá 200.000₫. | quà tặng trị giá hai trăm nghìn | quà tặng trị giá hai trăm nghìn đồng |
| dev-currency-010 | Thu nhập 5tr/tháng. | thu nhập năm tr xuyệt tê hát nờ gi | thu nhập năm triệu một tháng |
| dev-phone-005 | Số máy bàn 024.3825.1234. | số máy bàn hai mươi tư phẩy ba nghìn tám trăm hai mươi lăm một nghìn hai trăm ba mươi tư | số máy bàn không hai bốn ba tám hai năm một hai ba bốn |
| dev-range-001 | Từ 5-10 người. | từ năm tháng mười người | từ năm đến mười người |
| dev-range-003 | Giai đoạn 2020-2025. | giai đoạn hai nghìn không trăm hai mươi hai nghìn không trăm hai mươi lăm | giai đoạn hai nghìn không trăm hai mươi đến hai nghìn không trăm hai mươi lăm |
| dev-range-004 | Nhiệt độ 25-30°C. | nhiệt độ hai mươi lăm ba mươi độ xê | nhiệt độ hai mươi lăm đến ba mươi độ xê |
| dev-range-005 | Trẻ em 6-12 tuổi. | trẻ em sáu mười hai tuổi | trẻ em sáu đến mười hai tuổi |
| dev-abbreviation-009 | Hàng hóa, thực phẩm, v.v. | hàng hóa thực phẩm v v | hàng hóa thực phẩm vân vân |
| dev-abbreviation-010 | Cấp CCCD mới. | cấp cccd mới | cấp căn cước công dân mới |
| dev-acronym-001 | Công nghệ AI phát triển. | công nghệ ai phát triển | công nghệ a i phát triển |
| dev-acronym-003 | Kênh VTV1. | kênh vtv một | kênh vê tê vê một |
| dev-acronym-004 | Công ty FPT. | công ty fpt | công ty ép pê tê |
| dev-mixed-001 | Ngày 15/3/2024, giá vàng SJC tăng 1,2 triệu đồng/lượng, lên 80,5 triệu đồng. | ngày mười lăm tháng ba năm hai nghìn không trăm hai mươi tư giá vàng sjc tăng một phẩy hai triệu đồng lượng lên tám mươi phẩy năm triệu đồng | ngày mười lăm tháng ba năm hai nghìn không trăm hai mươi tư giá vàng ét gi xê tăng một phẩy hai triệu đồng một lượng lên tám mươi phẩy năm triệu đồng |
| dev-mixed-007 | Nhiệt độ Hà Nội hôm nay 28-35°C, độ ẩm 80%. | nhiệt độ hà nội hôm nay hai mươi tám ba mươi lăm độ xê độ ẩm tám mươi phần trăm | nhiệt độ hà nội hôm nay hai mươi tám đến ba mươi lăm độ xê độ ẩm tám mươi phần trăm |

## soe-vinorm: 10 wrong

| id | input | output | reference |
|---|---|---|---|
| dev-currency-001 | Giá 100k. | giá một trăm ca | giá một trăm nghìn |
| dev-currency-002 | Vé giá 50.000đ. | vé giá năm mươi nghìn đ | vé giá năm mươi nghìn đồng |
| dev-currency-006 | Chi phí 20 USD. | chi phí hai mươi u ét đê | chi phí hai mươi đô la |
| dev-currency-010 | Thu nhập 5tr/tháng. | thu nhập năm tê rờ trên tháng | thu nhập năm triệu một tháng |
| dev-time-002 | Họp lúc 8:05. | họp lúc tám năm | họp lúc tám giờ năm phút |
| dev-time-005 | Kết thúc lúc 23:59. | kết thúc lúc hai mươi ba năm mươi chín | kết thúc lúc hai mươi ba giờ năm mươi chín phút |
| dev-phone-004 | Liên hệ +84 912 345 678. | liên hệ tám bốn chín một hai ba bốn năm sáu bảy tám | liên hệ cộng tám tư chín một hai ba bốn năm sáu bảy tám |
| dev-range-003 | Giai đoạn 2020-2025. | giai đoạn hai nghìn không trăm hai mươi hai nghìn không trăm hai mươi lăm | giai đoạn hai nghìn không trăm hai mươi đến hai nghìn không trăm hai mươi lăm |
| dev-acronym-001 | Công nghệ AI phát triển. | công nghệ ai phát triển | công nghệ a i phát triển |
| dev-acronym-004 | Công ty FPT. | công ty fpt | công ty ép pê tê |

## vietnormalizer: 34 wrong

| id | input | output | reference |
|---|---|---|---|
| dev-decimal-005 | Tăng trưởng đạt 6,05. | tăng trưởng đạt sáu phẩy năm | tăng trưởng đạt sáu phẩy không năm |
| dev-currency-001 | Giá 100k. | giá 100k | giá một trăm nghìn |
| dev-currency-008 | Quà tặng trị giá 200.000₫. | quà tặng trị giá hai trăm không | quà tặng trị giá hai trăm nghìn đồng |
| dev-currency-009 | Giá xăng 23.450đ/lít. | giá xăng hai mươi ba nghìn bốn trăm năm mươi đồng lít | giá xăng hai mươi ba nghìn bốn trăm năm mươi đồng một lít |
| dev-currency-010 | Thu nhập 5tr/tháng. | thu nhập 5tr tháng | thu nhập năm triệu một tháng |
| dev-unit-005 | Nhiệt độ 36,5°C. | nhiệt độ ba mươi sáu phẩy năm c | nhiệt độ ba mươi sáu phẩy năm độ xê |
| dev-unit-008 | Ổ cứng 512GB. | ổ cứng 512gb | ổ cứng năm trăm mười hai gi ga bai |
| dev-date-001 | Ngày 2/9/1945. | ngày ngày hai tháng chín năm một nghìn chín trăm bốn mươi lăm | ngày hai tháng chín năm một nghìn chín trăm bốn mươi lăm |
| dev-date-006 | Khai giảng 5-9-2024. | khai giảng tháng năm đến tháng chín năm hai nghìn không trăm hai mươi tư | khai giảng ngày năm tháng chín năm hai nghìn không trăm hai mươi tư |
| dev-time-004 | Bắt đầu lúc 9g15. | bắt đầu lúc chín gam | bắt đầu lúc chín giờ mười lăm |
| dev-phone-002 | Tổng đài 1900 1234. | tổng đài một nghìn chín trăm một nghìn hai trăm ba mươi tư | tổng đài một chín không không một hai ba bốn |
| dev-phone-003 | SĐT: 0987 654 321. | sđt chín trăm tám mươi bảy sáu trăm năm mươi tư ba trăm hai mươi mốt | số điện thoại không chín tám bảy sáu năm bốn ba hai một |
| dev-phone-004 | Liên hệ +84 912 345 678. | liên hệ tám mươi tư chín trăm mười hai ba trăm bốn mươi lăm sáu trăm bảy mươi tám | liên hệ cộng tám tư chín một hai ba bốn năm sáu bảy tám |
| dev-phone-005 | Số máy bàn 024.3825.1234. | số máy bàn hai mươi tư ba nghìn tám trăm hai mươi lăm một nghìn hai trăm ba mươi tư | số máy bàn không hai bốn ba tám hai năm một hai ba bốn |
| dev-range-001 | Từ 5-10 người. | từ năm tháng mười người | từ năm đến mười người |
| dev-range-002 | Việt Nam thắng 3-1. | việt nam thắng ba tháng một | việt nam thắng ba một |
| dev-range-004 | Nhiệt độ 25-30°C. | nhiệt độ hai mươi lăm ba mươi độ c | nhiệt độ hai mươi lăm đến ba mươi độ xê |
| dev-range-005 | Trẻ em 6-12 tuổi. | trẻ em sáu tháng mười hai tuổi | trẻ em sáu đến mười hai tuổi |
| dev-abbreviation-002 | Học sinh THPT. | học sinh tê hát pê tê | học sinh trung học phổ thông |
| dev-abbreviation-003 | Tại TP.HCM. | tại tê pê hát xê em | tại thành phố hồ chí minh |
| dev-abbreviation-004 | GS. Ngô Bảo Châu. | gi ét ngô bảo châu | giáo sư ngô bảo châu |
| dev-abbreviation-005 | Liên hệ CSGT. | liên hệ xê ét gi tê | liên hệ cảnh sát giao thông |
| dev-abbreviation-006 | Đóng BHXH đầy đủ. | đóng bê hát ích hát đầy đủ | đóng bảo hiểm xã hội đầy đủ |
| dev-abbreviation-007 | Trường ĐH Bách khoa. | trường đh bách khoa | trường đại học bách khoa |
| dev-abbreviation-008 | TS. Nguyễn Văn An. | tê ét nguyễn văn an | tiến sĩ nguyễn văn an |
| dev-abbreviation-009 | Hàng hóa, thực phẩm, v.v. | hàng hóa thực phẩm v v | hàng hóa thực phẩm vân vân |
| dev-abbreviation-010 | Cấp CCCD mới. | cấp xê xê xê đê mới | cấp căn cước công dân mới |
| dev-acronym-005 | Bệnh COVID-19. | bệnh xê o vê i đê mười chín | bệnh cô vít mười chín |
| dev-mixed-001 | Ngày 15/3/2024, giá vàng SJC tăng 1,2 triệu đồng/lượng, lên 80,5 triệu đồng. | ngày ngày mười lăm tháng ba năm hai nghìn không trăm hai mươi tư giá vàng ét giây xê tăng một phẩy hai triệu đồng lượng lên tám mươi phẩy năm triệu đồng | ngày mười lăm tháng ba năm hai nghìn không trăm hai mươi tư giá vàng ét gi xê tăng một phẩy hai triệu đồng một lượng lên tám mươi phẩy năm triệu đồng |
| dev-mixed-003 | TP.HCM có hơn 9 triệu dân, tăng 2,3% so với năm 2019. | tê pê hát xê em có hơn chín triệu dân tăng hai phẩy ba phần trăm so với năm hai nghìn không trăm mười chín | thành phố hồ chí minh có hơn chín triệu dân tăng hai phẩy ba phần trăm so với năm hai nghìn không trăm mười chín |
| dev-mixed-005 | Gọi 0909 123 456 trước 17h để được giảm 10%. | gọi chín trăm linh chín một trăm hai mươi ba bốn trăm năm mươi sáu trước mười bảy giờ để được giảm mười phần trăm | gọi không chín không chín một hai ba bốn năm sáu trước mười bảy giờ để được giảm mười phần trăm |
| dev-mixed-006 | Học phí năm 2025 là 25.000.000đ/năm. | học phí năm hai nghìn không trăm hai mươi lăm là hai mươi lăm triệu đồng năm | học phí năm hai nghìn không trăm hai mươi lăm là hai mươi lăm triệu đồng một năm |
| dev-mixed-007 | Nhiệt độ Hà Nội hôm nay 28-35°C, độ ẩm 80%. | nhiệt độ hà nội hôm nay hai mươi tám ba mươi lăm độ c độ ẩm tám mươi phần trăm | nhiệt độ hà nội hôm nay hai mươi tám đến ba mươi lăm độ xê độ ẩm tám mươi phần trăm |
| dev-mixed-008 | Theo UBND TP. Hà Nội, 1.200 hộ dân đã nhận hỗ trợ. | theo ủy ban nhân dân tê pê hà nội một nghìn hai trăm hộ dân đã nhận hỗ trợ | theo ủy ban nhân dân thành phố hà nội một nghìn hai trăm hộ dân đã nhận hỗ trợ |

