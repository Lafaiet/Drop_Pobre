#!/bin/bash

echo "Instalando..."

git clone https://github.com/gorakhargosh/pathtools.git
cd pathtools
python setup.py install

apt-get install python-dev
git clone https://github.com/dlitz/pycrypto.git
cd pycrypto
python setup.py install


apt-get install python-pip
apt-get install libyaml-*
pip install watchdog


echo "Prontinho :D"