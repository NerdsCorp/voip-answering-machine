#!/bin/bash

RECORDING_FILE="$1"
CALLER_NUMBER="$2"
CALLER_NAME="$3"

# Full path to recording
FULL_PATH="/var/spool/asterisk/recording/$RECORDING_FILE"

# Check if file exists
if [ ! -f "$FULL_PATH" ]; then
    echo "Recording file not found: $FULL_PATH"
    exit 1
fi

# Convert to MP3 for smaller file size
MP3_FILE="${RECORDING_FILE%.*}.mp3"
MP3_PATH="/var/spool/asterisk/recording/$MP3_FILE"

sox "$FULL_PATH" "$MP3_PATH"

# Send to email and Discord
python3 /opt/voip-scripts/send_notification.py "$MP3_PATH" "$CALLER_NUMBER" "$CALLER_NAME"

echo "Processing complete for $RECORDING_FILE"
