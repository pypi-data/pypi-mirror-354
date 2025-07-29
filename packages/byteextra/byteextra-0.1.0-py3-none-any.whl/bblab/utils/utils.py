"""Utility functions for the package."""

import re
import ast
import shutil
import hashlib
from typing import Any
from logging import Logger
from pathlib import Path
from datetime import datetime, timezone, timedelta
from importlib import metadata

import jwt
import pandas as pd

from bblab.utils.logger import get_logger
from bblab.utils.decorator import timed, timed_block

logger: Logger = get_logger(__name__)


def hash_file(path: str) -> str:
    """Get SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def safe_literal_eval(value, fallback=None):
    """Fail eval silently."""
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError) as e:
        print(f"[E] failed to eval `{value}` Error: {e}")
        return fallback


@timed
def get_df_from_csv(path: Path, index_col: Any = None) -> pd.DataFrame:
    """Read a csv file from filesystem and return as a DataFrame."""
    if path.exists() and path.is_file():
        if index_col is None:
            return pd.read_csv(path)
        return pd.read_csv(path, index_col=index_col)
    logger.error("File %s does not exist or is not a valid file.", str(path.absolute()))
    raise FileNotFoundError


@timed
def get_df_from_zip(filepath: Path) -> pd.DataFrame:
    """Read a csv file from filesystem and return as a DataFrame."""
    if filepath.exists() and filepath.is_file():
        return pd.read_csv(filepath)

    logger.error(
        "ZIP File: %s does not exist or is not a valid zip file.", str(filepath.absolute())
    )
    raise FileNotFoundError


@timed
def write_df_to_csv(_df: pd.DataFrame, filepath: Path, index: bool = True) -> None:  # noqa: FBT001, FBT002
    """Read a csv file from filesystem and return as a DataFrame."""
    _df.to_csv(filepath, index=index)
    logger.info("[file] %s saved at: %s", filepath.name, str(filepath.absolute()))


def decode_jwt(token: str, enc_key: str = None, algorithm: str = "HS256"):  # noqa: RUF013
    """Decode the JWT token."""
    try:
        enc_key = enc_key or "SUPER_SECRET_KEY_TO_ENCODE_JWT"
        decoded = jwt.decode(token, enc_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError as e:
        return logger.warning("[JWT] Expired: %s\n[JWT]=%s\n[KEY]=%s", e, token, enc_key)
    except jwt.InvalidTokenError as e:
        return logger.warning("[JWT] Invalid: %s\n[JWT]=%s\n[KEY]=%s", e, token, enc_key)
    else:
        logger.debug("[JWT] [decoded=%s]", decoded)
        return decoded


def generate_jwt(
    payload: dict[str, Any] | None = None,
    key: str = "SUPER_SECRET_KEY_TO_ENCODE_JWT",
    algorithm: str = "HS256",
    exp_minutes: int = 30,
    headers: dict[str, Any] | None = None,
) -> str:
    """Generate JWT token to authenticate the user to the dash apps.

    :type payload: dict[str, Any] | None
    :param key: str - Encryption key
    :param algorithm: str default is `HS256`
    :param exp_minutes: int
    :type headers: dict[str, Any] | None
    :returns str:
    """
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    payload = payload if payload else {"user_id": "dev@local"}
    # noinspection PyTypeChecker
    payload["exp"] = expiration_time
    return jwt.encode(payload=payload, key=key, algorithm=algorithm, headers=headers)


def _is_writable(path: Path) -> bool:
    """Check if the path is writable (directory or existing file)."""
    try:
        if path.is_dir():
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
        elif path.is_file():
            with path.open("a"):
                pass
    except (Exception,):
        return False
    else:
        return True


def _mask_secret(_key: str, _value: str) -> str:
    """Mask sensitive values in environment variables."""
    if re.search(r"secret|key|token|pass|pwd", _key, re.IGNORECASE):
        return "***"
    return _value


try:
    __meta__ = metadata.metadata(__package__ or __name__)
    __version__ = metadata.version(__package__ or __name__) or "0.0.0"
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"
    __meta__ = {}

__project__ = "BitByteLab"
__title____ = "Utils"
__caption__ = "A collection of reusable utilities."
__license__ = __meta__.get("License", "MIT")
__url______ = "https://github.com/bitbytelab/bblab"
__copyright = "2025 BitByteLab"


def banner() -> None:  # noqa: D103
    terminal_size = shutil.get_terminal_size(fallback=(80, 24))
    w = min(terminal_size.columns, 80) - 2
    # fmt: off
    print("\n"
        f"+{'~~~~~~~~~~~~~~~~~~~~~~~~~~~~':{'~'}^{w}}+\n"
        f"│{__title____+' by '+__project__:{' '}^{w}}│\n"
        f"│{'    ' + __caption__ + '     ':{' '}^{w}}│\n"
        f"+{('~' * (len(__caption__) + 2)):{' '}^{w}}+\n"
        f"│{'  Version :  v' + __version__:{' '}^{w}}│\n"
        f"│{'  Copyright © ' + __copyright:{' '}^{w}}│\n"
        f"+{'~~~~~~~~~~~~~~~~~~~~~~~~~~~~':{'~'}^{w}}+\n",
    )
