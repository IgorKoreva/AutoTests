#!/bin/bash
echo "clear dir report"
rm -rf ./allure-reports
echo "generate report"
allure generate --clean -o allure-reports/
zip -r ./report.zip ./allure-reports/*
python3 -m http.server --directory ./allure-reports/
google-chrome-stable http://0.0.0.0:8000/