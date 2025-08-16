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
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNxYJwUAp8PWnqOWy2Q4ekjm047kMW1ZUhn84hsIPMyei3OTTcKhd4R4rvODCom3uA+i7f8/P35Wm5Q/RJixxSRBt7gRfxs9M7BkxI/GqX+vhryD3RHLcJxJ53AUqianCS8swUuz6Q/cLUZCM3La9pJdijAV1fcziQu6Ja7v1dVbNIJsA4nocsZcnmVssdTXYHj2tTBufcqyWp1KDFiVYhPUKnHmnhgAkG/Z/A0arM8iVCH9pUY6xMLskS5W7s2+6Og9YfOoxx96CO+FeEXYE8RlMhz8CxZxDtTxDOgwC1QtuF05uyi7+XTmWf0oyLIjPM4WNyU+mNsHv/jZksMyeD5Ei+akj8OckpmX+WNX6zz7OByqZZd8uWuLdwNTv8uDVwHPUjmy80DfJ+/BYtpZv/+5PL0HeP+KXclbW9Dqn2AhCWtaLvS96UinjTeNbjViRJIA4oBADuvEamW7wdk1sNtHwO61n9IjQ8ePZUBXrK7cviK7H9++WK4hwcoz8mfBixa4hasEfvXXUtoH7sBpdfZ2FFFoW92AoSPrrLnH2HWMw21MIcCO4nwFkOepwub7cI48Uh/GactMUkxKlEoESdxN1hSTTQNgCtP62dIHSINdXLFzJPD60Yg2gXsKaKBaUA4VUm0QI1YhHWMwR0f96xwBdLNaUaRmYZxzhSBOTv+Q== dotintrade@gmail.com
****************
cd C:\Datos\Trabajo\Crypto\Python\dotSaldo

De las dos claves que he generado, la PUBlica esla que se sube a digitalocean la otra es la que hay que usar:
ssh -i "dotintrade" root@206.81.25.147
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
ssh -i "dotintrade" dotintrade@206.81.25.147

pwd --> compruebo que estoy en el home del usuario dotintrade	
***************
Conexion a git ...

Descargo git:
sudo apt update && sudo apt install git -y

Creo unas claves nuevas en el servidor:

ssh-keygen -t rsa -b 4096 -C "dotingrade@gmail.com"

las claves se encuentran en: /home/dotintrade/.ssh/

cat ~/.ssh/id_rsa.pub

copio todo lo anterior al portapapeles
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDZ7a/NNBwFSQd5sPaaOk6hFHTnWnIr/pHhh7xYRFbAKfrHjqmmgeegHLM2xoKAz7fRDtDBHRDhwlz6rQ0RQWgVd9x7huPoKiaVdUr/BZTgV8fY6vVAsISaq+Sts5KjcHHv7ERXGgRK4RzRSZCo1lTsQwF6cNvYqDIWRzAOwAskroDSsMd1t7eDPzt8+UVp3JtlSAcswMFFSLKax6Y5Gh7+kX0kl8vm1kyFXmxPldFhTv1ODZmDOmmrmI70sBSmc1j2JSue/9IQtqw8g1hbTUf3WQHeSbUTDQ2HQWzXFyb/M6xKJLqSk3y4O7RA/OyPKfclYsJm01WAsQU2i+oLqDLmSKgftRK/25asx3F81pbsze4zOi360wkCxQoiT2ghh/S1ym1XJcLYcjZAlBdDjyQlY3V/Rz/2Nu1sdxkSKkO19sLX6AWhAyYroTcflHt3rNJSwPDxwjwWt7DSlxEZjj2tv4q/V6pY/opMNyAKr9bzPG4tkGLa8tE6uiCXe68gq0PhGO9PZcyISZBHika9RYYzbTs6vM+sLCwMPnSZydG3GA698na4bUwjfWTCQJ0OrP44VVLBWeukt+6vR9qxwY5Hu0s3TsIPaR96P2Jqc9bH+58Sctp+O6u2BEe73EpRs05x4JPgbM2x1Fvyk2AVkH+mACSKu1YKURsTORPruilejQ== dotingrade@gmail.com

Voy a git y en MI USUARIO y opcion settings SSH y GPH keys y creo una nueva clave SSH

Voy a mi repositorio y al boton CODE. selecciono la parte de SSH para constuir el comando que clonara el repositorio en git, en el servidor:

git@github.com:dotintrade/dotSaldo.git

git clone git@github.com:dotintrade/dotSaldo.git

Ejecuto el comando en el home del usuario dotintrade y ya está todo el codigo de git en el servidor.

cuando quiera traer cambios en git:

cd /ruta/del/repositorio
git pull origin main

***************************
Vamos a instala python y las dependencias:

sudo apt install python3-pip
pip install python-binance python-dotenv requests

