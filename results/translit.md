# Phiên âm từ nước ngoài: bộ test (1676 từ chưa gặp khi huấn luyện)

| Hệ thống | Tham số | Đúng cả từ ↑ | Lỗi âm tiết (SER) ↓ | Lỗi ký tự (CER) ↓ | ms/từ | VRAM |
|---|---:|---:|---:|---:|---:|---:|
| Giữ nguyên chữ tiếng Anh | – | 0.6% | 99.3% | 54.7% | 0.00 | – |
| vietnormalizer (quy tắc, không tra từ điển) | – | 7.8% | 73.1% | 40.5% | 0.07 | – |
| soe-vinorm | – | 0.5% | 110.5% | 58.6% | 0.05 | – |
| vitts translit (greedy) | 5.6M | 54.2% | 30.7% | 15.4% | 15.80 | 0.1 GB |
| vitts translit (beam 5) | 5.6M | 55.1% | 30.0% | 14.9% | 21.56 | 0.1 GB |
| Qwen2.5-7B-Instruct zero-shot | 7.6B | 3.2% | 95.3% | 59.3% | 6.61 | 16.6 GB |
| Qwen2.5-7B-Instruct few-shot (20 ví dụ từ train) | 7.6B | 4.2% | 95.9% | 58.2% | 22.09 | 20.8 GB |

vitts giải mã từng từ một; LLM sinh theo lô 64 từ trên GPU (ms/từ là thời gian trung bình khi chạy cả bộ).

## Ví dụ (30 từ đầu của bộ test)

| Từ | Đáp án | Giữ nguyên chữ tiếng Anh | vietnormalizer (quy tắc, không tra từ điển) | soe-vinorm | vitts translit (greedy) | vitts translit (beam 5) | Qwen2.5-7B-Instruct zero-shot | Qwen2.5-7B-Instruct few-shot (20 ví dụ từ train) |
|---|---|---|---|---|---|---|---|---|
| aaswath | a oát | aaswath | a xuát | aaswath | át oát | át oát | a s th | a s |
| abuse | a biu | abuse | a bu xe | abuse | a bu xê | a bu xê | abu se | ab us |
| abydos | a bai đốt | abydos | a bi dọt | abydos | a bi đốt | a bi đốt | ab id os | ab i do sô |
| accelerate | ắc xê lơ rết | accelerate | a ke ồ râi | accelerate | ắc xê lê rát | ắc xê lê rát | ác celerete | ác celer ate |
| accton | ác tần | accton | a ton | accton | ắc tơn | ắc tơn | ác tông | ăc tông |
| achalasia | a ca la xi a | achalasia | a cha la xia | achalasia | a cha la xi a | a cha la xi a | achalasis | a xả lả ya |
| acura | a ciu ra | acura | a cu ra | acura | a cu ra | a cu ra | ác úa | ác yura |
| adamson | a đăm xơn | adamson | a dam xon | adamson | a đam xơn | a đam xơn | ad am son | ad am sôn |
| adapt | a đáp | adapt | a dáp | adapt | a đáp | a đáp | adaptdown | ad áp tít |
| adel | a đen | adel | a deo | adel | a đen | a đen | adé | ad el |
| afzalov | áp za lốp | afzalov | áp da lo | afzalov | áp za lốp | áp za lốp | af zal ov | af zâl ô |
| agadir | a ga đi | agadir | a ga dơ | agadir | a ga đia | a ga đia | a gá dê | a ga đê |
| agatha | a ga tha | agatha | a gát ha | agatha | a ga tha | a ga tha | agatha | ag atha |
| agrelo | a grê lô | agrelo | á re lo | agrelo | a grê lô | a grê lô | ag re lo | a gề lo |
| agun | a gun | agun | a gân | agun | a gun | a gun | a gun | a gun |
| ahmedabad | a mê đa bát | ahmedabad | a me da bát | ahmedabad | a mê đa bát | a mê đa bát | a hmed a b d | ah me đà bát |
| ainsley | ain xờ li | ainsley | ain lâi | ainsley | ên xli | ên xli | ains lê | ain s |
| airbus | e bớt | airbus | ai bợt | airbus | e bớt | e bớt | áir bús | ây bù sê |
| aissata | ai xa ta | aissata | ai xa ta | aissata | ai xa ta | ai xa ta | ai sà ta | ai sà ta |
| akhenaten | a khê na tên | akhenaten | a che na ten | akhenaten | ác hê nét tần | ác hê nét tần | a ken a ten | a khen aten |
| akita | a ki ta | akita | a ki ta | akita | a ki ta | a ki ta | ak i ta | aki ta |
| akliouche | a li u chê | akliouche | a liu che | akliouche | a ki lu chê | a ki lu chê | a klio u che | a kl i u che |
| aksyonov | ác xi ô nốp | aksyonov | a xio no | aksyonov | ác xi ô nốp | ác xi ô nốp | aksyônôv | aks yon ô |
| albopictus | an bô pích tút | albopictus | a bo pi tợt | albopictus | an bô pích tút | an bô pích tút | al bo pi cu us | al bo pích tus |
| album | an bum | album | a bâm | album | an bum | an bum | al ba | al buhm |
| alcarez | al ca rét | alcarez | a ca re | alcarez | an ca rét | an ca rét | al ca rez | a la khe |
| alcohol | an cô hôn | alcohol | a co hôn | alcohol | an cô hôn | an cô hôn | al koh lơ | a loh cô |
| alcyoniidae | an xi ô ni i đê | alcyoniidae | a kio ni dae | alcyoniidae | an xi ô ni đê a | an xi ô ni đê a | al ky ô ni đài | al cy ô ni id a |
| alessandra | a lê xan đra | alessandra | a ồ xan ra | alessandra | a lết xan đra | a lết xan đra | ale ssan dra | a le ssa ran đà |
| alexei | a lếch xây | alexei | a ồ xâi | alexei | a lếch xây | a lếch xây | aleksey | al eksi |
