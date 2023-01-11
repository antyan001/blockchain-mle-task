from typing import Dict, Optional
import pathlib
import re

import yaml

ARTIFACTS_DIR = pathlib.Path(__file__).parent.absolute() / "artifacts"


def read_us_state_clean_mapping() -> Dict:

    with open(ARTIFACTS_DIR / "us_state_codes.yaml", "r") as f:
        us_state_codes = yaml.safe_load(f)

    us_state_codes_prefixed = {f"US-{k}": v for k, v in us_state_codes.items()}

    us_state_upper = {v.upper(): v for _, v in us_state_codes.items()}

    with open(ARTIFACTS_DIR / "us_state_misspellings.yaml", "r") as f:
        us_state_misspellings = yaml.safe_load(f)

    us_state_clean_mapping = dict(
        list(us_state_codes.items())
        + list(us_state_codes_prefixed.items())
        + list(us_state_upper.items())
        + list(us_state_misspellings.items())
    )

    return us_state_clean_mapping


US_STATE_CLEAN_MAPPING = read_us_state_clean_mapping()


def standardise_state(raw_us_state: Optional[str]) -> Optional[str]:
    """
    This method standardises the US state string and corrects misspellings.
    Ideally, however this process should sit in the application layer than here (users shouldn't
    be allowed to enter e.g. Los Angeles in the state field).
    """

    if raw_us_state == None:
        return None

    us_state = re.sub("\s+", " ", raw_us_state).strip().replace(".", "").upper()

    return US_STATE_CLEAN_MAPPING.get(us_state)
