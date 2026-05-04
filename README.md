# Monitoramento Remoto de Vacinas - UNIVESP

Sistema IoT para monitoramento em tempo real da temperatura em ambientes de armazenamento de vacinas.

---

## Visão Geral

O projeto coleta dados de temperatura via **ESP32**, transmite por **MQTT** e disponibiliza visualização através de um backend em **Flask**, utilizando **PostgreSQL** como banco de dados.

**Objetivo:** garantir rastreabilidade e integridade térmica em ambientes críticos (como os freezers de vacinas).

---

## Arquitetura

```
ESP32 → MQTT (Mosquitto) → Backend (Flask) → PostgreSQL → Frontend
```

- **ESP32**: coleta e publica temperatura  
- **MQTT Broker**: transporta as mensagens  
- **Backend**: processamento, API e gravação no banco de dados  
- **Frontend**: visualização e controle  

---

## Stack Tecnológica

- **Firmware**: C (ESP-IDF)  
- **Backend**: Python + Flask  
- **Banco de Dados**: PostgreSQL  
- **Protocolo de Comunicação IoT**: MQTT (Mosquitto)  
- **Frontend**: HTML/CSS/JS  

---

## Estrutura do Projeto

```
├── firmware/      # Código ESP32
├── app/           # Backend Flask
├── mqtt/          # Scripts auxiliares
├── frontend/      # Interfaces HTML
├── doc/           # Documentação técnica
├── run.py         # Entry point
└── requirements.txt
```

---

## Execução

### 1. Backend

```bash
git clone https://github.com/Bitx86/monitoramento-remoto-univesp.git
cd monitoramento-remoto-univesp

python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

Crie o arquivo `.env`:

```
DB_HOST=localhost
DB_USER=usuario
DB_PASS=senha
DB_DB=vacinas_db
SECRET_KEY=chave
```

Inicie o servidor:

```bash
python run.py
```

---

### 2. Banco de Dados

```sql
CREATE DATABASE vacinas_db;
```

> Consulte `doc/` para estrutura completa, incluindo DER e MLR para melhores orientações.

---

### 3. Firmware (ESP32)

```bash
cd firmware
idf.py build flash monitor
```

---

## Funcionalidades

- Monitoramento de temperatura em tempo real  
- Histórico de dados  
- Autenticação de usuários (JWT)  
- Gerenciamento de dispositivos  
- Integração via MQTT  

---

## API (Resumo)

- `POST /login`
- `GET /devices`
- `GET /historico`
- `GET /dashboard`

---

## Segurança

- Hash de senha (bcrypt)  
- Autenticação via JWT  
- Rate limiting  
- Validação de entrada  

---

## Direção do Projeto

- Suporte a múltiplos sensores  
- Sistema de alertas  
- Visualização avançada de dados  
- API documentada  

---

## Licença

Projeto acadêmico — UNIVESP (2026)

---

## Contato

Abra uma issue no repositório, e tentaremos entender ou corrigir o que vier a ocorrer.
