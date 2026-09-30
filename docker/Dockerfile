FROM python:3.12-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN useradd --system --uid 10001 --no-create-home appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/src/ .
USER 10001
EXPOSE 5000
CMD ["python", "app.py"]