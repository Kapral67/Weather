FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build-env
RUN mkdir /csharp
WORKDIR /csharp
ADD ./weatherFrontEnd/. /csharp/
WORKDIR /csharp/
RUN dotnet publish -c Release
#RUN dotnet build
#RUN dotnet dev-certs https
#RUN dotnet dev-certs https -ep /usr/local/share/ca-certificates/aspnet/https.crt --format PEM
#RUN update-ca-certificates
