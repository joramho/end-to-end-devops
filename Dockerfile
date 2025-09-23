FROM jenkins/jenkins:lts

USER root

# Install Python3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to Jenkins user
USER jenkins
