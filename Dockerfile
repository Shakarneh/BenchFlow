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

# Gather static files into STATIC_ROOT so WhiteNoise can serve them.
# Done at BUILD time, not start time -- every container boot would repeat it.
RUN DJANGO_SECRET_KEY=build-only POSTGRES_DB=x POSTGRES_USER=x \
    POSTGRES_PASSWORD=x POSTGRES_HOST=x POSTGRES_PORT=5432 \
    python manage.py collectstatic --noinput

EXPOSE 8000

# gunicorn, not runserver. Django's dev server is single-process, unencrypted
# and explicitly "do not use in production". gunicorn runs several worker
# processes and is built to face the internet.
#
# $PORT because hosting platforms choose the port and tell you via that
# variable; the default keeps docker-compose working unchanged.
# On every start: apply migrations, make sure demo data and an admin exist,
# then serve. The `|| true` on the last two means "nice to have, not fatal" --
# they fail harmlessly when the user already exists or the vars are unset,
# and the site must still come up.
CMD ["sh", "-c", "\
python manage.py migrate --noinput && \
(python manage.py seed_demo || true) && \
(python manage.py ensure_admin || true) && \
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]
