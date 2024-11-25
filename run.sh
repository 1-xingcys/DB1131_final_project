#!/bin/bash

if [ "$1" == "all" ]; then
    docker-compose up -d --build
elif [ "$1" == "dev" ]; then
    docker-compose -f docker-compose.dev.yml up -d --build
else
    echo "用法：$0 [all|dev]"
    echo "  all - 跑所有服務"
    echo "  dev - 只跑後端跟資料庫"
    exit 1
fi