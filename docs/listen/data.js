window.BENCH = {
 "reference": {
  "src": "audio/reference.mp3",
  "seconds": 8.05,
  "text": "xin chào việt nam, giá một trăm ngàn, giao lúc bốn giờ ba mươi phút ngày hai tháng chín tại thành phố hồ chí minh.",
  "utmos": 1.8201637268066406
 },
 "samples": [
  {
   "id": "short-06",
   "note": "Câu ngắn: viXTTS thêm từ thừa, VietTTS bỏ mất từ đầu",
   "category": "short",
   "text": "chúc mừng năm mới."
  },
  {
   "id": "short-09",
   "note": "Câu ngắn: MMS và Piper đọc nhầm một từ",
   "category": "short",
   "text": "con mèo đang ngủ."
  },
  {
   "id": "medium-01",
   "note": "Câu thường, có địa danh",
   "category": "medium",
   "text": "hà nội là thủ đô của việt nam, nổi tiếng với phố cổ và hồ hoàn kiếm."
  },
  {
   "id": "medium-06",
   "note": "Câu có số đã được đọc thành chữ",
   "category": "medium",
   "text": "giá xăng hôm nay giảm nhẹ, khoảng hai mươi ba nghìn đồng một lít."
  },
  {
   "id": "long-01",
   "note": "Câu dài: bản tin thời tiết",
   "category": "long",
   "text": "theo dự báo của trung tâm khí tượng thủy văn quốc gia, trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác, nhiệt độ thấp nhất từ hai mươi hai đến hai mươi bốn độ, người dân cần chú ý đề phòng lốc sét và gió giật mạnh."
  },
  {
   "id": "tones-05",
   "note": "Líu lưỡi: vần khó khuya, khoắt, khuỷu",
   "category": "tones",
   "text": "khuya khoắt, khuỷu tay khuơ khoắng chiếc khuy nhỏ."
  },
  {
   "id": "tones-07",
   "note": "Líu lưỡi: ngoằn ngoèo, nghoe nguẩy",
   "category": "tones",
   "text": "ngoằn ngoèo nghoe nguẩy, nghiêng ngả nghênh ngang."
  },
  {
   "id": "names-02",
   "note": "Địa danh Tây Nguyên, có từ mượn Pleiku",
   "category": "names",
   "text": "tôi đã từng đến buôn ma thuột, pleiku và kon tum."
  }
 ],
 "engines": [
  {
   "id": "indextts2",
   "name": "IndexTTS-2 Vietnamese",
   "repo": "dinhthuan/index-tts-2-vietnamese",
   "license": "Apache-2.0 (dùng thương mại cần phép của IndexTTS)",
   "wer": 0.018137847642079808,
   "utmos": 1.9878578758239747,
   "sim": 0.7408178436756134,
   "rtf": 1.0626428492748954,
   "vram": 8.943232512,
   "sample_rate": 22050,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/indextts2/short-06.mp3",
     "seconds": 1.83,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 2.0613582134246826,
     "sim": 0.6665341854095459,
     "runaway": false
    },
    "short-09": {
     "src": "audio/indextts2/short-09.mp3",
     "seconds": 1.45,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 2.4797255992889404,
     "sim": 0.5886591076850891,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/indextts2/medium-01.mp3",
     "seconds": 4.75,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 2.3118176460266113,
     "sim": 0.7422548532485962,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/indextts2/medium-06.mp3",
     "seconds": 3.81,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 1.9309941530227661,
     "sim": 0.7852751016616821,
     "runaway": false
    },
    "long-01": {
     "src": "audio/indextts2/long-01.mp3",
     "seconds": 17.12,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 1.7211633920669556,
     "sim": 0.8516219258308411,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/indextts2/tones-05.mp3",
     "seconds": 4.59,
     "asr": "khuya khoắt khuều tay khơ khoắn chiếc khuya nhỏ",
     "wer": 0.4444444444444444,
     "utmos": 2.433713436126709,
     "sim": 0.6270648241043091,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/indextts2/tones-07.mp3",
     "seconds": 4.03,
     "asr": "ngoằn ngoèo ngoe nguẩy nghiêng ngả nghênh ngang",
     "wer": 0.125,
     "utmos": 1.924863338470459,
     "sim": 0.6927886605262756,
     "runaway": false
    },
    "names-02": {
     "src": "audio/indextts2/names-02.mp3",
     "seconds": 3.34,
     "asr": "tôi đã từng đến buôn ma thuột pleiku và con tôm",
     "wer": 0.18181818181818182,
     "utmos": 1.9971544742584229,
     "sim": 0.5942647457122803,
     "runaway": false
    }
   }
  },
  {
   "id": "f5",
   "name": "F5-TTS-Vietnamese-1000h",
   "repo": "hynt/F5-TTS-Vietnamese-ViVoice",
   "license": "CC-BY-NC-SA-4.0",
   "wer": 0.030229746070133012,
   "utmos": 2.2113364124298096,
   "sim": 0.7310880815982819,
   "rtf": 0.21923457316593084,
   "vram": 0.82280448,
   "sample_rate": 24000,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/f5/short-06.mp3",
     "seconds": 1.31,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 2.146190643310547,
     "sim": 0.5278970003128052,
     "runaway": false
    },
    "short-09": {
     "src": "audio/f5/short-09.mp3",
     "seconds": 1.14,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 2.2928898334503174,
     "sim": 0.515148937702179,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/f5/medium-01.mp3",
     "seconds": 5.28,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 2.3374831676483154,
     "sim": 0.7092769742012024,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/f5/medium-06.mp3",
     "seconds": 4.57,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 2.3862221240997314,
     "sim": 0.7835620045661926,
     "runaway": false
    },
    "long-01": {
     "src": "audio/f5/long-01.mp3",
     "seconds": 16.99,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 2.0119261741638184,
     "sim": 0.8795360326766968,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/f5/tones-05.mp3",
     "seconds": 3.35,
     "asr": "khuya khoác khuỷu tay khô khoắn chiếc khuya nhỏ",
     "wer": 0.4444444444444444,
     "utmos": 2.324843645095825,
     "sim": 0.5708325505256653,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/f5/tones-07.mp3",
     "seconds": 3.24,
     "asr": "nguồn ngoèo quan ngủy nghiêng ngả nghênh ngang",
     "wer": 0.375,
     "utmos": 1.6140629053115845,
     "sim": 0.6337146759033203,
     "runaway": false
    },
    "names-02": {
     "src": "audio/f5/names-02.mp3",
     "seconds": 3.35,
     "asr": "tôi đã từng đến buôn ma thuột li cô và con tôm",
     "wer": 0.36363636363636365,
     "utmos": 2.1314218044281006,
     "sim": 0.7111822366714478,
     "runaway": false
    }
   }
  },
  {
   "id": "vieneu",
   "name": "VieNeu-TTS v3 Turbo",
   "repo": "pnnbao-ump/VieNeu-TTS-v3-Turbo",
   "license": "Apache-2.0",
   "wer": 0.032648125755743655,
   "utmos": 2.160719952583313,
   "sim": 0.6560919404029846,
   "rtf": 0.10081383240235559,
   "vram": 0.9358208,
   "sample_rate": 48000,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/vieneu/short-06.mp3",
     "seconds": 1.2,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 2.3959929943084717,
     "sim": 0.5526690483093262,
     "runaway": false
    },
    "short-09": {
     "src": "audio/vieneu/short-09.mp3",
     "seconds": 1.28,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 2.5020945072174072,
     "sim": 0.6443175077438354,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/vieneu/medium-01.mp3",
     "seconds": 4.88,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 2.206247329711914,
     "sim": 0.7067559361457825,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/vieneu/medium-06.mp3",
     "seconds": 3.84,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 2.354459524154663,
     "sim": 0.7120287418365479,
     "runaway": false
    },
    "long-01": {
     "src": "audio/vieneu/long-01.mp3",
     "seconds": 14.56,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 1.8300743103027344,
     "sim": 0.8399697542190552,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/vieneu/tones-05.mp3",
     "seconds": 3.04,
     "asr": "huyền khoác khuỷu tay khô khoáng chiếc khuy nhỏ",
     "wer": 0.4444444444444444,
     "utmos": 2.0405097007751465,
     "sim": 0.5169557332992554,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/vieneu/tones-07.mp3",
     "seconds": 3.28,
     "asr": "ngoằn ngoèo angel nguyễn nghiêng ngả nghiêng ngang",
     "wer": 0.375,
     "utmos": 2.2160768508911133,
     "sim": 0.4837108254432678,
     "runaway": false
    },
    "names-02": {
     "src": "audio/vieneu/names-02.mp3",
     "seconds": 3.36,
     "asr": "tôi đã từng đến buôn ma thuột pleiku và kon tum",
     "wer": 0.0,
     "utmos": 2.395695447921753,
     "sim": 0.6464365720748901,
     "runaway": false
    }
   }
  },
  {
   "id": "piper",
   "name": "Piper vi_VN-vais1000-medium",
   "repo": "rhasspy/piper-voices",
   "license": "CC-BY-4.0 (dữ liệu VAIS-1000)",
   "wer": 0.056831922611850064,
   "utmos": 2.366454734802246,
   "sim": 0.19840428814291955,
   "rtf": 0.037332022216230984,
   "vram": null,
   "sample_rate": 22050,
   "runaway": 0,
   "clones_voice": false,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/piper/short-06.mp3",
     "seconds": 0.75,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 2.5883090496063232,
     "sim": 0.17743021249771118,
     "runaway": false
    },
    "short-09": {
     "src": "audio/piper/short-09.mp3",
     "seconds": 0.8,
     "asr": "con mèo đang mù",
     "wer": 0.25,
     "utmos": 2.67024564743042,
     "sim": 0.2686913013458252,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/piper/medium-01.mp3",
     "seconds": 3.87,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 2.317746639251709,
     "sim": 0.17860575020313263,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/piper/medium-06.mp3",
     "seconds": 2.89,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 2.822802782058716,
     "sim": 0.1500062644481659,
     "runaway": false
    },
    "long-01": {
     "src": "audio/piper/long-01.mp3",
     "seconds": 11.39,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 1.7764911651611328,
     "sim": 0.18951094150543213,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/piper/tones-05.mp3",
     "seconds": 1.92,
     "asr": "khi gót khuỷu tay khuất khoắng chiếc khuy nọ",
     "wer": 0.4444444444444444,
     "utmos": 2.8641974925994873,
     "sim": 0.12001626938581467,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/piper/tones-07.mp3",
     "seconds": 1.66,
     "asr": "hôn ngầu hoa nguội miếng má lấy láng",
     "wer": 1.0,
     "utmos": 2.2731637954711914,
     "sim": 0.2360849380493164,
     "runaway": false
    },
    "names-02": {
     "src": "audio/piper/names-02.mp3",
     "seconds": 2.54,
     "asr": "tôi đã từng đến buôn ma thuột lê cụ và con tum",
     "wer": 0.2727272727272727,
     "utmos": 2.171764373779297,
     "sim": 0.15961956977844238,
     "runaway": false
    }
   }
  },
  {
   "id": "mms",
   "name": "MMS-TTS (Meta)",
   "repo": "facebook/mms-tts-vie",
   "license": "CC-BY-NC-4.0",
   "wer": 0.06892382103990327,
   "utmos": 2.7383735513687135,
   "sim": 0.3182960841059685,
   "rtf": 0.012800193293222578,
   "vram": 0.435067392,
   "sample_rate": 16000,
   "runaway": 0,
   "clones_voice": false,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/mms/short-06.mp3",
     "seconds": 1.71,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 2.4798226356506348,
     "sim": 0.28338000178337097,
     "runaway": false
    },
    "short-09": {
     "src": "audio/mms/short-09.mp3",
     "seconds": 1.71,
     "asr": "con nghẹo đang ngủ",
     "wer": 0.25,
     "utmos": 3.4861621856689453,
     "sim": 0.25304707884788513,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/mms/medium-01.mp3",
     "seconds": 5.76,
     "asr": "cà nôi là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.11764705882352941,
     "utmos": 2.4019694328308105,
     "sim": 0.27069932222366333,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/mms/medium-06.mp3",
     "seconds": 4.5,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một liếc",
     "wer": 0.07142857142857142,
     "utmos": 2.790830135345459,
     "sim": 0.4277123510837555,
     "runaway": false
    },
    "long-01": {
     "src": "audio/mms/long-01.mp3",
     "seconds": 16.85,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chúa đi đề phòng lốc sét và gió giật mạnh",
     "wer": 0.037037037037037035,
     "utmos": 2.3861968517303467,
     "sim": 0.3532889485359192,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/mms/tones-05.mp3",
     "seconds": 3.97,
     "asr": "khuya khoác khuỷu tay khua khoắng chiếc huy nhỏ",
     "wer": 0.3333333333333333,
     "utmos": 3.0925192832946777,
     "sim": 0.15913523733615875,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/mms/tones-07.mp3",
     "seconds": 2.64,
     "asr": "hoàng hoàng hoa mỹ nghiêng ngả nghiêng năng",
     "wer": 0.75,
     "utmos": 2.237384080886841,
     "sim": 0.353463351726532,
     "runaway": false
    },
    "names-02": {
     "src": "audio/mms/names-02.mp3",
     "seconds": 4.21,
     "asr": "tôi đã từng đến buôn ma thuộc lê hú và con tuông",
     "wer": 0.45454545454545453,
     "utmos": 2.3128104209899902,
     "sim": 0.3568999767303467,
     "runaway": false
    }
   }
  },
  {
   "id": "vixtts",
   "name": "viXTTS",
   "repo": "capleaf/viXTTS",
   "license": "CPML (non-commercial)",
   "wer": 0.09189842805320435,
   "utmos": 2.195470199584961,
   "sim": 0.6376812636852265,
   "rtf": 0.20176210504024247,
   "vram": 2.283957248,
   "sample_rate": 24000,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/vixtts/short-06.mp3",
     "seconds": 4.5,
     "asr": "chúc mừng năm mới tốt",
     "wer": 0.25,
     "utmos": 2.012552499771118,
     "sim": 0.6350548267364502,
     "runaway": false
    },
    "short-09": {
     "src": "audio/vixtts/short-09.mp3",
     "seconds": 3.06,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 1.9102656841278076,
     "sim": 0.5475937128067017,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/vixtts/medium-01.mp3",
     "seconds": 6.12,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng vì phố cổ và hồ hoàn kiếm",
     "wer": 0.058823529411764705,
     "utmos": 2.323251962661743,
     "sim": 0.634489893913269,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/vixtts/medium-06.mp3",
     "seconds": 4.82,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 2.1115777492523193,
     "sim": 0.6708078980445862,
     "runaway": false
    },
    "long-01": {
     "src": "audio/vixtts/long-01.mp3",
     "seconds": 13.23,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 2.1726441383361816,
     "sim": 0.7068043947219849,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/vixtts/tones-05.mp3",
     "seconds": 6.97,
     "asr": "khia vững giã liệt mẹ chelsea quấn chiếc huy nhỏ",
     "wer": 0.8888888888888888,
     "utmos": 2.0365493297576904,
     "sim": 0.6033846735954285,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/vixtts/tones-07.mp3",
     "seconds": 4.82,
     "asr": "nguăn mèo nguy nguẩy nhướng nặng nên ngành",
     "wer": 0.875,
     "utmos": 2.3200225830078125,
     "sim": 0.5334177613258362,
     "runaway": false
    },
    "names-02": {
     "src": "audio/vixtts/names-02.mp3",
     "seconds": 4.92,
     "asr": "tôi đã từng đến myanmar thuộc bryan hill và konton",
     "wer": 0.5454545454545454,
     "utmos": 2.22066593170166,
     "sim": 0.6278520226478577,
     "runaway": false
    }
   }
  },
  {
   "id": "viettts",
   "name": "VietTTS",
   "repo": "dangvansam/viet-tts",
   "license": "CC (model card)",
   "wer": 0.11970979443772672,
   "utmos": 2.3928317475318908,
   "sim": 0.7276192528009414,
   "rtf": 0.3948068726330642,
   "vram": 1.745420288,
   "sample_rate": 22050,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/viettts/short-06.mp3",
     "seconds": 1.39,
     "asr": "mừng năm mới",
     "wer": 0.25,
     "utmos": 1.9626166820526123,
     "sim": 0.562115490436554,
     "runaway": false
    },
    "short-09": {
     "src": "audio/viettts/short-09.mp3",
     "seconds": 1.2,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 2.18390154838562,
     "sim": 0.6105368137359619,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/viettts/medium-01.mp3",
     "seconds": 5.19,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cầu và hồ hoàn kiếm",
     "wer": 0.058823529411764705,
     "utmos": 2.5815112590789795,
     "sim": 0.6801893711090088,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/viettts/medium-06.mp3",
     "seconds": 4.52,
     "asr": "giá sân hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.07142857142857142,
     "utmos": 2.5964951515197754,
     "sim": 0.7824666500091553,
     "runaway": false
    },
    "long-01": {
     "src": "audio/viettts/long-01.mp3",
     "seconds": 15.28,
     "asr": "theo dự báo của trung tâm khí tượng thị văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.018518518518518517,
     "utmos": 2.266751766204834,
     "sim": 0.8194702863693237,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/viettts/tones-05.mp3",
     "seconds": 2.67,
     "asr": "vì khoác khuỷu tay vừa khoáng chứ quy nhỏ",
     "wer": 0.6666666666666666,
     "utmos": 2.4514169692993164,
     "sim": 0.7095547914505005,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/viettts/tones-07.mp3",
     "seconds": 3.11,
     "asr": "ngoan wel nguyễn vũ minh nhã nguyên nhân",
     "wer": 1.0,
     "utmos": 2.5668349266052246,
     "sim": 0.7599387764930725,
     "runaway": false
    },
    "names-02": {
     "src": "audio/viettts/names-02.mp3",
     "seconds": 3.91,
     "asr": "chúng tôi đã từng đến buôn ma thuột pleiku và cùng tung",
     "wer": 0.2727272727272727,
     "utmos": 2.311671733856201,
     "sim": 0.7728708982467651,
     "runaway": false
    }
   }
  }
 ]
};
