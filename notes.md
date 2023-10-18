
# tmux Sessions and Commands

## 1. zigbee2mqtt Session

```bash
tmux new-session -s zigbee2mqtt
npm start --prefix /opt/zigbee2mqtt
```
- After the above commands, the service should start.
- To detach from the session: Press `ctrl-b`, then `d`.

---

## 2. lavapy Session

```bash
tmux new-session -s lavapy
cd /home/gatnalysing/zigbee_projects/lavalamp
source lavenv/bin/activate
python lavalam.py
```
- After the above commands, the service should start.
- To detach from the session: Press `ctrl-b`, then `d`.

---

## 3. monitor Session

```bash
tmux new-session -s monitor
mosquitto_pub -h localhost -t zigbee2mqtt/MyLight/get -m '{}'
mosquitto_sub -h localhost -t zigbee2mqtt/MyLight -v
```
- After the above commands, the service should start.
- Optionally, you can stop the service with `ctrl + d`.
- To detach from the session: Press `ctrl-b`, then `d`.

---

## Helpful tmux Commands

- To re-enter a session (for example, `lavapy`): 
  ```bash
  tmux attach -t lavapy
  ```

- To list all active sessions:
  ```bash
  tmux list-sessions
  ```
```

I hope this format is better. Let me know if you'd like further modifications.

---

```markdown
## tmux Sessions and Commands

### **1. zigbee2mqtt Session**

```bash
tmux new-session -s zigbee2mqtt
npm start --prefix /opt/zigbee2mqtt
```
- After the above commands, the service should start.
- To detach from the session: Press `ctrl-b`, then `d`.

---

### **2. lavapy Session**

```bash
tmux new-session -s lavapy
cd /home/gatnalysing/zigbee_projects/lavalamp
source lavenv/bin/activate
python lavalam.py
```
- After the above commands, the service should start.
- To detach from the session: Press `ctrl-b`, then `d`.

---

### **3. monitor Session**

```bash
tmux new-session -s monitor
mosquitto_pub -h localhost -t zigbee2mqtt/MyLight/get -m '{}'
mosquitto_sub -h localhost -t zigbee2mqtt/MyLight -v
```
- After the above commands, the service should start.
- Optionally, you can stop the service with `ctrl + d`.
- To detach from the session: Press `ctrl-b`, then `d`.

---

### **Helpful tmux Commands**

- To re-enter a session (for example, `lavapy`): 
  ```bash
  tmux attach -t lavapy
  ```

- To list all active sessions:
  ```bash
  tmux list-sessions
  ```
```

This should give a clearer structure and organization to the content.
