# Phiên âm: bộ test nhiều đáp án do người duyệt (149 từ)

Người duyệt chọn mọi cách đọc chấp nhận được trong các ứng viên đã xáo trộn, không biết ứng viên đến từ hệ thống nào (duyệt mù), và có thể tự gõ thêm. Một output được tính là đúng nếu nằm trong các cách đọc được chấp nhận. Bỏ qua 1 từ đánh dấu không chắc.

| Hệ thống | Đúng ↑ | Lỗi âm tiết ↓ |
|---|---:|---:|
| gpt-4o-mini few-shot | 30.9% | 52.9% |
| gpt-4o-mini zero-shot | 30.2% | 57.9% |
| Đáp án gốc của từ điển vietnormalizer | 27.5% | 57.3% |
| vitts translit (5.6M, beam 5) | 24.8% | 57.8% |
| Qwen2.5-7B-Instruct few-shot | 14.8% | 92.4% |
| vietnormalizer (quy tắc) | 4.0% | 78.1% |
