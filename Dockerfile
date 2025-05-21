FROM debian:bullseye-slim

# Отмечаем папку по умолчанию
WORKDIR /app

# Копируем туда скарипт с нашей программмой
COPY main.py /app
COPY requirements.txt /app

# Устанавливаем Питон
RUN \
  apt update && \
  apt upgrade -y && \
  apt -y install \
    python \
    pip

# Устанавливаем зависимости (Flask)
RUN \
  pip3 install -r requirements.txt

# Запускаем наш скрипт
ENTRYPOINT [ "python3", "main.py" ]

