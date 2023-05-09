FROM kumatea/pyrogram:latest

# Create conda environment
RUN set -ex && \
    wget https://github.com/KumaTea/docker/tarball/master -O /tmp/kuma-docker.tar.gz && \
    mkdir -p /tmp/docker && \
    tar -xzf /tmp/kuma-docker.tar.gz -C /tmp/docker --strip-components 1 && \
    bash /tmp/docker/scripts/install-packages.sh "apscheduler" "" && \
    rm -rf /tmp/docker && \
    rm /tmp/kuma-docker.tar.gz

# Download repo
# No, I'll use volume mount

# Install dropbear as ssh client
RUN set -ex && \
    apt update && \
    apt install -y dropbear && \
    apt clean && \
    rm -rf /root/.cache/* || echo "No cache in .cache" && \
    rm -rf /var/cache/* || echo "No cache in /var" && \
    rm -rf /var/lib/apt/lists/* || echo "No apt lists"

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/home/kuma/bots/dk/docker/run-docker.sh"]
