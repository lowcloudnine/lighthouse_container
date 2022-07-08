FROM redhat/ubi8-minimal:latest

ENV WORK_DIR=/workspace
ENV USER=lighthouse

# Update the system & install Google Chrome
RUN \
    # Update the System
    microdnf -y update && \
    \
    # Add Google Chrome
    # microdnf -y install dnf-plugins-core && \
    microdnf -y install yum && \
    yum -y install yum-utils && \
    yum-config-manager --add-repo http://mirror.centos.org/centos/8-stream/AppStream/x86_64/os/ && \
    yum-config-manager --add-repo http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/ && \
    yum-config-manager --add-repo http://dl.google.com/linux/chrome/rpm/stable/x86_64 && \
    yum -y install xdg-utils liberation-fonts  --nogpgcheck && \
    yum -y install google-chrome-stable --nogpgcheck

# Install lighthouse and tools for running it, i.e. boto3, etc.
RUN \
    # Add Node JS
    curl -sL https://rpm.nodesource.com/setup_18.x | bash - && \
    yum -y install nodejs --nogpgcheck && \
    npm install -g lighthouse

# Create a lighthouse user & then do user related things
RUN \
    # Add User
    useradd -m ${USER} && \
    echo "${USER}:${USER}" | chpasswd && \
    \
    # Add Volume for data output
    mkdir -p $WORK_DIR && \
    chown ${USER}:${USER} $WORK_DIR

# Before changing to the lighthouse user, clean up the system
RUN \
    # Remove unused programs
    # microdnf -y remove vim-minimal && \
    # dnf -y remove curl && \
    # microdnf -y remove unzip -y && \
    # \
    # Clean up \
    microdnf clean all && \
    yum clean all && \
    rm -f /tmp/*.zip && \
    rm -rf /var/cache/*

# Switch to the lighthouse user and default to using the $WORK_DIR directory
USER ${USER}
VOLUME [ "$WORK_DIR" ]
WORKDIR $WORK_DIR

# Copy in the entrypoint script and make it the entry point
COPY ./entrypoint.py $WORK_DIR/entrypoint.py

# In the ENTRYPOINT Docker doesn't replace variables so, it's hard coded and
# the part before entrypoint.py needs to match the ENV variable WORK_DIR
# see https://docs.docker.com/engine/reference/builder/ for more info
ENTRYPOINT ["python3", "/workspace/entrypoint.py" ]
