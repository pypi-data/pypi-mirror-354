# Accepts the base image as a build argument
ARG BASE_IMAGE=ubuntu:latest
FROM ${BASE_IMAGE}

RUN if [ -f /etc/debian_version ]; then \
        apt-get update; \
        apt-get install -y --no-install-recommends pipx; \
    elif [ -f /etc/arch-release ]; then \
        pacman -Syu --noconfirm python-pipx; \
    elif [ -f /etc/fedora-release ]; then \
        dnf install -y pipx; \
    else \
        echo "Unknown distribution"; \
        exit 1; \
    fi

# Create a non-root user
RUN useradd -rm -d /home/sf -s /bin/bash -g root -u 1001 sf
USER sf
WORKDIR /home/sf/app

# Copy the current directory contents into the container at /home/sf/app
# excluding the tests directory
COPY --chown=sf:sf . /home/sf/app
RUN rm -rf /home/sf/app/tests

# Run install.sh from scripts directory
RUN chmod +x /home/sf/app/scripts/install.sh \
    && /home/sf/app/scripts/install.sh

RUN echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
