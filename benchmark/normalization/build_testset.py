"""Sinh `testset.jsonl` cho benchmark chuẩn hóa văn bản.

Mỗi mục: (category, input, [các cách đọc đúng]). Đáp án được viết tay theo cách đọc
tự nhiên của người Việt, KHÔNG sinh từ output của bất kỳ bộ chuẩn hóa nào.
Khi so sánh, các biến thể vùng miền phổ biến (ngàn/nghìn, lẻ/linh, tỉ/tỷ, ...) được
quy về một dạng, xem `vitts.bench.metrics.canonicalize`.

    python benchmark/normalization/build_testset.py
"""

import json
from pathlib import Path

Y2024 = "hai nghìn không trăm hai mươi tư"

CASES = [
    # ------------------------------------------------------------------ số đếm
    ("number", "Lớp có 21 học sinh.", ["lớp có hai mươi mốt học sinh"]),
    ("number", "Cô ấy 45 tuổi.", ["cô ấy bốn mươi lăm tuổi"]),
    ("number", "Tòa nhà cao 105 tầng.", ["tòa nhà cao một trăm linh năm tầng"]),
    ("number", "Dân số khoảng 2.500.000 người.", ["dân số khoảng hai triệu năm trăm nghìn người"]),
    ("number", "Năm 1945 là năm lịch sử.", ["năm một nghìn chín trăm bốn mươi lăm là năm lịch sử"]),
    ("number", "Có 1.005 người tham gia.", ["có một nghìn không trăm linh năm người tham gia"]),
    ("number", "Trường có 14 phòng học.", ["trường có mười bốn phòng học"]),
    ("number", "Kho chứa 3.000.000.000 lít.", ["kho chứa ba tỷ lít"]),
    ("number", "Anh ấy chạy 10 vòng.", ["anh ấy chạy mười vòng"]),
    ("number", "Cần 310 chữ ký.", ["cần ba trăm mười chữ ký"]),
    ("number", "Một ngày có 24 giờ.", ["một ngày có hai mươi tư giờ"]),
    ("number", "Đội có 11 cầu thủ.", ["đội có mười một cầu thủ"]),
    # ------------------------------------------------------------ số thập phân
    (
        "decimal",
        "Chiều cao 1,75 mét.",
        ["chiều cao một phẩy bảy mươi lăm mét", "chiều cao một phẩy bảy lăm mét", "chiều cao một phẩy bảy năm mét"],
    ),
    ("decimal", "Doanh thu tăng 3,5 lần.", ["doanh thu tăng ba phẩy năm lần"]),
    (
        "decimal",
        "Điểm trung bình là 8,25.",
        [
            "điểm trung bình là tám phẩy hai mươi lăm",
            "điểm trung bình là tám phẩy hai lăm",
            "điểm trung bình là tám phẩy hai năm",
        ],
    ),
    ("decimal", "Lãi suất giảm 0,5 điểm.", ["lãi suất giảm không phẩy năm điểm"]),
    ("decimal", "Tăng trưởng đạt 6,05.", ["tăng trưởng đạt sáu phẩy không năm"]),
    ("decimal", "Giá trị hợp đồng 2,1 tỷ.", ["giá trị hợp đồng hai phẩy một tỷ"]),
    # ------------------------------------------------------------------ tiền tệ
    ("currency", "Giá 100k.", ["giá một trăm nghìn", "giá một trăm nghìn đồng"]),
    ("currency", "Vé giá 50.000đ.", ["vé giá năm mươi nghìn đồng"]),
    ("currency", "Lương 15 triệu đồng.", ["lương mười lăm triệu đồng"]),
    ("currency", "Giá 1.250.000 VNĐ.", ["giá một triệu hai trăm năm mươi nghìn đồng"]),
    ("currency", "Chiếc máy có giá $999.", ["chiếc máy có giá chín trăm chín mươi chín đô la"]),
    ("currency", "Chi phí 20 USD.", ["chi phí hai mươi đô la"]),
    ("currency", "Nợ 5 tỷ đồng.", ["nợ năm tỷ đồng"]),
    ("currency", "Quà tặng trị giá 200.000₫.", ["quà tặng trị giá hai trăm nghìn đồng"]),
    (
        "currency",
        "Giá xăng 23.450đ/lít.",
        [
            "giá xăng hai mươi ba nghìn bốn trăm năm mươi đồng một lít",
            "giá xăng hai mươi ba nghìn bốn trăm năm mươi đồng mỗi lít",
            "giá xăng hai mươi ba nghìn bốn trăm năm mươi đồng trên lít",
        ],
    ),
    (
        "currency",
        "Thu nhập 5tr/tháng.",
        ["thu nhập năm triệu một tháng", "thu nhập năm triệu mỗi tháng", "thu nhập năm triệu trên tháng"],
    ),
    # ---------------------------------------------------------------- phần trăm
    ("percent", "Doanh số tăng 12%.", ["doanh số tăng mười hai phần trăm"]),
    ("percent", "Giảm 0,5%.", ["giảm không phẩy năm phần trăm"]),
    ("percent", "Chiếm 100% cổ phần.", ["chiếm một trăm phần trăm cổ phần"]),
    ("percent", "Tỷ lệ đạt 45,7%.", ["tỷ lệ đạt bốn mươi lăm phẩy bảy phần trăm"]),
    (
        "percent",
        "Lạm phát 3,25 %.",
        [
            "lạm phát ba phẩy hai mươi lăm phần trăm",
            "lạm phát ba phẩy hai lăm phần trăm",
            "lạm phát ba phẩy hai năm phần trăm",
        ],
    ),
    # ------------------------------------------------------------------ đơn vị
    ("unit", "Quãng đường 15km.", ["quãng đường mười lăm ki lô mét", "quãng đường mười lăm cây số"]),
    (
        "unit",
        "Anh ấy nặng 70kg.",
        ["anh ấy nặng bảy mươi ki lô gam", "anh ấy nặng bảy mươi cân", "anh ấy nặng bảy mươi ki lô"],
    ),
    (
        "unit",
        "Tốc độ tối đa 60km/h.",
        [
            "tốc độ tối đa sáu mươi ki lô mét trên giờ",
            "tốc độ tối đa sáu mươi ki lô mét một giờ",
            "tốc độ tối đa sáu mươi ki lô mét mỗi giờ",
            "tốc độ tối đa sáu mươi cây số một giờ",
        ],
    ),
    ("unit", "Diện tích 120m2.", ["diện tích một trăm hai mươi mét vuông"]),
    ("unit", "Nhiệt độ 36,5°C.", ["nhiệt độ ba mươi sáu phẩy năm độ xê", "nhiệt độ ba mươi sáu phẩy năm độ"]),
    ("unit", "Chai nước 500ml.", ["chai nước năm trăm mi li lít"]),
    ("unit", "Cao 180cm.", ["cao một trăm tám mươi xen ti mét"]),
    ("unit", "Ổ cứng 512GB.", ["ổ cứng năm trăm mười hai gi ga bai"]),
    ("unit", "Lượng mưa 50mm.", ["lượng mưa năm mươi mi li mét"]),
    ("unit", "Trang trại rộng 3 ha.", ["trang trại rộng ba héc ta"]),
    # --------------------------------------------------------------- ngày tháng
    ("date", "Ngày 2/9/1945.", ["ngày hai tháng chín năm một nghìn chín trăm bốn mươi lăm"]),
    ("date", "Sinh ngày 15/08/2000.", ["sinh ngày mười lăm tháng tám năm hai nghìn"]),
    (
        "date",
        "Hạn chót là 31/12/2024.",
        [
            f"hạn chót là ngày ba mươi mốt tháng mười hai năm {Y2024}",
            f"hạn chót là ba mươi mốt tháng mười hai năm {Y2024}",
        ],
    ),
    ("date", "Vào tháng 4/2023.", ["vào tháng tư năm hai nghìn không trăm hai mươi ba"]),
    ("date", "Lễ hội diễn ra ngày 10/3.", ["lễ hội diễn ra ngày mười tháng ba"]),
    (
        "date",
        "Khai giảng 5-9-2024.",
        [f"khai giảng ngày năm tháng chín năm {Y2024}", f"khai giảng năm tháng chín năm {Y2024}"],
    ),
    (
        "date",
        "Từ tháng 1/2025.",
        ["từ tháng một năm hai nghìn không trăm hai mươi lăm", "từ tháng giêng năm hai nghìn không trăm hai mươi lăm"],
    ),
    (
        "date",
        "Họp vào 01/06/2026.",
        [
            "họp vào ngày một tháng sáu năm hai nghìn không trăm hai mươi sáu",
            "họp vào một tháng sáu năm hai nghìn không trăm hai mươi sáu",
        ],
    ),
    ("date", "Ngày 20/11 là ngày Nhà giáo.", ["ngày hai mươi tháng mười một là ngày nhà giáo"]),
    # ------------------------------------------------------------------- giờ
    ("time", "Lúc 14h30.", ["lúc mười bốn giờ ba mươi", "lúc mười bốn giờ ba mươi phút"]),
    ("time", "Họp lúc 8:05.", ["họp lúc tám giờ năm phút", "họp lúc tám giờ năm"]),
    ("time", "Mở cửa từ 7h đến 22h.", ["mở cửa từ bảy giờ đến hai mươi hai giờ"]),
    ("time", "Bắt đầu lúc 9g15.", ["bắt đầu lúc chín giờ mười lăm", "bắt đầu lúc chín giờ mười lăm phút"]),
    (
        "time",
        "Kết thúc lúc 23:59.",
        ["kết thúc lúc hai mươi ba giờ năm mươi chín phút", "kết thúc lúc hai mươi ba giờ năm mươi chín"],
    ),
    ("time", "Hẹn 6h sáng mai.", ["hẹn sáu giờ sáng mai"]),
    # ------------------------------------------------------------ số điện thoại
    ("phone", "Gọi 0912345678.", ["gọi không chín một hai ba bốn năm sáu bảy tám"]),
    ("phone", "Tổng đài 1900 1234.", ["tổng đài một chín không không một hai ba bốn"]),
    ("phone", "SĐT: 0987 654 321.", ["số điện thoại không chín tám bảy sáu năm bốn ba hai một"]),
    (
        "phone",
        "Liên hệ +84 912 345 678.",
        [
            "liên hệ cộng tám tư chín một hai ba bốn năm sáu bảy tám",
            "liên hệ cộng tám bốn chín một hai ba bốn năm sáu bảy tám",
        ],
    ),
    ("phone", "Số máy bàn 024.3825.1234.", ["số máy bàn không hai bốn ba tám hai năm một hai ba bốn"]),
    # ------------------------------------------------------------ khoảng, tỉ số
    ("range", "Từ 5-10 người.", ["từ năm đến mười người"]),
    ("range", "Việt Nam thắng 3-1.", ["việt nam thắng ba một"]),
    (
        "range",
        "Giai đoạn 2020-2025.",
        ["giai đoạn hai nghìn không trăm hai mươi đến hai nghìn không trăm hai mươi lăm"],
    ),
    ("range", "Nhiệt độ 25-30°C.", ["nhiệt độ hai mươi lăm đến ba mươi độ xê", "nhiệt độ hai mươi lăm đến ba mươi độ"]),
    ("range", "Trẻ em 6-12 tuổi.", ["trẻ em sáu đến mười hai tuổi"]),
    # ---------------------------------------------------------------- viết tắt
    ("abbreviation", "UBND tỉnh họp.", ["ủy ban nhân dân tỉnh họp"]),
    ("abbreviation", "Học sinh THPT.", ["học sinh trung học phổ thông"]),
    ("abbreviation", "Tại TP.HCM.", ["tại thành phố hồ chí minh"]),
    ("abbreviation", "GS. Ngô Bảo Châu.", ["giáo sư ngô bảo châu"]),
    ("abbreviation", "Liên hệ CSGT.", ["liên hệ cảnh sát giao thông"]),
    ("abbreviation", "Đóng BHXH đầy đủ.", ["đóng bảo hiểm xã hội đầy đủ"]),
    ("abbreviation", "Trường ĐH Bách khoa.", ["trường đại học bách khoa"]),
    ("abbreviation", "TS. Nguyễn Văn An.", ["tiến sĩ nguyễn văn an"]),
    ("abbreviation", "Hàng hóa, thực phẩm, v.v.", ["hàng hóa, thực phẩm, vân vân"]),
    ("abbreviation", "Cấp CCCD mới.", ["cấp căn cước công dân mới"]),
    # --------------------------------------------------------- đánh vần chữ cái
    ("acronym", "Công nghệ AI phát triển.", ["công nghệ a i phát triển", "công nghệ ây ai phát triển"]),
    ("acronym", "Đội U23 Việt Nam.", ["đội u hai mươi ba việt nam"]),
    ("acronym", "Kênh VTV1.", ["kênh vê tê vê một"]),
    ("acronym", "Công ty FPT.", ["công ty ép pê tê"]),
    ("acronym", "Bệnh COVID-19.", ["bệnh cô vít mười chín", "bệnh covid mười chín"]),
    # --------------------------------------- câu thường: không được thay đổi gì
    ("plain", "Hôm nay trời đẹp quá.", ["hôm nay trời đẹp quá"]),
    ("plain", "Tôi yêu Việt Nam.", ["tôi yêu việt nam"]),
    ("plain", "Cô giáo đang giảng bài.", ["cô giáo đang giảng bài"]),
    ("plain", "Mẹ đi chợ mua rau.", ["mẹ đi chợ mua rau"]),
    ("plain", "Anh ấy làm việc rất chăm chỉ.", ["anh ấy làm việc rất chăm chỉ"]),
    ("plain", "Hà Nội là thủ đô của Việt Nam.", ["hà nội là thủ đô của việt nam"]),
    ("plain", "Bạn có khỏe không?", ["bạn có khỏe không"]),
    ("plain", "Mùa thu lá vàng rơi.", ["mùa thu lá vàng rơi"]),
    # ------------------------------------------------- câu thực tế (báo chí)
    (
        "mixed",
        "Ngày 15/3/2024, giá vàng SJC tăng 1,2 triệu đồng/lượng, lên 80,5 triệu đồng.",
        [
            f"ngày mười lăm tháng ba năm {Y2024}, giá vàng ét {j} xê tăng một phẩy hai triệu đồng {per} lượng, "
            "lên tám mươi phẩy năm triệu đồng"
            for per in ("một", "mỗi", "trên")
            for j in ("gi", "di")
        ],
    ),
    (
        "mixed",
        "Lúc 19h30 tối 20/11, U23 Việt Nam thắng 2-0.",
        [
            f"lúc mười chín giờ ba mươi{p} tối {d}hai mươi tháng mười một, u hai mươi ba việt nam thắng hai không"
            for p in ("", " phút")
            for d in ("", "ngày ")
        ],
    ),
    (
        "mixed",
        "TP.HCM có hơn 9 triệu dân, tăng 2,3% so với năm 2019.",
        [
            "thành phố hồ chí minh có hơn chín triệu dân, tăng hai phẩy ba phần trăm so với năm "
            "hai nghìn không trăm mười chín"
        ],
    ),
    (
        "mixed",
        "Xe chạy 120km/h trên cao tốc dài 55km.",
        [
            f"xe chạy một trăm hai mươi ki lô mét {per} giờ trên cao tốc dài năm mươi lăm ki lô mét"
            for per in ("trên", "một", "mỗi")
        ],
    ),
    (
        "mixed",
        "Gọi 0909 123 456 trước 17h để được giảm 10%.",
        ["gọi không chín không chín một hai ba bốn năm sáu trước mười bảy giờ để được giảm mười phần trăm"],
    ),
    (
        "mixed",
        "Học phí năm 2025 là 25.000.000đ/năm.",
        [
            f"học phí năm hai nghìn không trăm hai mươi lăm là hai mươi lăm triệu đồng {per} năm"
            for per in ("một", "mỗi", "trên")
        ],
    ),
    (
        "mixed",
        "Nhiệt độ Hà Nội hôm nay 28-35°C, độ ẩm 80%.",
        [
            "nhiệt độ hà nội hôm nay hai mươi tám đến ba mươi lăm độ xê, độ ẩm tám mươi phần trăm",
            "nhiệt độ hà nội hôm nay hai mươi tám đến ba mươi lăm độ, độ ẩm tám mươi phần trăm",
        ],
    ),
    (
        "mixed",
        "Theo UBND TP. Hà Nội, 1.200 hộ dân đã nhận hỗ trợ.",
        ["theo ủy ban nhân dân thành phố hà nội, một nghìn hai trăm hộ dân đã nhận hỗ trợ"],
    ),
]

# ----------------------------------------------------------------------------
# HELD-OUT: viết SAU khi vitts đã được phát triển trên CASES ở trên, gồm các hiện
# tượng chưa được code riêng. Quy tắc: không sửa vitts dựa trên bộ này. Kết quả
# held-out là con số công bố chính. Khi cần bộ held-out mới, thêm HELDOUT_V2.
# ----------------------------------------------------------------------------
PER = ("một", "mỗi", "trên")

HELDOUT = [
    # số, thứ tự, số La Mã, phân số
    ("number", "Anh ấy về thứ 3.", ["anh ấy về thứ ba"]),
    ("number", "Lần thứ 2 tham dự.", ["lần thứ hai tham dự"]),
    ("number", "Thế kỷ XXI.", ["thế kỷ hai mươi mốt"]),
    ("number", "Chiến tranh thế giới thứ II.", ["chiến tranh thế giới thứ hai"]),
    ("number", "Có 1 triệu 200 nghìn người.", ["có một triệu hai trăm nghìn người"]),
    ("number", "Những năm 90 của thế kỷ trước.", ["những năm chín mươi của thế kỷ trước"]),
    ("number", "Điểm số 9/10.", ["điểm số chín trên mười", "điểm số chín phần mười"]),
    ("number", "Uống 1/2 cốc nước.", ["uống một phần hai cốc nước", "uống một trên hai cốc nước", "uống nửa cốc nước"]),
    ("number", "Nhà số 12A.", ["nhà số mười hai a"]),
    ("number", "Top 10 bài hát.", ["tốp mười bài hát", "top mười bài hát"]),
    ("number", "Cách mạng công nghiệp 4.0.", ["cách mạng công nghiệp bốn chấm không"]),
    ("number", "Có 700.000 lượt xem.", ["có bảy trăm nghìn lượt xem"]),
    ("number", "Khoảng 1.000 - 2.000 người.", ["khoảng một nghìn đến hai nghìn người"]),
    # ngày, giờ
    ("date", "Tháng 12 năm 2023.", ["tháng mười hai năm hai nghìn không trăm hai mươi ba"]),
    ("date", "Ngày 1/1.", ["ngày một tháng một"]),
    ("date", "Sinh năm 2005.", ["sinh năm hai nghìn không trăm linh năm", "sinh năm hai nghìn linh năm"]),
    ("date", "Ngày 30/4/1975.", ["ngày ba mươi tháng tư năm một nghìn chín trăm bảy mươi lăm"]),
    ("date", "Đường 3/2.", ["đường ba tháng hai"]),
    ("time", "Từ 8h đến 17h30.", ["từ tám giờ đến mười bảy giờ ba mươi", "từ tám giờ đến mười bảy giờ ba mươi phút"]),
    ("time", "Chờ 15 phút.", ["chờ mười lăm phút"]),
    (
        "time",
        "Khởi hành 5h45 sáng.",
        ["khởi hành năm giờ bốn mươi lăm sáng", "khởi hành năm giờ bốn mươi lăm phút sáng"],
    ),
    ("time", "Lúc 0h.", ["lúc không giờ"]),
    # đơn vị
    ("unit", "Cao 1m75.", ["cao một mét bảy mươi lăm", "cao một mét bảy lăm"]),
    (
        "unit",
        "Nặng 2,5kg.",
        ["nặng hai phẩy năm ki lô gam", "nặng hai phẩy năm ki lô", "nặng hai phẩy năm cân"],
    ),
    ("unit", "Pin 5000mAh.", ["pin năm nghìn mi li am pe giờ"]),
    ("unit", "Màn hình 6,7 inch.", [f"màn hình sáu phẩy bảy {w}" for w in ("inh", "in", "inch")]),
    ("unit", "Công suất 1.500W.", ["công suất một nghìn năm trăm oát"]),
    (
        "unit",
        "Tốc độ mạng 100Mbps.",
        ["tốc độ mạng một trăm mê ga bít trên giây", "tốc độ mạng một trăm mê ga bít"],
    ),
    ("unit", "Nhiệt độ -5°C.", ["nhiệt độ âm năm độ xê", "nhiệt độ âm năm độ"]),
    # tiền
    ("currency", "Giá 1,5 tỷ đồng.", ["giá một phẩy năm tỷ đồng", "giá một tỷ rưỡi đồng"]),
    ("currency", "Giảm 50k.", ["giảm năm mươi nghìn", "giảm năm mươi nghìn đồng"]),
    ("currency", "Giá 3$.", ["giá ba đô la"]),
    ("currency", "Giá 99.000đ.", ["giá chín mươi chín nghìn đồng"]),
    (
        "currency",
        "Tỷ giá 25.400 VND/USD.",
        [f"tỷ giá hai mươi lăm nghìn bốn trăm đồng {p} đô la" for p in PER],
    ),
    ("percent", "Lãi 7,5%/năm.", [f"lãi bảy phẩy năm phần trăm {p} năm" for p in PER]),
    # điện thoại
    ("phone", "Gọi 113.", ["gọi một một ba"]),
    (
        "phone",
        "Hotline: 0243.123.4567.",
        [f"{h} không hai bốn ba một hai ba bốn năm sáu bảy" for h in ("hotline", "hót lai")],
    ),
    ("phone", "Số 0901.234.567.", ["số không chín không một hai ba bốn năm sáu bảy"]),
    # viết tắt, chữ cái, từ nước ngoài
    ("abbreviation", "Q.1, TP.HCM.", ["quận một, thành phố hồ chí minh"]),
    ("abbreviation", "P. Bến Nghé.", ["phường bến nghé"]),
    ("abbreviation", "Bộ GD&ĐT.", ["bộ giáo dục và đào tạo"]),
    ("abbreviation", "Công an TP. Đà Nẵng.", ["công an thành phố đà nẵng"]),
    ("abbreviation", "Khoa CNTT.", ["khoa công nghệ thông tin"]),
    ("abbreviation", "Căn hộ 3PN.", ["căn hộ ba phòng ngủ"]),
    ("acronym", "Ông Nguyễn Văn B.", ["ông nguyễn văn bê"]),
    ("acronym", "Tổ chức NATO.", ["tổ chức na tô"]),
    ("acronym", "Hệ thống ATM.", ["hệ thống a tê em mờ", "hệ thống a tê em", "hệ thống ây ti em"]),
    ("foreign", "Mua iPhone 15.", ["mua ai phôn mười lăm"]),
    ("foreign", "Giải SEA Games 31.", ["giải xi gêm ba mươi mốt"]),
    ("foreign", "Chuẩn IELTS 6.5.", ["chuẩn ai eo sáu chấm năm", "chuẩn ai en ti ét sáu chấm năm"]),
    # câu thường
    ("plain", "Con mèo nằm ngủ trên ghế.", ["con mèo nằm ngủ trên ghế"]),
    ("plain", "Chúng tôi sẽ đi du lịch vào cuối tuần.", ["chúng tôi sẽ đi du lịch vào cuối tuần"]),
    ("plain", "Ông bà tôi sống ở quê.", ["ông bà tôi sống ở quê"]),
    ("plain", "Trời mưa to suốt đêm qua.", ["trời mưa to suốt đêm qua"]),
    # câu thực tế
    (
        "mixed",
        "Sáng 5/10, giá USD tại ngân hàng tăng 20 đồng, lên 24.500 đồng/USD.",
        [
            f"sáng {d}năm tháng mười, giá đô la tại ngân hàng tăng hai mươi đồng, "
            f"lên hai mươi tư nghìn năm trăm đồng {p} đô la"
            for p in PER
            for d in ("", "ngày ")
        ],
    ),
    (
        "mixed",
        "Trận đấu lúc 20h ngày 12/6 kết thúc với tỷ số 1-1.",
        [f"trận đấu lúc hai mươi giờ ngày mười hai tháng sáu kết thúc với tỷ số {s}" for s in ("một một", "một đều")],
    ),
    (
        "mixed",
        "Dự án 2.000 tỷ đồng dài 15,5km dự kiến xong năm 2026.",
        ["dự án hai nghìn tỷ đồng dài mười lăm phẩy năm ki lô mét dự kiến xong năm hai nghìn không trăm hai mươi sáu"],
    ),
    (
        "mixed",
        "Bệnh viện tiếp nhận 30-40 ca/ngày.",
        [f"bệnh viện tiếp nhận ba mươi đến bốn mươi ca {p} ngày" for p in PER],
    ),
    (
        "mixed",
        "Tại Q.7, giá nhà khoảng 50-60 triệu/m2.",
        [f"tại quận bảy, giá nhà khoảng năm mươi đến sáu mươi triệu {p} mét vuông" for p in PER],
    ),
]

SPLITS = {"dev": ("testset.jsonl", CASES), "heldout": ("testset_heldout.jsonl", HELDOUT)}


def main():
    for split, (filename, cases) in SPLITS.items():
        out = Path(__file__).with_name(filename)
        counters: dict[str, int] = {}
        with out.open("w", encoding="utf-8") as f:
            for category, text, refs in cases:
                counters[category] = counters.get(category, 0) + 1
                item = {
                    "id": f"{split}-{category}-{counters[category]:03d}",
                    "category": category,
                    "input": text,
                    "references": refs,
                }
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"{split}: {len(cases)} mục -> {out}")


if __name__ == "__main__":
    main()
