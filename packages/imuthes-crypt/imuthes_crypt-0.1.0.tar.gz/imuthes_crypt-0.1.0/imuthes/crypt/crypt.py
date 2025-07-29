import pathlib
import sys

if sys.platform == "win32":
    from .win32 import get_machine_user_fernet
else:
    from .linux import get_machine_user_fernet

# from hakisto import Logger
# logger = Logger('imuthes.crypt')

__all__ = ["enigma", "denigma", "read"]


def enigma(value: str) -> bytes:
    """Return ``value`` encrypted for machine and user.

    :param value: String to be encrypted.
    :type value: ``str``
    :returns: Encrypted string.
    :rtype: ``bytes``
    """
    # logger.verbose("Encrypting string")
    return get_machine_user_fernet().encrypt(value.encode())


def denigma(value: bytes) -> str:
    """Return ``value`` decrypted for machine and user.

    :param value: Encrypted string.
    :type value: ``bytes``
    :returns: Decrypted string.
    :rtype: ``str``
    """
    # logger.verbose("Decrypting string")
    # logger.debug(f"{value}")
    return get_machine_user_fernet().decrypt(value).decode()


def read(path: pathlib.Path) -> str:
    # logger.debug(f"Reading file {path}")
    with path.open("rb") as f:
        data = f.read()
        # logger.debug(f"Read {len(data)} bytes.")
        return denigma(data)
