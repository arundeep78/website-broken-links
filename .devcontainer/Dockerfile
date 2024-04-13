FROM raviqqe/muffet AS build

FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

COPY --from=build /muffet /usr/bin/muffet

