# Potential-Robo-Net

Potential Robo Net is a small Django-based robotics platform for monitoring and controlling WiFi-enabled micro robots (example: NodeMCU ESP8266). This repository contains a backend API and a simple web UI that demonstrates real-time command/control and telemetry for an ESP8266-powered robot.

## What this repo contains
- Django project: `potential_robot_net`
- Dashboard app: `robot_dashboard` (existing)
- Controller app: `robot_control` (new) — UI + proxy API to send commands to an ESP8266 robot and display telemetry (distance, speed)
- Example ESP8266 sketch: `robot.ino` (in the repo attachments) — the robot serves a small JSON payload at `/` when it receives `?State=` commands.

## Key features
- Web-based controller UI served at `/control/` that sends commands and shows telemetry.
- Server-side proxy endpoint at `/control/api/command/` which forwards commands to the robot and returns the robot's JSON response (avoids browser CORS issues).
- Simple polling to keep distance and speed values updated.

## Quick start (development)
1. Create and activate a Python virtual environment.

```bash
python -m venv .venv
.
# Windows
.venv\Scripts\activate
# mac / linux
source .venv/bin/activate
```

2. Install dependencies (Django 4.x is required; add other deps as needed):

```bash
pip install django
```

3. Run migrations and start the dev server:

```bash
python manage.py migrate
python manage.py runserver
```

4. Open the controller UI at http://127.0.0.1:8000/control/

## Using the controller UI
- Enter your robot's IP address (for a NodeMCU in AP mode the default is usually `192.168.4.1`).
- Click the control buttons (Forward, Back, Left, Right, Stop, Beep, Light On/Off, Speed presets). The UI sends commands to the Django proxy which forwards them to your robot.
- The UI displays `distance` and `speed` values returned by the robot's HTTP response.

## Robot sketch behavior (ESP8266)
The provided `robot.ino` sketch listens for an HTTP query parameter `State` and performs motor/LED/buzzer actions. When a request to `/` contains `State`, the sketch returns a small JSON payload like:

```json
{"command":"F", "distance":"34", "speed":"1023"}
```

The Django proxy view (`robot_control/views.py`) requests `http://{robot_ip}/?State={X}` and relays that JSON to the web UI.

## Files to look at
- `robot_control/templates/robot_control/index.html` — controller UI template
- `robot_control/static/robot_control/controller.js` — client-side logic that calls the proxy
- `robot_control/views.py` — proxy endpoint that forwards commands to the robot
- `potential_robot_net/settings.py` — `robot_control` is registered in `INSTALLED_APPS` and `STATIC_URL` is configured

## Notes & troubleshooting
- Make sure the Django server can reach the robot's IP on the network (same LAN or connected to the robot's AP).
- If the UI doesn't load CSS/JS, hard-refresh the browser and make sure `STATIC_URL` is set to `/static/` (it is already updated).
- If your robot uses a different API or port, supply `host:port` in the UI's Robot IP field.

## Extending this project
- Add authentication or user access control to the controller UI.
- Replace polling with WebSocket or Server-Sent Events for lower-latency telemetry.
- Add persistent logging of commands and telemetry to the database.

## License & Contributing
Feel free to open issues or PRs. This repository is a demo platform — adapt it to your own robot hardware and networks.

