window.BENCH = {
 "reference": {
  "src": "audio/reference.mp3",
  "seconds": 8.66,
  "utmos": 2.413245677947998
 },
 "samples": [
  {
   "id": "short-06",
   "note": "viXTTS đọc bịa thêm từ ở câu ngắn",
   "category": "short",
   "text": "chúc mừng năm mới."
  },
  {
   "id": "short-09",
   "note": "IndexTTS-2 không dừng, sinh thêm khoảng lặng dài",
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
   "wer": 0.019347037484885126,
   "utmos": 2.7943202543258665,
   "sim": 0.721650043129921,
   "rtf": 0.7803331729185,
   "vram": 8.917745152,
   "sample_rate": 22050,
   "runaway": 5,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/indextts2/short-06.mp3",
     "seconds": 2.84,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 2.6744279861450195,
     "sim": 0.6778954863548279,
     "runaway": false
    },
    "short-09": {
     "src": "audio/indextts2/short-09.mp3",
     "seconds": 29.95,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 2.315720796585083,
     "sim": 0.6127487421035767,
     "runaway": true
    },
    "medium-01": {
     "src": "audio/indextts2/medium-01.mp3",
     "seconds": 5.05,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 2.6770272254943848,
     "sim": 0.7639857530593872,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/indextts2/medium-06.mp3",
     "seconds": 4.31,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 3.0770275592803955,
     "sim": 0.7053129076957703,
     "runaway": false
    },
    "long-01": {
     "src": "audio/indextts2/long-01.mp3",
     "seconds": 14.54,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 2.5496954917907715,
     "sim": 0.8262870907783508,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/indextts2/tones-05.mp3",
     "seconds": 4.47,
     "asr": "khuya khoắt khuỷu tay khơ khoắng chiếc huy nhỏ",
     "wer": 0.2222222222222222,
     "utmos": 2.841404438018799,
     "sim": 0.6465083360671997,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/indextts2/tones-07.mp3",
     "seconds": 29.95,
     "asr": "ngoằn ngoèo ngoai ngoại dây ngã nghênh ngang",
     "wer": 0.5,
     "utmos": 2.40777587890625,
     "sim": 0.4995061457157135,
     "runaway": true
    },
    "names-02": {
     "src": "audio/indextts2/names-02.mp3",
     "seconds": 3.77,
     "asr": "tôi đã từng đến buôn ma thuột lai cu và con tum",
     "wer": 0.2727272727272727,
     "utmos": 2.469266891479492,
     "sim": 0.7281328439712524,
     "runaway": false
    }
   }
  },
  {
   "id": "f5",
   "name": "F5-TTS-Vietnamese-1000h",
   "repo": "hynt/F5-TTS-Vietnamese-ViVoice",
   "license": "CC-BY-NC-SA-4.0",
   "wer": 0.022974607013301087,
   "utmos": 3.1679218721389772,
   "sim": 0.7584820139408112,
   "rtf": 0.27680823020808915,
   "vram": 0.822307328,
   "sample_rate": 24000,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/f5/short-06.mp3",
     "seconds": 0.93,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 2.9347496032714844,
     "sim": 0.6773589253425598,
     "runaway": false
    },
    "short-09": {
     "src": "audio/f5/short-09.mp3",
     "seconds": 0.81,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 3.6695427894592285,
     "sim": 0.6017508506774902,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/f5/medium-01.mp3",
     "seconds": 3.77,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 3.277761936187744,
     "sim": 0.8321752548217773,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/f5/medium-06.mp3",
     "seconds": 3.25,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 3.7640178203582764,
     "sim": 0.7351825833320618,
     "runaway": false
    },
    "long-01": {
     "src": "audio/f5/long-01.mp3",
     "seconds": 12.29,
     "asr": "theo dự báo của trung tâm khí tượng thụy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.018518518518518517,
     "utmos": 2.8038458824157715,
     "sim": 0.8672938942909241,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/f5/tones-05.mp3",
     "seconds": 2.39,
     "asr": "khuya khoắt khuỷu tay khua khoắng chiếc khuya nhỏ",
     "wer": 0.2222222222222222,
     "utmos": 3.2265241146087646,
     "sim": 0.7314271330833435,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/f5/tones-07.mp3",
     "seconds": 2.31,
     "asr": "ngoằn ngoèo nghe nguẩy nghiêng ngả nghênh ngang",
     "wer": 0.125,
     "utmos": 2.6863059997558594,
     "sim": 0.5679741501808167,
     "runaway": false
    },
    "names-02": {
     "src": "audio/f5/names-02.mp3",
     "seconds": 2.39,
     "asr": "tôi đã từng đến buôn ma thuột pleiku và con tôm",
     "wer": 0.18181818181818182,
     "utmos": 3.218627691268921,
     "sim": 0.7399327754974365,
     "runaway": false
    }
   }
  },
  {
   "id": "vieneu",
   "name": "VieNeu-TTS v3 Turbo",
   "repo": "pnnbao-ump/VieNeu-TTS-v3-Turbo",
   "license": "Apache-2.0",
   "wer": 0.02781136638452237,
   "utmos": 2.9829295969009397,
   "sim": 0.7336151301860809,
   "rtf": 0.10098484350090153,
   "vram": 0.91206144,
   "sample_rate": 48000,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/vieneu/short-06.mp3",
     "seconds": 1.12,
     "asr": "chúc ngày năm mới",
     "wer": 0.25,
     "utmos": 2.827664375305176,
     "sim": 0.5624052286148071,
     "runaway": false
    },
    "short-09": {
     "src": "audio/vieneu/short-09.mp3",
     "seconds": 1.2,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 2.9059958457946777,
     "sim": 0.6086251139640808,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/vieneu/medium-01.mp3",
     "seconds": 4.32,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 3.2970986366271973,
     "sim": 0.786780595779419,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/vieneu/medium-06.mp3",
     "seconds": 3.36,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 3.062565803527832,
     "sim": 0.7327278256416321,
     "runaway": false
    },
    "long-01": {
     "src": "audio/vieneu/long-01.mp3",
     "seconds": 13.2,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 2.8005709648132324,
     "sim": 0.8412747979164124,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/vieneu/tones-05.mp3",
     "seconds": 2.64,
     "asr": "huy khoác khuỷu tay khô khoắn chiếc huy nhỏ",
     "wer": 0.5555555555555556,
     "utmos": 3.563990354537964,
     "sim": 0.6967051029205322,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/vieneu/tones-07.mp3",
     "seconds": 2.64,
     "asr": "hoàng mèo angel hồ nguẩy nghiêng ngả nghênh ngang",
     "wer": 0.5,
     "utmos": 2.6514394283294678,
     "sim": 0.6709403991699219,
     "runaway": false
    },
    "names-02": {
     "src": "audio/vieneu/names-02.mp3",
     "seconds": 3.12,
     "asr": "tôi đã từng đến puma thuộc pleiku và quantum",
     "wer": 0.45454545454545453,
     "utmos": 3.1106417179107666,
     "sim": 0.8120834827423096,
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
   "sim": 0.1688626402616501,
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
     "sim": 0.20135338604450226,
     "runaway": false
    },
    "short-09": {
     "src": "audio/piper/short-09.mp3",
     "seconds": 0.8,
     "asr": "con mèo đang mù",
     "wer": 0.25,
     "utmos": 2.67024564743042,
     "sim": 0.0761827751994133,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/piper/medium-01.mp3",
     "seconds": 3.87,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 2.317746639251709,
     "sim": 0.1704559326171875,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/piper/medium-06.mp3",
     "seconds": 2.89,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 2.822802782058716,
     "sim": 0.1598968207836151,
     "runaway": false
    },
    "long-01": {
     "src": "audio/piper/long-01.mp3",
     "seconds": 11.39,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 1.7764911651611328,
     "sim": 0.19908374547958374,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/piper/tones-05.mp3",
     "seconds": 1.92,
     "asr": "khi gót khuỷu tay khuất khoắng chiếc khuy nọ",
     "wer": 0.4444444444444444,
     "utmos": 2.8641974925994873,
     "sim": 0.07923466712236404,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/piper/tones-07.mp3",
     "seconds": 1.66,
     "asr": "hôn ngầu hoa nguội miếng má lấy láng",
     "wer": 1.0,
     "utmos": 2.2731637954711914,
     "sim": 0.13414594531059265,
     "runaway": false
    },
    "names-02": {
     "src": "audio/piper/names-02.mp3",
     "seconds": 2.54,
     "asr": "tôi đã từng đến buôn ma thuột lê cụ và con tum",
     "wer": 0.2727272727272727,
     "utmos": 2.171764373779297,
     "sim": 0.08288653939962387,
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
   "sim": 0.1138310531899333,
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
     "sim": 0.024770231917500496,
     "runaway": false
    },
    "short-09": {
     "src": "audio/mms/short-09.mp3",
     "seconds": 1.71,
     "asr": "con nghẹo đang ngủ",
     "wer": 0.25,
     "utmos": 3.4861621856689453,
     "sim": 0.1684999167919159,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/mms/medium-01.mp3",
     "seconds": 5.76,
     "asr": "cà nôi là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.11764705882352941,
     "utmos": 2.4019694328308105,
     "sim": 0.11243987828493118,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/mms/medium-06.mp3",
     "seconds": 4.5,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một liếc",
     "wer": 0.07142857142857142,
     "utmos": 2.790830135345459,
     "sim": 0.07471585273742676,
     "runaway": false
    },
    "long-01": {
     "src": "audio/mms/long-01.mp3",
     "seconds": 16.85,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chúa đi đề phòng lốc sét và gió giật mạnh",
     "wer": 0.037037037037037035,
     "utmos": 2.3861968517303467,
     "sim": 0.11829924583435059,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/mms/tones-05.mp3",
     "seconds": 3.97,
     "asr": "khuya khoác khuỷu tay khua khoắng chiếc huy nhỏ",
     "wer": 0.3333333333333333,
     "utmos": 3.0925192832946777,
     "sim": 0.06941526383161545,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/mms/tones-07.mp3",
     "seconds": 2.64,
     "asr": "hoàng hoàng hoa mỹ nghiêng ngả nghiêng năng",
     "wer": 0.75,
     "utmos": 2.237384080886841,
     "sim": 0.18130537867546082,
     "runaway": false
    },
    "names-02": {
     "src": "audio/mms/names-02.mp3",
     "seconds": 4.21,
     "asr": "tôi đã từng đến buôn ma thuộc lê hú và con tuông",
     "wer": 0.45454545454545453,
     "utmos": 2.3128104209899902,
     "sim": 0.10298904776573181,
     "runaway": false
    }
   }
  },
  {
   "id": "vixtts",
   "name": "viXTTS",
   "repo": "capleaf/viXTTS",
   "license": "CPML (non-commercial)",
   "wer": 0.094316807738815,
   "utmos": 2.597807936668396,
   "sim": 0.8118814766407013,
   "rtf": 0.1931030738858446,
   "vram": 2.239896064,
   "sample_rate": 24000,
   "runaway": 1,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/vixtts/short-06.mp3",
     "seconds": 3.2,
     "asr": "chúc mừng năm nợ yết hôn thây",
     "wer": 1.0,
     "utmos": 2.6326675415039062,
     "sim": 0.7785186171531677,
     "runaway": false
    },
    "short-09": {
     "src": "audio/vixtts/short-09.mp3",
     "seconds": 4.68,
     "asr": "cameo đặng nhĩ đặng thị ly hận",
     "wer": 1.75,
     "utmos": 2.238816738128662,
     "sim": 0.7921060919761658,
     "runaway": true
    },
    "medium-01": {
     "src": "audio/vixtts/medium-01.mp3",
     "seconds": 4.68,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng với phố cổ và hồ hoàn kiếm",
     "wer": 0.0,
     "utmos": 2.6256184577941895,
     "sim": 0.8270763158798218,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/vixtts/medium-06.mp3",
     "seconds": 3.75,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 2.8433403968811035,
     "sim": 0.8237326741218567,
     "runaway": false
    },
    "long-01": {
     "src": "audio/vixtts/long-01.mp3",
     "seconds": 12.71,
     "asr": "theo dự báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lốc sét và gió giật mạnh",
     "wer": 0.0,
     "utmos": 2.5198633670806885,
     "sim": 0.8523077964782715,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/vixtts/tones-05.mp3",
     "seconds": 3.89,
     "asr": "khuya khách khuỷu tay khờ khẩn chỉ huy nhỏ tê giận",
     "wer": 0.7777777777777778,
     "utmos": 2.19640851020813,
     "sim": 0.8361705541610718,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/vixtts/tones-07.mp3",
     "seconds": 3.38,
     "asr": "mình mèo mây nguẩy nghiêng ngả lênh nan",
     "wer": 0.625,
     "utmos": 2.460329055786133,
     "sim": 0.6935460567474365,
     "runaway": false
    },
    "names-02": {
     "src": "audio/vixtts/names-02.mp3",
     "seconds": 3.75,
     "asr": "tôi đã từng đến buôn ma thuột pleiku và canton",
     "wer": 0.18181818181818182,
     "utmos": 2.9882946014404297,
     "sim": 0.7979289293289185,
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
   "utmos": 3.161082191467285,
   "sim": 0.7662364184856415,
   "rtf": 0.4855298375949031,
   "vram": 1.670685184,
   "sample_rate": 22050,
   "runaway": 0,
   "clones_voice": true,
   "n": 50,
   "clips": {
    "short-06": {
     "src": "audio/viettts/short-06.mp3",
     "seconds": 0.95,
     "asr": "chúc mừng năm mới",
     "wer": 0.0,
     "utmos": 3.3124616146087646,
     "sim": 0.5967290997505188,
     "runaway": false
    },
    "short-09": {
     "src": "audio/viettts/short-09.mp3",
     "seconds": 1.15,
     "asr": "con mèo đang ngủ",
     "wer": 0.0,
     "utmos": 2.9011518955230713,
     "sim": 0.6078625917434692,
     "runaway": false
    },
    "medium-01": {
     "src": "audio/viettts/medium-01.mp3",
     "seconds": 3.6,
     "asr": "hà nội là thủ đô của việt nam nổi tiếng bởi phố cổ và hồ hoàn kiếm",
     "wer": 0.058823529411764705,
     "utmos": 3.0089666843414307,
     "sim": 0.8252942562103271,
     "runaway": false
    },
    "medium-06": {
     "src": "audio/viettts/medium-06.mp3",
     "seconds": 2.95,
     "asr": "giá xăng hôm nay giảm nhẹ khoảng hai mươi ba nghìn đồng một lít",
     "wer": 0.0,
     "utmos": 3.851398468017578,
     "sim": 0.7847014665603638,
     "runaway": false
    },
    "long-01": {
     "src": "audio/viettts/long-01.mp3",
     "seconds": 12.04,
     "asr": "theo triệu báo của trung tâm khí tượng thủy văn quốc gia trong những ngày tới khu vực bắc bộ sẽ có mưa rào và dông rải rác nhiệt độ thấp nhất từ hai mươi hai đến hai mươi tư độ người dân cần chú ý đề phòng lộc rét và gió giật mạnh",
     "wer": 0.05555555555555555,
     "utmos": 3.226926565170288,
     "sim": 0.8343074321746826,
     "runaway": false
    },
    "tones-05": {
     "src": "audio/viettts/tones-05.mp3",
     "seconds": 2.19,
     "asr": "khuyến khích kiểu tày cổ khoáng triệt khi nhỏ",
     "wer": 0.8888888888888888,
     "utmos": 3.2984559535980225,
     "sim": 0.7538892030715942,
     "runaway": false
    },
    "tones-07": {
     "src": "audio/viettts/tones-07.mp3",
     "seconds": 2.08,
     "asr": "muốn quèm với người nhưng ngản inh ngang",
     "wer": 0.875,
     "utmos": 3.225036859512329,
     "sim": 0.6558221578598022,
     "runaway": false
    },
    "names-02": {
     "src": "audio/viettts/names-02.mp3",
     "seconds": 3.0,
     "asr": "tôi đã từng đến buôn ma thuột pleiku và con thươm",
     "wer": 0.18181818181818182,
     "utmos": 3.4267899990081787,
     "sim": 0.7545468807220459,
     "runaway": false
    }
   }
  }
 ]
};
