from typing import Optional

import pytest

from blockchain_task.preprocessing.address import standardise_state


@pytest.mark.parametrize(
    "raw_state_string, preprocessed_state_string",
    [
        ("US-IL", "Illinois"),
        ("Delaware", "Delaware"),
        ("Ca", "California"),
        ("arkansas", "Arkansas"),
        ("GGazhbz", None),
        ("Pennelyvenia", "Pennsylvania"),
        ("Los Angeles", "California"),
        (None, None),
    ],
)
def test_standardise_state(
    raw_state_string: Optional[str], preprocessed_state_string: Optional[str]
):
    assert standardise_state(raw_state_string) == preprocessed_state_string
