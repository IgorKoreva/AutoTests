for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a
start /b py -3 -m http.server --directory .
rundll32 url.dll,FileProtocolHandler http://127.0.0.1:8000/
