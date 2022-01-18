#!/bin/bash
rm -rf ./allure-reports/*
allure generate --clean -o allure-reports/
rm -rf ./allure-results/history
cp -r ./allure-reports/history ./allure-results/history
zip -r ./"report_$(date '+%Y-%m-%d_%H:%M:%S').zip" ./allure-reports/*
kill -9 $(lsof -ti:8000) || sudo kill -9 $(lsof -ti:8000)
python3 -m http.server --directory ./allure-reports/ &
xdg-open http://127.0.0.1:8000/ || open http://0.0.0.0:8000/