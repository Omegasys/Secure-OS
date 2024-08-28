import json
import os
from cryptography.fernet import Fernet
import zlib

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Save the key to a file
def save_key(key, filename='key.key'):
    with open(filename, 'wb') as key_file:
        key_file.write(key)

# Load the key from a file
def load_key(filename='key.key'):
    try:
        with open(filename, 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        raise Exception("Key file not found. Please generate a key.")

# Encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    return encrypted_data

# Decrypt data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data

# Compress data
def compress_data(data):
    return zlib.compress(data)

# Decompress data
def decompress_data(data):
    return zlib.decompress(data)

# Filesystem class
class HyperFS128:
    def __init__(self, root_dir='fs_root'):
        self.root_dir = root_dir
        self.key = generate_key()
        self.metadata_file = os.path.join(root_dir, 'metadata.json')
        self.data_dir = os.path.join(root_dir, 'data')
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.load_key()
        self.load_metadata()

    def load_key(self):
        try:
            self.key = load_key()
        except Exception as e:
            print(f"Error loading key: {e}")
            raise

    def save_key(self):
        save_key(self.key)

    def encrypt_boot(self):
        boot_data = json.dumps(self.metadata).encode()
        encrypted_boot = encrypt_data(boot_data, self.key)
        with open(os.path.join(self.root_dir, 'boot.enc'), 'wb') as file:
            file.write(encrypted_boot)

    def decrypt_boot(self):
        try:
            with open(os.path.join(self.root_dir, 'boot.enc'), 'rb') as file:
                encrypted_boot = file.read()
            boot_data = decrypt_data(encrypted_boot, self.key)
            self.metadata = json.loads(boot_data.decode())
        except FileNotFoundError:
            print("No encrypted boot file found.")
            self.metadata = {}

    def compress_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            compressed_data = compress_data(file_data)
            with open(file_path, 'wb') as file:
                file.write(compressed_data)
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    def decompress_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                compressed_data = file.read()
            file_data = decompress_data(compressed_data)
            with open(file_path, 'wb') as file:
                file.write(file_data)
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    def create_directory(self, path):
        parts = path.strip('/').split('/')
        dir_ref = self.metadata
        for part in parts:
            if part not in dir_ref:
                dir_ref[part] = {}
            dir_ref = dir_ref[part]
        self.save_metadata()

    def create_file(self, path, content):
        parts = path.strip('/').split('/')
        file_name = parts.pop()
        dir_ref = self.metadata
        for part in parts:
            if part not in dir_ref:
                dir_ref[part] = {}
            dir_ref = dir_ref[part]
        dir_ref[file_name] = {'path': os.path.join(self.data_dir, file_name)}
        with open(dir_ref[file_name]['path'], 'wb') as file:
            file.write(content)
        self.save_metadata()

    def read_file(self, path):
        parts = path.strip('/').split('/')
        file_name = parts.pop()
        dir_ref = self.metadata
        for part in parts:
            if part not in dir_ref:
                raise FileNotFoundError(f"Directory not found: {'/'.join(parts)}")
            dir_ref = dir_ref[part]
        if file_name in dir_ref:
            file_path = dir_ref[file_name]['path']
            try:
                with open(file_path, 'rb') as file:
                    return file.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {file_path}")
        else:
            raise FileNotFoundError(f"File not found: {'/'.join(parts)}/{file_name}")

    def list_directory(self, path):
        parts = path.strip('/').split('/')
        dir_ref = self.metadata
        for part in parts:
            if part in dir_ref:
                dir_ref = dir_ref[part]
            else:
                raise FileNotFoundError(f"Directory not found: {'/'.join(parts)}")
        return dir_ref

    def save_metadata(self):
        with open(self.metadata_file, 'w') as file:
            json.dump(self.metadata, file, indent=4)

    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as file:
                    self.metadata = json.load(file)
            except Exception as e:
                print(f"Error loading metadata: {e}")
                self.metadata = {}
        else:
            self.metadata = {}

# Example usage
fs = HyperFS128()
fs.create_directory('/programs/128-bit/shared')
fs.create_file('/programs/128-bit/shared/testfile.txt', b'This is a test file')

# Encrypt and save boot directory
fs.encrypt_boot()

# Clear and decrypt boot directory
fs.metadata = {}
fs.decrypt_boot()

print(fs.list_directory('/programs/128-bit/shared'))

# Example file compression and decompression
file_path = os.path.join(fs.data_dir, 'testfile.txt')
fs.compress_file(file_path)
fs.decompress_file(file_path)
