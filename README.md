# Secure File Share (Flask + AES-GCM)

This project is a secure file sharing system built with Flask. All uploaded files are encrypted using AES-256-GCM before being stored on the server. The system ensures confidentiality, integrity, and safe handling of sensitive data during upload, storage, and download.

## Overview

The application allows users to:

* Upload files through a web interface
* Store those files in encrypted form
* Download and decrypt files on demand

Plaintext files are never written to disk. All encryption and decryption occurs in memory.

The project demonstrates secure file handling, modern cryptography practices, and backend web development principles.

## Features

* AES-256-GCM encryption for confidentiality and integrity
* PBKDF2-HMAC-SHA256 key derivation with a unique salt
* Encrypted files stored with a `.enc` extension
* Filename sanitization to prevent path traversal
* Minimal and functional user interface
* Clear separation between cryptographic logic and web routes
* Environment-based key management

## How It Works

1. The user uploads a file through the web interface.
2. The application encrypts the file using AES-GCM and derives the encryption key from a master password.
3. The encrypted data is written to disk in the `uploads/` directory.
4. When a user downloads a file, the system decrypts it in memory and returns the plaintext as a downloadable attachment.
5. If any part of an encrypted file is changed, AES-GCM authentication fails and decryption is rejected.

## Technology Stack

* Python 3
* Flask
* PyCryptodome
* AES-256-GCM encryption
* PBKDF2-HMAC-SHA256 key derivation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/secure-file-share.git
   cd secure-file-share
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set:

   ```
   FILESTORE_MASTER_PASSWORD=YourStrongPassphrase
   UPLOAD_FOLDER=uploads
   ```

   The master password must be kept secure.
   Losing it makes all existing encrypted files unrecoverable.

## Running the Application

Start the server:

```bash
python app.py
```

Open the application in a browser:

```
http://localhost:8080
```

From the interface, you can:

* Upload files for encrypted storage
* Download files, which decrypts them on demand

## Security Summary

* AES-GCM provides authenticated encryption, ensuring both secrecy and tamper detection.
* A unique 12-byte nonce is generated for every encrypted file.
* Keys are derived using PBKDF2 with a 16-byte salt and 200,000 iterations.
* The encryption key is never stored; it is derived in memory at runtime.
* Encrypted files follow this structure:

  ```
  [Nonce (12 bytes)] + [Tag (16 bytes)] + [Ciphertext]
  ```
* Plaintext content is never written to disk.

## Project Structure

```
secure-file-share/
│
├── app.py
├── crypto.py
├── requirements.txt
├── .env.example
├── templates/
│   ├── upload.html
│   └── list.html
└── uploads/     (encrypted files only)
```

## Notes

* This project is intended for educational and internship use.
* For production deployment, further improvements are needed such as HTTPS, proper authentication, audited logging, and a secure key management system.

## License

This project is released under the MIT License.


