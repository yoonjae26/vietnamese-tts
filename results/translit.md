# Phiên âm từ nước ngoài: bộ test (1676 từ chưa gặp khi huấn luyện)

| Hệ thống | Đúng cả từ ↑ | Lỗi âm tiết (SER) ↓ | Lỗi ký tự (CER) ↓ | ms/từ |
|---|---:|---:|---:|---:|
| Giữ nguyên chữ tiếng Anh | 0.6% | 99.3% | 54.7% | 0.00 |
| vietnormalizer (quy tắc, không tra từ điển) | 7.8% | 73.1% | 40.5% | 0.07 |
| soe-vinorm | 0.5% | 110.5% | 58.6% | 0.05 |
| vitts translit (greedy) | 54.2% | 30.7% | 15.4% | 17.70 |
| vitts translit (beam 5) | 55.1% | 30.0% | 14.9% | 23.97 |

## Ví dụ (30 từ đầu của bộ test)

| Từ | Đáp án | Giữ nguyên chữ tiếng Anh | vietnormalizer (quy tắc, không tra từ điển) | soe-vinorm | vitts translit (greedy) | vitts translit (beam 5) |
|---|---|---|---|---|---|---|
| aaswath | a oát | aaswath | a xuát | aaswath | át oát | át oát |
| abuse | a biu | abuse | a bu xe | abuse | a bu xê | a bu xê |
| abydos | a bai đốt | abydos | a bi dọt | abydos | a bi đốt | a bi đốt |
| accelerate | ắc xê lơ rết | accelerate | a ke ồ râi | accelerate | ắc xê lê rát | ắc xê lê rát |
| accton | ác tần | accton | a ton | accton | ắc tơn | ắc tơn |
| achalasia | a ca la xi a | achalasia | a cha la xia | achalasia | a cha la xi a | a cha la xi a |
| acura | a ciu ra | acura | a cu ra | acura | a cu ra | a cu ra |
| adamson | a đăm xơn | adamson | a dam xon | adamson | a đam xơn | a đam xơn |
| adapt | a đáp | adapt | a dáp | adapt | a đáp | a đáp |
| adel | a đen | adel | a deo | adel | a đen | a đen |
| afzalov | áp za lốp | afzalov | áp da lo | afzalov | áp za lốp | áp za lốp |
| agadir | a ga đi | agadir | a ga dơ | agadir | a ga đia | a ga đia |
| agatha | a ga tha | agatha | a gát ha | agatha | a ga tha | a ga tha |
| agrelo | a grê lô | agrelo | á re lo | agrelo | a grê lô | a grê lô |
| agun | a gun | agun | a gân | agun | a gun | a gun |
| ahmedabad | a mê đa bát | ahmedabad | a me da bát | ahmedabad | a mê đa bát | a mê đa bát |
| ainsley | ain xờ li | ainsley | ain lâi | ainsley | ên xli | ên xli |
| airbus | e bớt | airbus | ai bợt | airbus | e bớt | e bớt |
| aissata | ai xa ta | aissata | ai xa ta | aissata | ai xa ta | ai xa ta |
| akhenaten | a khê na tên | akhenaten | a che na ten | akhenaten | ác hê nét tần | ác hê nét tần |
| akita | a ki ta | akita | a ki ta | akita | a ki ta | a ki ta |
| akliouche | a li u chê | akliouche | a liu che | akliouche | a ki lu chê | a ki lu chê |
| aksyonov | ác xi ô nốp | aksyonov | a xio no | aksyonov | ác xi ô nốp | ác xi ô nốp |
| albopictus | an bô pích tút | albopictus | a bo pi tợt | albopictus | an bô pích tút | an bô pích tút |
| album | an bum | album | a bâm | album | an bum | an bum |
| alcarez | al ca rét | alcarez | a ca re | alcarez | an ca rét | an ca rét |
| alcohol | an cô hôn | alcohol | a co hôn | alcohol | an cô hôn | an cô hôn |
| alcyoniidae | an xi ô ni i đê | alcyoniidae | a kio ni dae | alcyoniidae | an xi ô ni đê a | an xi ô ni đê a |
| alessandra | a lê xan đra | alessandra | a ồ xan ra | alessandra | a lết xan đra | a lết xan đra |
| alexei | a lếch xây | alexei | a ồ xâi | alexei | a lếch xây | a lếch xây |
