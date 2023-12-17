# syntax=docker/dockerfile:1
FROM python:3.11-alpine as build

WORKDIR /usr/app

# RUN apk add --no-cache gcc musl-dev linux-headers

# COPY requirements.txt .
# RUN python -m venv /usr/app/venv
# ENV PATH="/usr/app/venv/bin:$PATH"
# RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

# COPY . .

# RUN python setup.py install

# FROM python:3.11-alpine

# RUN mkdir /var/log/supervisord

# COPY --from=build /usr/app/venv /usr/app/venv

# ENV PATH=/usr/app/venv/bin:$PATH

# COPY docker/polyvisor/polyvisor.conf /etc/
# COPY docker/bin/* /usr/local/bin/

# CMD ["supervisord", "-c", "/etc/supervisord/supervisord.conf"]
