from app.data.preprocess import preprocess_record


def test_preprocess_trims_and_normalizes():
    record = {
        "external_id": "  abc-123  ",
        "text": "Line 1\r\n\r\n\r\nLine 2   ",
        "language": " English "
    }

    result = preprocess_record(record)

    assert result["external_id"] == "abc-123"
    assert result["text"] == "Line 1\n\nLine 2"
    assert result["language"] == "en"


def test_preprocess_french_alias():
    record = {
        "external_id": "id-1",
        "text": "Bonjour",
        "language": "français"
    }

    result = preprocess_record(record)

    assert result["language"] == "fr"