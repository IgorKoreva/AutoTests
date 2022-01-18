#!/bin/bash
reports="$(pwd)/allure-reports"
results="$(pwd)/allure-results"
pid=$(lsof -ti:8000)
url="http://127.0.0.1:8000/"
rm -rf "${reports}/*"
allure generate --clean -o ${reports}
rm -rf ${results}/history
cp -r ${reports}/history ${results}/history
cp run.cmd run.sh ${reports}
zip -r ./"report_$(date '+%Y-%m-%d_%H:%M:%S').zip" ${reports}/*
kill -9 ${pid} || sudo kill -9 ${pid}
python3 -m http.server --directory ${reports}/ &
xdg-open ${url} || open ${url}