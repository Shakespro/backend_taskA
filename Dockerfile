FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Create and activate a virtual environment (optional)
# RUN python -m venv /venv
# ENV PATH="/venv/bin:$PATH"

COPY . /app

ENTRYPOINT ["gunicorn", "backend.wsgi", "-b", "0.0.0.0:8000"]