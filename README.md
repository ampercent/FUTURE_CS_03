
  content: |
    # Secure File Share (Flask + AES)

    A secure file sharing web application built with Flask. All uploaded files are encrypted using AES-256-GCM before being stored on the server. This ensures confidentiality and integrity even if the storage is accessed by an unauthorized party.

    ## Features

    - Server-side file encryption using AES-256-GCM  
    - Authenticated encryption to detect tampering  
    - Key derivation using PBKDF2 with a unique salt and high iteration count  
    - Plaintext files never written to disk  
    - Sanitized filenames to prevent directory traversal  
    - Simple interface for uploading, listing, and downloading files  

    ## Technology Stack

    - Python 3.x  
    - Flask  
    - PyCryptodome  
    - AES-256-GCM  
    - PBKDF2-HMAC-SHA256  

    ## Prerequisites

    - Python 3.8 or higher  
    - pip package manager  

    ## Installation

    1. Clone the repository:
       ```bash
       git clone https://github.com/yourusername/secure-file-share.git
       cd secure-file-share
       ```

    2. Create a virtual environment:
       ```bash
       python -m venv venv

       # Windows
       venv\Scripts\activate

       # macOS/Linux
       source venv/bin/activate
       ```

    3. Install dependencies:
       ```bash
       pip install -r requirements.txt
       ```

    4. Configure environment variables:

       Copy the example environment file:
       ```bash
       cp .env.example .env
       ```

       Edit `.env` and set a strong master password:
       ```
       FILESTORE_MASTER_PASSWORD=YourStrongPassphrase
       UPLOAD_FOLDER=uploads
       ```

       Note: If the master password is lost, encrypted files cannot be recovered.

    ## Usage

    1. Run the application:
       ```bash
       python app.py
       ```

    2. Open the interface:
       ```
       http://localhost:8080
       ```

    3. Upload and download files:
       - Upload using the provided form  
       - Download any stored file to decrypt it  

    ## Security Overview

    - Encryption key derived with PBKDF2 using a 16-byte salt stored in `salt.bin`  
    - AES-256-GCM provides confidentiality and integrity  
    - Each file uses a unique 12-byte nonce  

    File format structure:
    ```
    [Nonce (12 bytes)] + [Authentication Tag (16 bytes)] + [Ciphertext]
    ```

    ## License

    This project is licensed under the MIT License.
