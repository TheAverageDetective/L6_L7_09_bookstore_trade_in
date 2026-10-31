import pytest

from bookstore_trade_in import inspect_scanner_calibration, process_book_buybacks


def test_branch_validation_short_circuit_paths():
    with pytest.raises(ValueError):
        process_book_buybacks({}, 5.0)
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


def test_branch_batch_approval_and_unknown_format():
    result = process_book_buybacks(
        [
            {"intake_approved": False, "format": "paperback"},
            {"intake_approved": True, "format": "magazine"},
        ],
        0.0,
    )
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_branch_formats_conditions_credit_and_completed_status():
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
                "books": [{"condition": "other"}],
            },
        ],
        5.0,
    )
    assert result == {"total_payout": 143.75, "status": "COMPLETED"}


def test_branch_missing_pages_and_counterfeit_paths():
    missing = process_book_buybacks(
        [{
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 2}, {"missing_pages": 0}],
        }],
        0.0,
    )
    assert missing == {"total_payout": 8.0, "status": "COMPLETED"}

    textbook = process_book_buybacks(
        [{
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": True,
            "books": [{"condition": "good"}, {"counterfeit": True}],
        }],
        10.0,
    )
    assert textbook == {"total_payout": 10.0, "status": "COMPLETED"}

    other_format = process_book_buybacks(
        [{
            "intake_approved": True,
            "format": "hardcover",
            "books": [{"counterfeit": True}, {"condition": "good"}],
        }],
        0.0,
    )
    assert other_format == {"total_payout": 15.0, "status": "COMPLETED"}


def test_branch_final_statuses():
    assert process_book_buybacks(
        [{
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 1}] * 5,
        }],
        0.0,
    ) == {"total_payout": 0.0, "status": "AUDIT_REJECTED"}

    assert process_book_buybacks(
        [{"intake_approved": True, "format": "magazine"}], 0.0
    ) == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_branch_scanner_streak_and_reset_paths():
    assert inspect_scanner_calibration([]) == "NO_DATA"
    assert inspect_scanner_calibration([[6, 2, 7]]) == "CALIBRATED"
    assert inspect_scanner_calibration([[6, 6]]) == "RECALIBRATE"
