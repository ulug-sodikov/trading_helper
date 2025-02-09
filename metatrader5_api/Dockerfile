FROM ghcr.io/linuxserver/baseimage-kasmvnc:debianbullseye-8446af38-ls104

RUN apt update
RUN apt install wget

# https://gitlab.winehq.org/wine/wine/-/wikis/Debian-Ubuntu
RUN dpkg --add-architecture i386

# Download and add the repository key.
RUN mkdir -pm755 /etc/apt/keyrings
RUN wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
RUN gpg --dearmor /etc/apt/keyrings/winehq-archive.key

RUN wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bullseye/winehq-bullseye.sources
RUN apt update
RUN apt install --install-recommends winehq-stable -y

RUN wget -O /mt5setup.exe https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe
RUN wget -O /python_installer.exe https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe

# /defaults/autostart will run on debian start.
COPY ./root /

# Make /scripts/autostart_script.sh file executable.
RUN chmod +x /scripts/autostart_script.sh

COPY ./server /server

ENV MT5_TERMINAL_PATH="/config/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe"
