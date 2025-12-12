---

# Secure File Share (Flask + AES)

A secure file sharing web application built with Flask. All uploaded files are encrypted using AES-256-GCM before being stored on the server. This ensures confidentiality and integrity even if server storage is accessed by an unauthorized party.

## Features

* Server-side encryption using AES-256-GCM.
* Authenticated encryption to detect any modification of stored files.
* Key derivation using PBKDF2 with a unique salt and a high iteration count.
* Files are encrypted and decrypted entirely in memory; plaintext files are never written to disk.
* Filenames are sanitized to prevent directory traversal issues.
* Simple interface for uploading, listing, and downloading files.

## Technology Stack

* Python 3.x
* Flask
* PyCryptodome
* AES-256-GCM encryption
* PBKDF2-HMAC-SHA256 key derivation

## Prerequisites

* Python 3.8 or higher
* pip (Python package installer)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/secure-file-share.git
   cd secure-file-share
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and set a strong master password:

   ```ini
   FILESTORE_MASTER_PASSWORD=YourStrongPassphrase
   UPLOAD_FOLDER=uploads
   ```

   Note: If the master password is lost, encrypted files cannot be recovered.

## Usage

1. **Run the application**

   ```bash
   python app.py
   ```

2. **Open the interface**
   Navigate to:

   ```
   http://localhost:8080
   ```

3. **Upload and download files**

   * Upload a file using the provided form.
   * Download any stored file to decrypt it.

## Security Overview

* The encryption key is derived from the master password using PBKDF2 with a 16-byte salt stored in `salt.bin`.
* AES-256-GCM is used for both confidentiality and authentication.
* Each encrypted file uses a unique, random 12-byte nonce.
* Files are stored in the `uploads/` directory with a `.enc` extension.

File format structure:

```
[Nonce (12 bytes)] + [Authentication Tag (16 bytes)] + [Ciphertext]
```

## Contributing

Contributions are welcome. Submit a pull request if you wish to improve or extend the project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---


