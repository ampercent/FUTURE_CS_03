import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# Constants for security configuration
PBKDF2_ITERATIONS = 200_000  # High iteration count to slow down brute-force attacks
KEY_LEN = 32                 # 32 bytes = 256 bits (AES-256)
SALT_FILE = 'salt.bin'       # File to store the random salt unique to this installation

def _ensure_salt():
    """
    Ensures a salt file exists and returns its content.
    If not, generates a new 16-byte random salt and saves it.
    The salt is critical for KDF to prevent rainbow table attacks.
    """
    if not os.path.exists(SALT_FILE):
        with open(SALT_FILE, 'wb') as f:
            f.write(get_random_bytes(16))
    with open(SALT_FILE, 'rb') as f:
        return f.read()

def derive_key_from_password(password: str) -> bytes:
    """
    Derives a cryptographic key from a user password using PBKDF2.
    
    Args:
        password (str): The master password.
        
    Returns:
        bytes: A 32-byte (256-bit) key suitable for AES-GCM.
    """
    salt = _ensure_salt()
    # PBKDF2 stretches the password into a secure key using the salt and many iterations
    key = PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERATIONS)
    return key

def encrypt_bytes(plaintext: bytes, key: bytes) -> bytes:
    """
    Encrypts data using AES in GCM mode (Galois/Counter Mode).
    GCM provides both confidentiality (encryption) and authenticity (integrity check).
    
    Args:
        plaintext (bytes): The raw data to encrypt.
        key (bytes): The 256-bit encryption key.
        
    Returns:
        bytes: A blob containing nonce + tag + ciphertext.
    """
    # Nonce (Number used ONCE) must be unique for every encryption with the same key.
    nonce = get_random_bytes(12) 
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # encrypt_and_digest produces the ciphertext and an authentication tag
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # We simply concatenate them. To decrypt, we'll need to slice them apart.
    return nonce + tag + ciphertext

def decrypt_bytes(blob: bytes, key: bytes) -> bytes:
    """
    Decrypts a data blob encrypted by encrypt_bytes.
    
    Args:
        blob (bytes): The encrypted blob (nonce + tag + ciphertext).
        key (bytes): The 256-bit decryption key.
        
    Returns:
        bytes: The original plaintext.
        
    Raises:
        ValueError: If decryption or integrity check fails.
    """
    # Validation: Ensure blob is large enough to contain nonce (12) + tag (16)
    if len(blob) < 12 + 16:
        raise ValueError('Invalid blob size')
        
    # Extract components based on known sizes
    nonce = blob[:12]
    tag = blob[12:28]      # 16 bytes tag
    ciphertext = blob[28:] # Rest is ciphertext
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # decrypt_and_verify will raise ValueError if the tag doesn't match the ciphertext
    # This ensures the file hasn't been tampered with.
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext
