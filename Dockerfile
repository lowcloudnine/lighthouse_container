FROM redhat/ubi8:8.5

ENV WORK_DIR=/workspace

# Update the system & install Google Chrome
RUN \
    # Update the System
    dnf -y update && \
    \
    # Add Google Chrome
    dnf -y install dnf-plugins-core && \
    dnf -y config-manager --add-repo http://mirror.centos.org/centos/8-stream/AppStream/x86_64/os/ && \
    dnf -y config-manager --add-repo http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/ && \
    dnf -y config-manager --add-repo http://dl.google.com/linux/chrome/rpm/stable/x86_64 && \
    dnf -y install xdg-utils liberation-fonts --nogpgcheck && \
    dnf -y install google-chrome-stable --nogpgcheck

# Install lighthouse and tools for running it, i.e. boto3, etc.
RUN \
    # Add Node JS
    curl -sL https://rpm.nodesource.com/setup_18.x | bash - && \
    dnf -y install nodejs --nogpgcheck && \
    npm install -g lighthouse && \
    \
    # Install boto3 in Python 3 for using S3 to store reports
    pip3 install boto3

# Create a lighthouse user & then do user related things
RUN \
    # Add User
    useradd -m lighthouse && \
    echo "lighthouse:lighthouse" | chpasswd && \
    \
    # Add Volume for data output
    mkdir -p $WORK_DIR && \
    chown lighthouse:lighthouse $WORK_DIR

# Before changing to the lighthouse user, clean up the system
RUN \
    # Clean up
    dnf remove unzip -y && \
    dnf clean all && \
    rm -f /tmp/*.zip && \
    rm -rf /var/cache/*

# Switch to the lighthouse user and default to using the $WORK_DIR directory
USER lighthouse
VOLUME [ "$WORK_DIR" ]
WORKDIR $WORK_DIR

# Copy in the entrypoint script and make it the entry point
COPY ./entrypoint.py $WORK_DIR/entrypoint.py

# In the ENTRYPOINT Docker doesn't replace variables so, it's hard coded and
# the part before entrypoint.py needs to match the ENV variable WORK_DIR
# see https://docs.docker.com/engine/reference/builder/ for more info
ENTRYPOINT ["python3", "/workspace/entrypoint.py" ]
