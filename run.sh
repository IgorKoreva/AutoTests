kill -9 $(lsof -ti:8000) || sudo kill -9 $(lsof -ti:8000)
python3 -m http.server --directory . &
xdg-open http://127.0.0.1:8000/ || open http://0.0.0.0:8000/