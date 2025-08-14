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

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY build ./build

EXPOSE 5000
CMD ["python", "app.py"]
