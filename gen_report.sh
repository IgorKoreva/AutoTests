#!/bin/bash
rm -rf ./allure-reports/*
allure generate --clean -o allure-reports/
rm -rf ./allure-results/history
cp -r ./allure-reports/history ./allure-results/history
zip -r ./report.zip ./allure-reports/*
sudo lsof -t -i tcp:8000 | xargs kill -9
python3 -m http.server --directory ./allure-reports/ &
google-chrome-stable http://0.0.0.0:8000/