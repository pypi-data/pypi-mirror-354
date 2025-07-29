import base64
import subprocess
import uuid
import winreg

from cryptography.fernet import Fernet

# from hakisto import Logger
# logger = Logger('imuthes.crypt.win32')


__all__ = ["get_machine_user_fernet"]

__key = uuid.UUID(
    winreg.QueryValueEx(
        winreg.OpenKey(key=winreg.HKEY_LOCAL_MACHINE, sub_key=r"SOFTWARE\\Microsoft\\Cryptography\\"), "MachineGuid"
    )[0]
).bytes
__salt = uuid.UUID(
    int=int(subprocess.check_output("whoami /User").decode().split("\n")[6].split()[1][1:].replace("-", ""))
).bytes


def get_machine_user_fernet() -> Fernet:
    """Return Fernet object based on machine and user"""
    return Fernet(base64.urlsafe_b64encode(__key + __salt))
