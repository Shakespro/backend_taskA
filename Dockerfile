FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_ENV=production

# Install the exact versions tested locally before copying application source.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# The host supplies PORT, DATABASE_URL, and DJANGO_SECRET_KEY at runtime.
CMD ["sh", "./start.sh"]
