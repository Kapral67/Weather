# Whether README
- Blazor Site Accessible at https://whether.maxkapral.com (weather.maxkapral.com is setup as a redirect as well)
- Django-REST API is hosted at https://cdn.maxkapral.com
- Django Backend uses Django-REST to serve content and store locations as well as user accounts
- Blazor runs native WebAssembly using [AOT Compilation](https://docs.microsoft.com/en-us/aspnet/core/blazor/host-and-deploy/webassembly?view=aspnetcore-6.0#ahead-of-time-aot-compilation)
- Locations are Geocoded using the google maps API in the backend (django)

- This app is intended to run and has been tested on Ubuntu-20.04-focal LTS amd64

## Running, Complete Following in Order:

#### Setting Up Django:

   - `docker-compose build django`
   - `docker-compose run django /bin/bash`
      - `cd django/weatherBackEnd`
      - `python manage.py makemigrations && python manage.py migrate`

#### Setting Up Blazor:

   - `docker-compose build blazor`
   - `docker-compose run blazor /bin/bash`
      - `cd blazor-wasm/weatherFrontEnd`
      - `dotnet publish -c Release`
      - `chmod -R 777 bin && chmod -R 777 obj`

#### Setting Up Nginx:

   - `docker-compose build nginx`

#### Running:

   - `docker-compose up` or `docker-compose up -d`
