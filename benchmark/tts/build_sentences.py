"""Sinh `sentences.jsonl`: bộ câu chung cho mọi model TTS.

Câu đã ở dạng đọc (không còn số, ký hiệu, viết tắt) để đo riêng chất lượng model,
không lẫn lỗi chuẩn hóa văn bản. Mọi model nhận đúng cùng một chuỗi.

    python benchmark/tts/build_sentences.py
"""

import json
from pathlib import Path

SENTENCES = {
    # < 10 từ: nhiều model tạo sinh (XTTS, F5) dễ lỗi ở câu ngắn
    "short": [
        "xin chào các bạn.",
        "hôm nay trời nắng đẹp.",
        "cảm ơn bạn rất nhiều.",
        "tôi đang đi làm.",
        "bạn đã ăn cơm chưa?",
        "chúc mừng năm mới.",
        "mời bạn vào nhà.",
        "đèn đỏ rồi, dừng lại.",
        "con mèo đang ngủ.",
        "hẹn gặp lại ngày mai.",
    ],
    # 10 đến 30 từ
    "medium": [
        "hà nội là thủ đô của việt nam, nổi tiếng với phố cổ và hồ hoàn kiếm.",
        "mỗi sáng tôi thường uống một ly cà phê sữa đá trước khi bắt đầu công việc.",
        "cơn mưa bất chợt khiến dòng người trên phố vội vã tìm chỗ trú.",
        "học sinh cả nước đang chuẩn bị cho kỳ thi tốt nghiệp trung học phổ thông.",
        "bà ngoại kể cho tôi nghe những câu chuyện cổ tích mỗi tối trước khi đi ngủ.",
        "giá xăng hôm nay giảm nhẹ, khoảng hai mươi ba nghìn đồng một lít.",
        "đội tuyển việt nam đã giành chiến thắng với tỷ số hai không trong trận đấu tối qua.",
        "những cánh đồng lúa chín vàng trải dài đến tận chân trời.",
        "ứng dụng này giúp người dùng đặt vé máy bay chỉ trong vài phút.",
        "thành phố hồ chí minh là trung tâm kinh tế lớn nhất cả nước.",
        "các nhà khoa học đang nghiên cứu một loại vắc xin mới phòng bệnh cúm.",
        "cuối tuần này gia đình tôi sẽ về quê thăm ông bà.",
        "vịnh hạ long được công nhận là di sản thiên nhiên thế giới.",
        "anh ấy luyện tập chăm chỉ mỗi ngày để chuẩn bị cho giải chạy ma ra tông.",
        "người dân miền trung đang khắc phục hậu quả của cơn bão số ba.",
    ],
    # > 30 từ: kiểm tra độ ổn định, lặp từ, bỏ từ
    "long": [
        "theo dự báo của trung tâm khí tượng thủy văn quốc gia, trong những ngày tới khu vực bắc bộ sẽ có mưa rào "
        "và dông rải rác, nhiệt độ thấp nhất từ hai mươi hai đến hai mươi bốn độ, người dân cần chú ý đề phòng "
        "lốc sét và gió giật mạnh.",
        "trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc và học tập, từ những trợ lý ảo có thể trả lời câu hỏi "
        "cho đến các hệ thống tự động dịch thuật, tuy nhiên chúng ta cũng cần thận trọng với những rủi ro mà công nghệ "
        "này có thể mang lại.",
        "ngày xửa ngày xưa, ở một ngôi làng nhỏ ven sông, có hai anh em mồ côi sống nương tựa vào nhau, người anh "
        "tham lam còn người em hiền lành chăm chỉ, và câu chuyện của họ đã trở thành bài học cho biết bao thế hệ.",
        "để bảo vệ sức khỏe, các chuyên gia khuyên mỗi người nên ngủ đủ bảy đến tám tiếng mỗi đêm, ăn nhiều rau xanh, "
        "hạn chế đồ ngọt, và dành ít nhất ba mươi phút mỗi ngày để vận động hoặc tập thể dục.",
        "sau hơn hai năm thi công, cây cầu mới bắc qua sông hồng đã chính thức thông xe, giúp rút ngắn thời gian di "
        "chuyển giữa hai bờ và giảm đáng kể tình trạng ùn tắc giao thông vào giờ cao điểm.",
        "khi mùa thu đến, hà nội khoác lên mình một vẻ đẹp dịu dàng, những con phố rợp bóng cây, mùi hoa sữa thoang "
        "thoảng trong gió và những gánh hàng rong bán cốm xanh khiến ai đi xa cũng nhớ.",
        "hội nghị lần này tập trung thảo luận các giải pháp thúc đẩy chuyển đổi số trong giáo dục, y tế và hành chính "
        "công, nhằm nâng cao chất lượng dịch vụ và tạo thuận lợi cho người dân và doanh nghiệp.",
        "nếu bạn đang tìm kiếm một điểm đến yên bình cho kỳ nghỉ, hãy thử ghé thăm những bản làng vùng cao tây bắc, "
        "nơi có ruộng bậc thang tuyệt đẹp, không khí trong lành và những con người mến khách.",
    ],
    # dày đặc thanh điệu dễ nhầm (hỏi / ngã, dấu nặng, vần khó)
    "tones": [
        "bà ba bán bánh bò, bé bi bốn bịch bánh.",
        "mẹ mở mũ mới, mẹ mỉm miệng mừng.",
        "những ngã rẽ nhỏ khiến kẻ lạ dễ lỡ đường.",
        "nồi lẩu nấm nóng nực, nêm nếm nước mắm ngon.",
        "khuya khoắt, khuỷu tay khuơ khoắng chiếc khuy nhỏ.",
        "chuyện chưa chắc chắn, chớ vội chuyển đi.",
        "ngoằn ngoèo nghoe nguẩy, nghiêng ngả nghênh ngang.",
        "quả xoài xanh, quả ổi chín, quả nhãn lồng thơm lừng.",
    ],
    # tên riêng, địa danh, từ mượn đã phiên âm
    "names": [
        "chủ tịch hồ chí minh đọc bản tuyên ngôn độc lập tại quảng trường ba đình.",
        "tôi đã từng đến buôn ma thuột, pleiku và kon tum.",
        "nguyễn du là tác giả của truyện kiều.",
        "chuyến bay từ nội bài đến tân sơn nhất mất khoảng hai tiếng.",
        "anh tuấn và chị hương vừa mở một quán cà phê ở đà lạt.",
        "cô ấy làm việc tại một công ty phần mềm ở cầu giấy.",
        "đội bóng hoàng anh gia lai có nhiều cầu thủ trẻ tài năng.",
        "phở, bánh mì và bún chả là những món ăn nổi tiếng của việt nam.",
        "mùa hè năm ngoái, chúng tôi đi du lịch phú quốc và côn đảo.",
    ],
}


def main():
    out = Path(__file__).with_name("sentences.jsonl")
    n = 0
    with out.open("w", encoding="utf-8") as f:
        for category, items in SENTENCES.items():
            for i, text in enumerate(items, 1):
                f.write(
                    json.dumps({"id": f"{category}-{i:02d}", "category": category, "text": text}, ensure_ascii=False)
                )
                f.write("\n")
                n += 1
    print(f"{n} câu -> {out}")


if __name__ == "__main__":
    main()
