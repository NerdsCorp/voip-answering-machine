# Dockerfile
FROM debian:bullseye-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    asterisk \
    python3 \
    python3-pip \
    sox \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install requests python-dotenv

# Create directories
RUN mkdir -p /var/spool/asterisk/recording \
    && mkdir -p /etc/asterisk/custom \
    && mkdir -p /opt/voip-scripts \
    && mkdir -p /var/log/asterisk/cdr-csv && chown -R asterisk:asterisk /var/log/asterisk

# Copy configuration files
COPY asterisk/ /etc/asterisk/
COPY scripts/ /opt/voip-scripts/
COPY docker-entrypoint.sh /

# Make scripts executable
RUN chmod +x /docker-entrypoint.sh \
    && chmod +x /opt/voip-scripts/*.py \
    && chmod +x /opt/voip-scripts/*.sh

# Set proper ownership
RUN chown -R asterisk:asterisk /var/spool/asterisk \
    && chown -R asterisk:asterisk /etc/asterisk \
    && chown -R asterisk:asterisk /opt/voip-scripts

EXPOSE 5060/udp 10000-10001/udp

ENTRYPOINT ["/docker-entrypoint.sh"]
