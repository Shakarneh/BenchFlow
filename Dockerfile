# How to build a sealed Linux box containing benchFlow and everything it needs.
#
# Each instruction creates a LAYER, and Docker caches layers. That is why
# requirements are copied and installed BEFORE the source code: changing a
# .py file then rebuilds only the last layer, not the whole dependency
# install. Reversing those two lines would make every rebuild slow.

FROM python:3.13-slim

# PYTHONDONTWRITEBYTECODE: no .pyc files -- pointless inside a container.
# PYTHONUNBUFFERED: print immediately instead of buffering, so `docker logs`
# shows output as it happens rather than in delayed chunks.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# --- dependency layer (changes rarely) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- source layer (changes constantly) ---
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
