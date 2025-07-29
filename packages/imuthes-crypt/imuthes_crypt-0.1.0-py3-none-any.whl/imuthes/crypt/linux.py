import base64
import getpass
import hashlib
import os
import pathlib
import uuid

from cryptography.fernet import Fernet

# from hakisto import Logger
# logger = Logger('imuthes.crypt.linux')

__all__ = ["get_machine_user_fernet"]


def ensure_path(file_name: str) -> pathlib.Path:
    p = pathlib.Path.home() / ".local"
    p.mkdir(exist_ok=True, parents=True)
    p = p / file_name
    if not p.exists():
        # logger.info("Creating random id")
        with p.open("w") as f:
            f.write(os.urandom(16).hex())
    return p


path = pathlib.Path("/etc/machine-id")
if not path.exists():
    # logger.warning("Could not find /etc/machine-id")
    path = ensure_path("machine-id")
with path.open() as f:
    __key = uuid.UUID(f.read().strip()).bytes
# logger.debug(f"machine-id: {__key}")

try:
    uid = os.getuid()
except OSError:
    # logger.warning("Issue getting User ID")
    path = ensure_path("user-id")
    with path.open() as f:
        __salt = uuid.UUID(f.read().strip()).bytes
else:
    # logger.debug(f"uid: {uid}")
    login = getpass.getuser()
    # logger.debug(f"login: {login}")
    md5 = hashlib.md5()
    md5.update((login * (uid % (2**16) or 1)).encode())
    __salt = md5.digest()
# logger.debug(f"salt: {__salt}")


def get_machine_user_fernet() -> Fernet:
    """Return Fernet object based on machine and user"""
    return Fernet(base64.urlsafe_b64encode(__key + __salt))
