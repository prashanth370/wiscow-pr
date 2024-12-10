import os
import paramiko
from datetime import datetime

# Configuration
SOURCE_DIR = "/path/to/local/directory"  # Replace with the directory to back up
REMOTE_HOST = "your.remote.server.ip"    # Replace with your remote server IP
REMOTE_USER = "username"                 # Replace with your username
REMOTE_PASS = "password"                 # Replace with your password
REMOTE_DIR = "/path/to/remote/directory" # Replace with the remote backup directory

def backup_directory():
    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASS)

        # SCP client for file transfer
        sftp = ssh.open_sftp()

        # Create a remote directory with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(REMOTE_DIR, f"backup_{timestamp}")
        sftp.mkdir(backup_path)

        # Transfer files
        for root, dirs, files in os.walk(SOURCE_DIR):
            remote_path = os.path.join(backup_path, os.path.relpath(root, SOURCE_DIR))
            sftp.mkdir(remote_path)

            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_path, file)
                sftp.put(local_file, remote_file)
                print(f"Transferred: {local_file} -> {remote_file}")

        sftp.close()
        ssh.close()
        print("Backup completed successfully.")
    except Exception as e:
        print(f"Backup failed: {e}")

if __name__ == "__main__":
    backup_directory()
