# === nanosignfs/signer.py ===

import gnupg
import os
from .config import GPG_KEY_ID

gpg = gnupg.GPG()

def sign_file(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'rb') as f:
        signed_data = gpg.sign_file(f, keyid=GPG_KEY_ID, detach=True)

    sig_path = file_path + ".sig"
    with open(sig_path, 'w') as sig_file:
        sig_file.write(str(signed_data))

    return sig_path

