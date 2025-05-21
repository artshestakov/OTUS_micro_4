#!/bin/bash

# Получаем версию (кол-во коммитов в репозитории)
#VERSION=$(git rev-list --count HEAD)

# Собираем образ
docker build --no-cache -t 'crud' .
