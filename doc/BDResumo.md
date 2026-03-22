# 1) Visão geral do modelo

Você tem quatro blocos:

* **users** → identidade humana
* **devices** → identidade do ESP32
* **device_telemetry** → dados enviados
* **device_tokens / device_acl** → controle e segurança

A relação central é:

```
users → devices → telemetry
```

---

# 2) users (já existente)

Representa o usuário do sistema (login).

Campos importantes:

* `id` → UUID (chave principal)
* `email` → login único
* `password_hash` → autenticação web
* `role` → controle de acesso

Uso no sistema:

* login no Flask
* dono dos devices

---

# 3) devices (núcleo do IoT)

Cada ESP32 é um registro aqui.

```sql
devices
```

Campos:

* `id` → UUID interno (usado no banco)
* `device_id` → identificador público (usado no MQTT)
* `user_id` → dono do dispositivo
* `device_secret_hash` → autenticação do device
* `is_active` → permite revogar acesso
* `last_seen` → monitoramento

### Uso prático

Quando o usuário cria um device:

1. gera `device_id`
2. gera `secret` (plaintext, só uma vez)
3. salva `hash(secret)`
4. retorna ao usuário

---

# 4) device_telemetry (dados)

Armazena tudo que vem do MQTT.

```sql
device_telemetry
```

Campos:

* `device_id` → FK para devices
* `temperature`, `humidity` → dados estruturados
* `payload` → flexível (JSON)
* `created_at` → timestamp

### Uso prático

Subscriber MQTT faz:

```
recebe mensagem → resolve device → insere aqui
```

---

# 5) device_tokens (opcional / futuro)

Serve para:

* JWT
* sessões de device
* expiração de acesso

Hoje você **não precisa usar ainda**.

---

# 6) device_acl (opcional)

Controle fino de tópicos MQTT.

Mas no seu caso inicial:

> melhor gerar ACL dinamicamente baseado em user/device

Então essa tabela pode ficar parada por enquanto.

---

# 7) Fluxo completo do sistema

### 1. Usuário cria device

Flask:

```
POST /devices
```

Backend:

* cria `device_id`
* gera `secret`
* salva hash
* retorna:

```json
{
  "device_id": "esp32-001",
  "secret": "abc123",
  "topic": "users/{user_id}/devices/esp32-001/"
}
```

---

### 2. ESP32 conecta no MQTT

```
username = device_id
password = secret
```

---

### 3. Publicação

```
topic: users/{user_id}/devices/{device_id}/temperature
```

---

### 4. Backend (subscriber)

* escuta MQTT
* extrai `device_id`
* valida no banco
* insere em `device_telemetry`


