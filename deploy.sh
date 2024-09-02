#!/bin/bash

# Получение значений из переменных окружения GitHub Actions
DOCKER_IMAGE="4836297/postgres-application:$GITHUB_RUN_NUMBER"

# Вывод значений на экран
echo "Docker Image Tag: $DOCKER_IMAGE"