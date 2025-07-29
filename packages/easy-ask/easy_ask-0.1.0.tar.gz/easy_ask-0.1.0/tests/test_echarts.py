from easy_ask import generate_option


def test_line_chart() -> None:
    data = {"labels": ["A"], "values": [1]}
    option = generate_option("line", data)
    assert option["series"][0]["type"] == "line"


def test_pie_chart() -> None:
    data = {"labels": ["A"], "values": [1]}
    option = generate_option("pie", data)
    assert option["series"][0]["type"] == "pie"
