#!/bin/bash

# Script de build para o Render

echo "Instalando dependências do Python..."
pip install -r requirements.txt

echo "Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

echo "Instalando pnpm..."
npm install -g pnpm

echo "Entrando no diretório frontend..."
cd frontend

echo "Instalando dependências do frontend..."
pnpm install

echo "Fazendo build do frontend..."
pnpm run build

echo "Copiando arquivos para o diretório static do Flask..."
mkdir -p ../src/static
cp -r dist/* ../src/static/

echo "Voltando para o diretório raiz..."
cd ..

echo "Build concluído!"

