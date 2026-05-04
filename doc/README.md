# Arquitetura de Dados

Visão conceitual do modelo de dados utilizado no sistema de monitoramento remoto de vacinas.

Este documento descreve **entidades, relações e fluxo de dados**, independentemente da implementação específica no backend.

---

## Estrutura Conceitual

```
Usuário → Dispositivo → Telemetria
                ├── Tokens
                └── Permissões (ACL)
```

---

## Entidades

### Usuário
Representa quem utiliza o sistema.

- Autenticação  
- Identificação  
- Controle de acesso aos dispositivos  

---

### Dispositivo
Representa um equipamento físico (ex: ESP32).

- Associado a um usuário  
- Possui identidade própria no sistema  
- Mantém estado (ativo, último contato)  

---

### Telemetria
Dados coletados pelo dispositivo.

- Leituras periódicas (ex: temperatura)  
- Dados estruturados + payload flexível  
- Crescimento contínuo (alto volume)  

---

### Tokens
Credenciais usadas por dispositivos.

- Autenticação automatizada  
- Podem expirar  
- Podem existir múltiplos por dispositivo  

---

### Permissões (ACL)
Controle de acesso a recursos (ex: tópicos MQTT).

- Define o que cada dispositivo pode fazer  
- Baseado em regras (publish / subscribe)  

---

## Relações

- Um usuário possui múltiplos dispositivos  
- Um dispositivo gera múltiplos dados de telemetria  
- Um dispositivo pode ter múltiplos tokens  
- Um dispositivo pode ter múltiplas permissões  

---

## Fluxo de Dados

### Coleta

```
Dispositivo → Broker MQTT → Backend → BD
```

---

### Consulta

```
Frontend → Backend → Dados → Frontend
```

---

## Diretrizes de Projeto

- Separação clara entre identidade, dados e controle de acesso  
- Modelo preparado para crescimento de telemetria  
- Flexibilidade para diferentes tipos de sensores  
- Independência entre modelo conceitual e implementação  

---

## Observações

- O modelo aqui descrito é **abstrato**  
- A implementação real (Flask / PostgreSQL) pode variar  
- Consulte o código para detalhes específicos  

---

## Referência

- BDResumo: `BDResumo.md`
- DER: `diagrama_der.png`  
- Modelo lógico: `modelo_logico_relacional.jpeg`  
