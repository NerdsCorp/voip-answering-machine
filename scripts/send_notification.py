#!/usr/bin/env python3

import os
import sys
import smtplib
import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from datetime import datetime

def send_email(recording_path, caller_number, caller_name):
    """Send recording via email"""
    
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    email_to = os.getenv('EMAIL_TO')
    
    if not all([smtp_server, smtp_username, smtp_password, email_to]):
        print("Email configuration missing")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email_to
        msg['Subject'] = f"VoIP Voicemail from {caller_name or caller_number}"
        
        # Email body
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"""
New voicemail received:

Caller: {caller_name or 'Unknown'}
Number: {caller_number or 'Unknown'}
Time: {timestamp}

Recording attached.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach recording
        if os.path.exists(recording_path):
            with open(recording_path, 'rb') as f:
                audio = MIMEAudio(f.read(), _subtype='mp3')
                audio.add_header('Content-Disposition', 
                               f'attachment; filename={os.path.basename(recording_path)}')
                msg.attach(audio)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print("Email sent successfully")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_discord(recording_path, caller_number, caller_name):
    """Send notification to Discord"""
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("Discord webhook URL not configured")
        return False
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Discord embed
        embed = {
            "title": "📞 New Voicemail",
            "color": 3447003,  # Blue
            "fields": [
                {
                    "name": "Caller",
                    "value": caller_name or "Unknown",
                    "inline": True
                },
                {
                    "name": "Number", 
                    "value": caller_number or "Unknown",
                    "inline": True
                },
                {
                    "name": "Time",
                    "value": timestamp,
                    "inline": False
                }
            ],
            "footer": {
                "text": "VoIP Answering Machine"
            }
        }
        
        # Send text notification first
        payload = {
            "embeds": [embed]
        }
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            print("Discord notification sent")
            
            # Try to send audio file (Discord has file size limits)
            if os.path.exists(recording_path):
                file_size = os.path.getsize(recording_path)
                if file_size < 8 * 1024 * 1024:  # 8MB limit
                    with open(recording_path, 'rb') as f:
                        files = {'file': f}
                        requests.post(webhook_url, files=files)
                    print("Discord audio file sent")
                else:
                    print("Audio file too large for Discord")
            
            return True
        else:
            print(f"Discord webhook failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")
        return False

def main():
    if len(sys.argv) != 4:
        print("Usage: send_notification.py <recording_path> <caller_number> <caller_name>")
        sys.exit(1)
    
    recording_path = sys.argv[1]
    caller_number = sys.argv[2]
    caller_name = sys.argv[3]
    
    print(f"Processing notification for: {caller_name} ({caller_number})")
    
    # Send to both email and Discord
    email_success = send_email(recording_path, caller_number, caller_name)
    discord_success = send_discord(recording_path, caller_number, caller_name)
    
    if email_success or discord_success:
        print("Notification sent successfully")
    else:
        print("Failed to send notifications")

if __name__ == "__main__":
    main()
