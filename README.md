# youtube downloader as an website form

A youtube downloader in form of website consist of 2 parts

1. Backend with Pytube/FastAPI/PostgreSQL (caching) and uvicorn
2. Frontend with Svelte (static)

For API implementation you can take a look at `/frontend/src/lib`

## requirements

- Python 3.9^
- PostgreSQL
- NodeJS
- NPM
- Your webserver (like NGINX, tomcat or whatever)
- GNU make (winget install -e --id GnuWin32.Make for windows. else every os should have it on PATH)
before you can host you need to edit .env file (required for backend) by rename .env.example to .env and edit

## hosting

read [requirements](#requirements) and IF YOU WANT TO RUN THIS PLEASE DO IT AT THE ROOT NOT INSIDE `/frontend` OR `/backend` ELSE IT WILL BREAK

1. Install dependencies with `make install_dep`
2. Build frontend with `make build_frontend` and output HTML is at `/frontend/build` and you can serve this with NGINX
3. Run backend up with `make run_backend` and it should run it at port 8000
