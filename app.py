import os
from flask import Flask, request, redirect, url_for, send_file, render_template, flash
from werkzeug.utils import secure_filename
from crypto import derive_key_from_password, encrypt_bytes, decrypt_bytes
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Configuration
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MASTER_PASSWORD = os.getenv('FILESTORE_MASTER_PASSWORD')

# Security Check: Ensure master password is set
if not MASTER_PASSWORD:
    raise RuntimeError('Set FILESTORE_MASTER_PASSWORD in environment or .env')

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret key is used for signing session cookies (like flash messages)
app.secret_key = os.urandom(24)

# Derive the AES key once at startup. 
# In a real app with multiple users, you might derive this per-user session.
KEY = derive_key_from_password(MASTER_PASSWORD)

@app.route('/')
def index():
    """List all encrypted files."""
    files = sorted(os.listdir(app.config['UPLOAD_FOLDER']))
    return render_template('list.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle file upload and encryption."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        # SANITIZE: Always sanitize filenames to prevent directory traversal attacks
        filename = secure_filename(f.filename)
        data = f.read()
        
        # ENCRYPT: Encrypt the file content in memory
        encrypted = encrypt_bytes(data, KEY)
        
        # STORAGE: Save with .enc extension
        stored_name = filename + '.enc'
        path = os.path.join(app.config['UPLOAD_FOLDER'], stored_name)
        
        with open(path, 'wb') as out:
            out.write(encrypted)
            
        flash(f'Uploaded and encrypted: {filename}')
        return redirect(url_for('index'))
        
    return render_template('upload.html')

@app.route('/download/<stored_name>')
def download(stored_name):
    """Decrypt and download a file."""
    # SANITIZE again before using in file path
    path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(stored_name))
    
    if not os.path.exists(path):
        flash('File not found')
        return redirect(url_for('index'))
        
    with open(path, 'rb') as f:
        blob = f.read()
        
    try:
        # DECRYPT: Verify integrity and decrypt
        plaintext = decrypt_bytes(blob, KEY)
    except Exception:
        flash('Decryption failed! Password mismatch or file tampering detected.')
        return redirect(url_for('index'))
        
    # Restore original filename (remove .enc)
    orig_name = stored_name[:-4] if stored_name.endswith('.enc') else stored_name
    
    # Send as attachment using in-memory byte stream so we don't save decrypted file to disk
    return send_file(BytesIO(plaintext), as_attachment=True, download_name=orig_name)

if __name__ == '__main__':
    # Anti-Gravity expects apps to listen on 0.0.0.0:8080
    app.run(host='0.0.0.0', port=8080)
