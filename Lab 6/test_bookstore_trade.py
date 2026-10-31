import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration

# Example test case:
def test_single_paperback_good():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_invalid_batches_and_credit_bonus():
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks({}, 5.0)

    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks([], -1.0)


def test_unapproved_and_unknown_format_batches_are_ignored_or_rejected():
    result = process_book_buybacks(
        [
            {"intake_approved": False, "format": "paperback"},
            {"intake_approved": True, "format": "magazine"},
        ],
        0.0,
    )
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_all_supported_formats_conditions_and_store_credit():
    batches = [
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
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result == {"total_payout": 143.75, "status": "COMPLETED"}


def test_missing_pages_are_rejected_without_credit():
    result = process_book_buybacks(
        [
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{"missing_pages": 2}, {"missing_pages": 0}],
            }
        ],
        0.0,
    )
    assert result == {"total_payout": 8.0, "status": "COMPLETED"}


def test_counterfeit_textbook_cancels_remaining_batch_credit():
    result = process_book_buybacks(
        [
            {
                "intake_approved": True,
                "format": "textbook",
                "payout_in_credit": True,
                "books": [
                    {"condition": "good"},
                    {"counterfeit": True},
                    {"condition": "mint"},
                ],
            }
        ],
        10.0,
    )
    assert result == {"total_payout": 10.0, "status": "COMPLETED"}


def test_counterfeit_non_textbook_is_rejected_but_other_books_count():
    result = process_book_buybacks(
        [
            {
                "intake_approved": True,
                "format": "hardcover",
                "books": [{"counterfeit": True}, {"condition": "good"}],
            }
        ],
        0.0,
    )
    assert result == {"total_payout": 15.0, "status": "COMPLETED"}


def test_more_than_four_rejections_require_audit():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 1}] * 5,
        }
    ]
    assert process_book_buybacks(batches, 0.0) == {
        "total_payout": 0.0,
        "status": "AUDIT_REJECTED",
    }


def test_scanner_calibration_empty_calibrated_and_recalibration_paths():
    assert inspect_scanner_calibration([]) == "NO_DATA"
    assert inspect_scanner_calibration([[1, 6, 2, 7, 3], [], [5]]) == "CALIBRATED"
    assert inspect_scanner_calibration([[6, 6]]) == "RECALIBRATE"


def test_scanner_streak_resets_after_a_non_misread():
    assert inspect_scanner_calibration([[6, 2, 7]]) == "CALIBRATED"
