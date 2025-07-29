import re

email_validation_pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"  # noqa: E501


def _extract_all(text: str, pattern: str = email_validation_pattern) -> list:
    """Extract valid emails from texts by regex."""
    return re.findall(pattern, text)


def _extract_one(text: str, pattern: str = email_validation_pattern) -> str:
    """Extract a valid email from texts by regex."""
    valid_list = _extract_all(text=text, pattern=pattern)
    return valid_list[0] if len(valid_list) else ""


extract_email = get_email = get_valid_email = _extract_one
extract_emails = get_emails = extract_valid_emails = get_valid_emails = _extract_all
