FROM redhat/ubi8:latest

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
    dnf -y install google-chrome-stable --nogpgcheck && \
    \
    # Add Node JS
    curl -sL https://rpm.nodesource.com/setup_17.x | bash - && \
    dnf -y install nodejs --nogpgcheck && \
    npm install -g lighthouse && \
    \
    # Add User
    useradd -m lighthouse && \
    echo "lighthouse:lighthouse" | chpasswd && \
    \
    # Add Volume for data output
    mkdir -p /output && \
    chown lighthouse:lighthouse /output && \
    \
    # Clean up
    dnf remove unzip -y && \
    dnf clean all && \
    rm -f /tmp/*.zip && \
    rm -rf /var/cache/*

USER lighthouse
VOLUME [ "/output" ]
WORKDIR /output

COPY ./entrypoint.py .
ENTRYPOINT [ "python3", "./entrypoint.py" ]
