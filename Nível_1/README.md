# Projeto de Extensão de Monitoramento Ambiental

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Licença](https://img.shields.io/badge/licença-MIT-blue)

## Índice

- [Descrição do Projeto](#descrição-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Licença](#licença)

## Descrição do Projeto

O **Projeto de Extensão de Monitoramento Ambiental** é um sistema IoT desenvolvido para monitorar a qualidade do ar em áreas urbanas. Utilizando sensores integrados e análise em tempo real, o projeto visa promover a conscientização ambiental e fornecer dados precisos para a comunidade.

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python 3.11.2
- **Banco de Dados:** MongoDB

## Instalação

Para configurar o ambiente de desenvolvimento, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/IncludeLuisFerreira/Equipe-de-programacao.git


2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt

3. **Renomeie o arquivo passwords.exemple.py para passwords.py:**
   ```bash
   mv passwords.exemple.py passwords.py

4. **Preencha as suas credenciais no arquivo passwords.py:**
   ```python
   keys =  {
    "MONGO_URI" : "exemploUri\mongoUser",
    "MQTT_SERVER" : "coloque o server",
    "MQTT_USER" : "insira o user",
    "MQTT_PASSWORD" : "digite a senha"
   }

4. **Execute o programa no terminal**
   ```bash
   python3 python_bd.py

## Licença

Distribuído sob a licença MIT. Veja **LICENSE** para detalhes.