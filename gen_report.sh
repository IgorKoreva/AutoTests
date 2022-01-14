#!/bin/bash
echo "clear dir report"
rm -rf ./allure-reports
echo "generate report"
allure generate --clean -o allure-reports/
zip -r ./report.zip ./allure-reports/*
sudo lsof -t -i tcp:8000 | xargs kill -9
python3 -m http.server --directory ./allure-reports/ &
google-chrome-stable http://0.0.0.0:8000/