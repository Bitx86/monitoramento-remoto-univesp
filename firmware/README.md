# Firmware ESP32

Firmware embarcado responsável pela coleta de temperatura e envio de dados para o backend via MQTT.

Este código faz parte do sistema de monitoramento remoto de vacinas e representa a **camada de aquisição de dados (edge)**, camada demonstrada na disciplina "Protocolos de Comunicação IOT COM380".

---

## Visão Geral

O firmware executa no ESP32 e tem como responsabilidades:

- Conectar O ESP32 a rede WiFi  
- Autenticar no broker MQTT  
- Ler sensores de temperatura  
- Publicar dados periodicamente  

---

## Arquitetura

O projeto foi estruturado seguindo uma abordagem **modular e orientada a componentes**, separando responsabilidades em blocos independentes.

```
WiFi → MQTT → Sensor → Publish
```

### Componentes

- **WiFi (`wifi.c`)**  
  Gerencia conexão, eventos e reconexão automática  

- **MQTT (`mqtt.c`)**  
  Responsável pela autenticação e envio de mensagens  

- **Sensor (`temp.c`)**  
  Abstrai a leitura de temperatura (ex: DS18B20)  

- **Main (`sistema-vacinas-esp32.c`)**  
  Organiza todos juntos, e orquestra a inicialização e loop principal  

---

## Estrutura

```
main/
├── sistema-vacinas-esp32.c
├── wifi.c / wifi.h
├── mqtt.c / mqtt.h
├── temp.c / temp.h
```

Separação clara entre:
- comunicação (WiFi / MQTT)  
- aquisição de dados (sensor)  
- controle (main / tasks)  

---

## Integração com o Sistema

O firmware se conecta ao backend através do broker MQTT.

- **Autenticação**
  - `username` = device_id  
  - `password` = secret  

- **Tópico**
```
users/{user_id}/devices/{device_id}/temperature
```

---

## Execução

### Configuração

```bash
idf.py menuconfig
```

Configurar:
- "Configuraçãoo Wi-Fi:" WiFi (SSID / senha)  
- "Configuração MQTT:" MQTT (broker, credenciais, tópico)  

---

### Build e Flash

```bash
cd firmware
idf.py build flash monitor
```

---

## Fluxo de Operação

1. Inicializa WiFi  
2. Conecta ao broker MQTT  
3. Lê sensor  
4. Publica dados em intervalo fixo  

---

## Formato da Mensagem

```json
{
  "temperatura": 5.25
}
```

---

## Debug

```bash
idf.py monitor
```

Monitoramento MQTT:

```bash
mosquitto_sub -t "users/+/devices/+/temperature" -v
```

---

## Observações de Projeto

- Arquitetura modular facilita manutenção e extensão  
- Comunicação desacoplada via MQTT (pub/sub)  
- Preparado para:
  - múltiplos sensores  
  - novos tipos de dados  
  - melhorias como OTA ou economia de energia  

---

## Problemas Comuns

**WiFi não conecta**
- Verifique SSID/senha (2.4GHz)

**MQTT falha**
- Confira credenciais (`device_id` / `secret`)

**Sensor retorna valor inválido**
- Verifique conexão e GPIO  
