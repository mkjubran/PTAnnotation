FROM python:3.11-slim

# Set proxy build arguments
ARG HTTP_PROXY
ARG HTTPS_PROXY
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}

WORKDIR /app

COPY requirements.txt .

# Optional: configure pip to always use proxy
RUN mkdir /root/.pip && \
    echo "[global]\nproxy = ${HTTP_PROXY}" > /root/.pip/pip.conf

# Configure apt to use proxy for this install
RUN echo "Acquire::http::Proxy \"${HTTP_PROXY}\";" > /etc/apt/apt.conf.d/01proxy && \
    echo "Acquire::https::Proxy \"${HTTPS_PROXY}\";" >> /etc/apt/apt.conf.d/01proxy && \
    apt-get update && \
    apt-get install -y nano && \
    rm -rf /var/lib/apt/lists/* && \
    rm /etc/apt/apt.conf.d/01proxy

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY build ./build

EXPOSE 5000
CMD ["python", "app.py"]
