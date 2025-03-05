# Python 12
FROM openvino/ubuntu24_dev:2025.0.0

USER root
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# vscodeユーザーを作成
RUN useradd -m vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# GPU アクセスのためのグループ設定
RUN set -eux; \
    GID="$(stat -c '%g' /dev/dri/render* 2>/dev/null || true)"; \
    if [ -n "$GID" ]; then \
      # /dev/dri/render* から GID が取得できた場合
      groupadd -r -g "$GID" render; \
    else \
      # 取得できなかった場合は -g を指定しない（空き GID を自動採用）
      groupadd -r render; \
    fi; \
    usermod -aG render vscode
    
ARG USER=vscode
USER $USER
WORKDIR /workspaces

ENTRYPOINT [ "/bin/bash" ]
