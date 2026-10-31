import pytest

from bookstore_trade_in import inspect_scanner_calibration, process_book_buybacks


def test_code_single_paperback_good():
    result = process_book_buybacks(
        [{
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        }],
        5.0,
    )
    assert result == {"total_payout": 8.0, "status": "COMPLETED"}


def test_code_invalid_input():
    with pytest.raises(ValueError):
        process_book_buybacks({}, 5.0)
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


def test_code_supported_formats_and_conditions():
    result = process_book_buybacks(
        [
            {
                "intake_approved": True,
                "format": "textbook",
                "payout_in_credit": True,
                "books": [
                    {"condition": "mint"},
                    {"condition": "poor"},
                    {"condition": "good"},
                ],
            },
            {
                "intake_approved": True,
                "format": "hardcover",
                "books": [{"condition": "mint"}, {"condition": "poor"}],
            },
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{"condition": "new-condition"}],
            },
        ],
        5.0,
    )
    assert result == {"total_payout": 143.75, "status": "COMPLETED"}


def test_code_missing_pages_and_counterfeits():
    result = process_book_buybacks(
        [
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{"missing_pages": 2}, {"missing_pages": 0}],
            },
            {
                "intake_approved": True,
                "format": "textbook",
                "payout_in_credit": True,
                "books": [{"condition": "good"}, {"counterfeit": True}],
            },
            {
                "intake_approved": True,
                "format": "hardcover",
                "books": [{"counterfeit": True}, {"condition": "good"}],
            },
        ],
        10.0,
    )
    assert result == {"total_payout": 33.0, "status": "COMPLETED"}


def test_code_audit_zero_credit_and_scanner_results():
    audit = process_book_buybacks(
        [{
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 1}] * 5,
        }],
        0.0,
    )
    assert audit == {"total_payout": 0.0, "status": "AUDIT_REJECTED"}

    zero = process_book_buybacks(
        [{"intake_approved": True, "format": "magazine"}], 0.0
    )
    assert zero == {"total_payout": 0.0, "status": "ZERO_CREDIT"}
    assert inspect_scanner_calibration([]) == "NO_DATA"
    assert inspect_scanner_calibration([[1, 6, 2, 7, 3], [], [5]]) == "CALIBRATED"
    assert inspect_scanner_calibration([[6, 6]]) == "RECALIBRATE"
