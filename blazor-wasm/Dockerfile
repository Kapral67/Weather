FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build-env
RUN mkdir /csharp
WORKDIR /csharp
ADD ./weatherFrontEnd/. /csharp/
WORKDIR /csharp/
RUN apt-get update -y
RUN apt-get install -y python3
RUN dotnet workload install wasm-tools
RUN dotnet clean
#RUN dotnet publish -c Release
#RUN dotnet dev-certs https
#RUN dotnet dev-certs https -ep /usr/local/share/ca-certificates/aspnet/https.crt --format PEM
#RUN update-ca-certificates
