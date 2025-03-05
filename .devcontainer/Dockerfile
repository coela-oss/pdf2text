# Python 12 ベースの OpenVINO コンテナ
FROM openvino/ubuntu24_dev:2025.0.0

USER root

ENV DEBIAN_FRONTEND=noninteractive \
    WORKSPACE_DIR=/workspaces/pdf2text \
    VENV_PATH=/opt/venv

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget \
    clinfo \
    vulkan-tools \
    mesa-vulkan-drivers \
    && rm -rf /var/lib/apt/lists/*

# Intel GPU 用ドライバ・ランタイムのインストール
WORKDIR /tmp/neo
RUN wget https://github.com/intel/intel-graphics-compiler/releases/download/v2.7.11/intel-igc-core-2_2.7.11+18581_amd64.deb \
    && wget https://github.com/intel/intel-graphics-compiler/releases/download/v2.7.11/intel-igc-opencl-2_2.7.11+18581_amd64.deb \
    && wget https://github.com/intel/compute-runtime/releases/download/25.05.32567.17/intel-level-zero-gpu-dbgsym_1.6.32567.17_amd64.ddeb \
    && wget https://github.com/intel/compute-runtime/releases/download/25.05.32567.17/intel-level-zero-gpu_1.6.32567.17_amd64.deb \
    && wget https://github.com/intel/compute-runtime/releases/download/25.05.32567.17/intel-opencl-icd-dbgsym_25.05.32567.17_amd64.ddeb \
    && wget https://github.com/intel/compute-runtime/releases/download/25.05.32567.17/intel-opencl-icd_25.05.32567.17_amd64.deb \
    && wget https://github.com/intel/compute-runtime/releases/download/25.05.32567.17/libigdgmm12_22.6.0_amd64.deb

# SHA256 チェック
RUN wget https://github.com/intel/compute-runtime/releases/download/25.05.32567.17/ww05.sum \
    && sha256sum -c ww05.sum || exit 1

# .deb パッケージのインストール
RUN dpkg -i *.deb || apt-get install -f -y

# 一時ディレクトリを削除
WORKDIR /
RUN rm -rf /tmp/neo

# GPU アクセス用の `render` グループ設定
RUN groupadd -r render \
    && usermod -aG render openvino \
    && usermod -aG render root

# ワークスペースディレクトリの作成と権限設定
RUN mkdir -p ${WORKSPACE_DIR} && chown -R openvino:openvino ${WORKSPACE_DIR}

WORKDIR ${WORKSPACE_DIR}

# 仮想環境の作成（権限エラー回避のために所有者を変更）
RUN mkdir -p ${VENV_PATH} && chown -R openvino:openvino ${VENV_PATH} \
    && python -m venv ${VENV_PATH}

# `venv` をデフォルト環境に設定
ENV VIRTUAL_ENV=${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:$PATH"

# `.bashrc` に仮想環境の有効化を追加し、VSCode のターミナルでも自動適用
RUN echo "source ${VENV_PATH}/bin/activate" >> /home/openvino/.bashrc

CMD ["/bin/bash"]
USER openvino
