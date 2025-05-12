from grants.views import parse_budget

def test_empty_input():
    result = parse_budget("")
    assert result == {"details": ""}

def test_total_only():
    input_text = "Total Amount: 1500$"
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$1500.00",
        "details": ""
    }

def test_details_only():
    input_text = """• Flight (round‐trip): approximately $350
• Lodging: $50 per night × 5 nights = $250
• Visa: $0
• Ground Transportation: approximately $100
• Incidentals: approximately $100"""
    result = parse_budget(input_text)
    assert result == {
        "details": "• Flight (round‐trip): approximately $350\n• Lodging: $50 per night × 5 nights = $250\n• Visa: $0\n• Ground Transportation: approximately $100\n• Incidentals: approximately $100"
    }
    assert "total_amount" not in result

def test_total_and_details():
    input_text = """I will need a Total  of :  $891
Fight (round-trip): $831
Lodging -  $60
Visa - I do not need a visa
Ground Transportation - I will cover ground transportation"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$891.00",
        "details": "Fight (round-trip): $831\nLodging -  $60\nVisa - I do not need a visa\nGround Transportation - I will cover ground transportation"
    }

def test_decimal_total():
    input_text = """Total Amount: 2171.52
Flight (round-trip) : 1739$
Lodging - US$38.13 × 4 nights
(US$152.52)
Visa: 0$
Ground Transportation - 80$
miscellaneous- 200$"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$2171.52",
        "details": "Flight (round-trip) : 1739$\nLodging - US$38.13 × 4 nights\n(US$152.52)\nVisa: 0$\nGround Transportation - 80$\nmiscellaneous- 200$"
    }

def test_case_insensitivity():
    input_text = """TOTAL: $500
Item: $100"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$500.00",
        "details": "Item: $100"
    }

def test_extra_whitespace():
    input_text = """\n  Total: $1000  \n\nItem1: $500\n  Item2: $300  \n\n"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$1000.00",
        "details": "Item1: $500\nItem2: $300"
    }

def test_commas_in_total():
    input_text = """Total: 1,500$
Details: Some item"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$1500.00",
        "details": "Details: Some item"
    }

def test_total_line_excluded_from_details():
    input_text = """Line 1: $100
Total Amount: $300
Line 2: $200"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$300.00",
        "details": "Line 1: $100\nLine 2: $200"
    }