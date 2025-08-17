git add .
o bien: git add nombre_fichero
git commit -m "Primera version"
git push origin main

****************
https://www.youtube.com/watch?v=Z4yeRyf8MhM
****************
digitalocean.com
****************

ssh-keygen -t rsa -b 4096 -C "dotintrade@gmail.com"
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDHICCTL/8Sl+/7h/sSkAkCcx5ALay+8Aw6VJL5ULARye5Kj8R3g/tsJVTq6okt7WpWYmMTywwsS4AlxBgyU9MpuAMqgQPcU6hU+HJqD72u4xCu/B9Zv445Hme+IRsggGN82Gi0mXUjUS+bpy8jpczKd9dV3Ua9qu5y2yaclz2jUxyQyaRuRIKKMvZlvpvx8n3lDmDY7SI98/9VB3tnA0meGh4HSRBk4SnbHLqA9wWGwwe9IA+H3fgopHdBNVHzB2iw35RfuWo8H9xzZoQ3XZf49EFO7KFUsOiipkTK/ehsCc5SCoUK7aFkXZpjQ+8t/QebIMOoa8M+oR3CXE++2759hGueJ2oYQV3KgrWEmg026Xl5hwjFBGxX7dyoT0AzkE/WhWoYULBKD+j7aCEBZVcF3s7wOSwfQ8mvyy+PzLQ4YMoiwbt3PcUQrdXIR2gYvqvOcblyhwKbDSBvEajIU1/2/wD39c/SRCi35ZCph03/D6Ft4bPHofrhUsakgL9sVnHB3pA1jlgDWeLWqxun6d/KbFhZpeT25W0HfIkPnvFzks2y4pAEn+j2nLJIZbYo1q/TXTeItucgGY04Jr+DWHCVg/pt2+u8JG0TaCaPPkUHUGvXqht/krDUkPDd3VnKLXtLk2E4xrxhagMVfjRqMej73fZ+DI3sdhaZuY579dNlGw== dotintrade@gmail.com

****************
22.04 (LTS) x64
****************
cd C:\Datos\Trabajo\Crypto\Python\dotSaldo

De las dos claves que he generado, la PUBlica esla que se sube a digitalocean la otra es la que hay que usar:
ssh -i "dotintrade" root@206.189.56.163
****************
sudo apt upgrade

****************
adduser dotintrade
...
usermod -aG sudo dotintrade
****************
ufw app list
ufw allow OpenSSH
ufw status
ufw enable
****************
rsync --archive --chown=dotintrade:dotintrade ~/.ssh /home/dotintrade
****************
ssh -i "dotintrade" dotintrade@206.189.56.163

pwd --> compruebo que estoy en el home del usuario dotintrade	
***************
Conexion a git ...

Descargo git:
sudo apt update && sudo apt install git -y

Creo unas claves nuevas en el servidor:

cd ./ssh

ssh-keygen -t rsa -b 4096 -C "dotingrade@gmail.com"

las claves se encuentran en: /home/dotintrade/.ssh/

cat ~/.ssh/id_rsa.pub

copio todo lo anterior al portapapeles
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDlQSoUQ7vl9u655Utt7fnWYk65y5BqjaZopWGmbdBw6+WbEwc8QeV0/GZBiPsESOJnBiu80wyq1DfhzSf7w6M9mnUCOEQnFAjOKkmnBw1jN6CaXxUQ3E6XrD7jvijznxhBJzvxKVafYdcP6nAziODKFqFS14LBnm2M54URa4d6qdl/hTnjPOuT8h8yIOu1NxPzxk+jir5KBWqteiZIT8TUTX/5Q1WiIdoRy2vUn3LllSR79MoZUcjkDIb099y8a8GX7sYPbLq/vcQWImyDsdLWcHDK9uw2aycrZbIp3Nz8g1/M1pU6vtsBnDhGC4vWLHHcNKAxNEFyD+57n8Rq0Vmbvok9ZuKkaz9uuGZnDREBdEgTIhB3t8EkPwxVLZ0qqHXYF8kxxjcmkA4vhe2CZDWZkR5+LNijtizCoEOLJU8UTovDQa4fPLeEeSeLbIZNJvHsCki2X00AyruhET5Gt5MyNQjUReUP0IB/1p56hZ5rQ/Dijs0+WaVkhSwzMYgfjDnrjVb5w4XESr7JjHjyB/a89ux7N6yj30zXNrzF2Xj51YtSHZ3fJaJsbClaVo5sxibGpLS2DavzBdGf0KPEGKchDWlNKgdt5NC8SEydtXZHURuc5/xW+tGrii7C+RsntXaYxxzIIA/RZVVNF+T+/drbFGPL6ZWZp9BPwDjeFQQeKw== dotingrade@gmail.com

Voy a git y en MI USUARIO y opcion settings SSH y GPH keys y creo una nueva clave SSH

Voy a mi repositorio y al boton CODE. selecciono la parte de SSH para constuir el comando que clonara el repositorio en git, en el servidor:

git@github.com:dotintrade/dotSaldo.git

git clone git@github.com:dotintrade/dotSaldo.git

Ejecuto el comando en el home del usuario dotintrade y ya está todo el codigo de git en el servidor.

cuando quiera traer cambios en git:

cd /ruta/del/repositorio
git pull origin main

***************************
Vamos a instalar python y las dependencias:

sudo apt install python3-pip
pip install python-binance python-dotenv requests

no reconoce python, vamos a decirle que es python3:
sudo apt update && sudo apt install -y python-is-python3
***************************
para quitar tabuladores a espacios
	
expand -t 4 testSaldo.py > testSaldo_fixed.py
mv testSaldo_fixed.py testSaldo.py

****************************
Para descargargar lo que tengo en github al repo en el servidor

git pull git@github.com:dotintrade/dotSaldo.git