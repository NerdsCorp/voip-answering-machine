# VoIP Answering Machine

A Docker-based VoIP answering machine using Asterisk that automatically sends voicemail recordings to email and Discord.

## Features

- Asterisk-based VoIP server
- Automatic call answering and recording
- Email notifications with audio attachments
- Discord notifications with optional audio files
- Configurable via environment variables
- Persistent storage for recordings

## Setup

1. Clone this repository
2. Copy `.env.example` to `.env` and configure your settings
3. Build and run: `docker-compose up -d`

## Configuration

### Email Setup
- Use app-specific passwords for Gmail
- Configure SMTP settings in environment variables

### Discord Setup
1. Create a Discord webhook in your server
2. Copy the webhook URL to your environment variables

### SIP Configuration
- Default SIP peer: `answering_machine` 
- Configure your VoIP client to connect to the container IP on port 5060
- Use the credentials defined in `asterisk/sip.conf`

## Usage

1. Configure your VoIP client to connect to the Asterisk server
2. Call extension 100 or let calls go to the default context
3. Leave a voicemail after the beep
4. Recordings will be automatically sent to email and Discord

## File Structure

```
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── asterisk/
│   ├── extensions.conf
│   ├── sip.conf
│   └── modules.conf
├── scripts/
│   ├── process_recording.sh
│   └── send_notification.py
└── README.md
```

## Customization

- Modify `extensions.conf` to change call flow
- Adjust recording length (default: 300 seconds)
- Configure additional SIP peers in `sip.conf`
- Customize notification messages in `send_notification.py`
