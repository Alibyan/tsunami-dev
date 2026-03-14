# path: .devcontainer/Dockerfile
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=1000

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV TZ=Etc/UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    ca-certificates \
    curl \
    wget \
    git \
    git-lfs \
    gnupg \
    lsb-release \
    bash-completion \
    nano \
    vim \
    less \
    unzip \
    zip \
    jq \
    tree \
    procps \
    htop \
    build-essential \
    pkg-config \
    gcc \
    g++ \
    make \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    sqlite3 \
    libsqlite3-dev \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    libreadline-dev \
    libgomp1 \
    nodejs \
    npm \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Dedicated Python environment for the dev container
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:/home/${USERNAME}/.local/bin:${PATH}"

# Project runtime + dev tooling
RUN pip install --upgrade pip setuptools wheel && \
    pip install \
      requests \
      pandas \
      numpy \
      pydantic \
      scikit-learn \
      streamlit \
      plotly \
      pydeck \
      pyarrow \
      python-dotenv \
      jupyter \
      ipykernel \
      pytest \
      black \
      ruff \
      mypy \
      mcp-server-fetch

# Local MCP server for filesystem access in Copilot/VS Code
RUN npm install -g @modelcontextprotocol/server-filesystem && \
    npm cache clean --force

# Convenience symlinks
RUN ln -sf /opt/venv/bin/python /usr/local/bin/python && \
    ln -sf /opt/venv/bin/pip /usr/local/bin/pip

# Non-root user with passwordless sudo
RUN deluser ubuntu && \
    groupadd --gid ${USER_GID} ${USERNAME} && \
    useradd --uid ${USER_UID} --gid ${USER_GID} -m -s /bin/bash ${USERNAME} && \
    usermod -aG sudo ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME}

# Prepare workspace path; the actual repo bind mount happens in devcontainer.json
RUN mkdir -p /workspace /workspace/data /workspace/notebooks /workspace/outputs && \
    chown -R ${USERNAME}:${USERNAME} /workspace /home/${USERNAME}

WORKDIR /workspace
USER ${USERNAME}

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["sleep", "infinity"]