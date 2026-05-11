# lgtv-web

Web UI to control LG webOS TVs over your local network. Built with Flask + bscpylgtv.

## Setup

```bash
git clone https://github.com/mac1010z/lgtv-web
cd lgtv-web
pip install -r requirements.txt
```

Edit the TV IPs in `server.py`:

```python
TVS = {
    "mine":    {"ip": "192.168.x.x", "name": "My TV"},
    "parents": {"ip": "192.168.x.x", "name": "Parents TV"},
}
```

## Run

```bash
python3 server.py
```

Open `http://<your-mac-ip>:5000` on any device on the same network.

## Requirements

- Python 3.8+
- LG webOS TV on the same network
- LG Remote Service enabled on the TV:
  `Settings → Support → Quick Help → LG Remote Service`
