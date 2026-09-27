from vitts.bench.metrics import canonicalize, edit_distance, score


def test_canonicalize_merges_regional_variants():
    assert canonicalize("Một NGÀN lẻ năm, hai mươi bốn!") == "một nghìn linh năm hai mươi tư"
    assert canonicalize("hoà") == canonicalize("hòa")


def test_edit_distance():
    assert edit_distance("a b c".split(), "a x c".split()) == 1
    assert edit_distance([], "a b".split()) == 2


def test_score_picks_closest_reference():
    assert score("năm triệu mỗi tháng", ["năm triệu một tháng", "năm triệu mỗi tháng"]) == (0, 4)
    assert score("năm triệu tháng", ["năm triệu một tháng"]) == (1, 4)
