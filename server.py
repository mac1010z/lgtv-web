import asyncio
import threading
from flask import Flask, jsonify, request, render_template
from bscpylgtv import WebOsClient

app = Flask(__name__)

TVS = {
    "mine":    {"ip": "192.168.12.192", "name": "My TV"},
    "parents": {"ip": "192.168.12.233", "name": "Parents TV"},
}

clients = {}
loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()

def run(coro):
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result(timeout=10)

def get_client(tv):
    if tv not in clients:
        ip = TVS[tv]["ip"]
        async def connect():
            client = await WebOsClient.create(ip)
            await client.connect()
            return client
        clients[tv] = run(connect())
    return clients[tv]

@app.route("/")
def index():
    return render_template("index.html", tvs=TVS)

@app.route("/cmd/<tv>/<cmd>")
def cmd(tv, cmd):
    if tv not in TVS:
        return jsonify({"error": "Unknown TV"}), 404
    try:
        c = get_client(tv)
        val = request.args.get("val")

        if cmd == "vol_up":           run(c.volume_up())
        elif cmd == "vol_down":       run(c.volume_down())
        elif cmd == "vol_set":        run(c.set_volume(int(val)))
        elif cmd == "mute":           run(c.set_mute(not run(c.get_muted())))
        elif cmd == "power":          run(c.power_off())
        elif cmd == "play":           run(c.button("PLAY"))
        elif cmd == "stop":           run(c.button("STOP"))
        elif cmd == "ff":             run(c.button("FASTFORWARD"))
        elif cmd == "rw":             run(c.button("REWIND"))
        elif cmd == "up":             run(c.button("UP"))
        elif cmd == "down":           run(c.button("DOWN"))
        elif cmd == "left":           run(c.button("LEFT"))
        elif cmd == "right":          run(c.button("RIGHT"))
        elif cmd == "ok":             run(c.button("ENTER"))
        elif cmd == "back":           run(c.button("BACK"))
        elif cmd == "home":           run(c.button("HOME"))
        elif cmd == "info":           run(c.button("INFO"))
        elif cmd == "ch_up":          run(c.button("CHANNELUP"))
        elif cmd == "ch_down":        run(c.button("CHANNELDOWN"))
        elif cmd == "hdmi":           run(c.set_input(f"HDMI_{val}"))
        elif cmd == "netflix":        run(c.launch_app("netflix"))
        elif cmd == "youtube":        run(c.launch_app("youtube.leanback.v4"))
        elif cmd == "disney":         run(c.launch_app("com.disney.disneyplus-prod"))
        elif cmd == "hbo":            run(c.launch_app("com.hbo.hbonow"))
        elif cmd == "hulu":           run(c.launch_app("hulu"))
        elif cmd == "prime":          run(c.launch_app("amazon"))
        elif cmd == "apple":          run(c.launch_app("com.apple.appletv"))
        elif cmd == "peacock":        run(c.launch_app("com.peacocktv.peacockus"))
        elif cmd == "spotify":        run(c.launch_app("com.spotify.TV"))
        elif cmd == "url":            run(c.open_url(val if val.startswith("http") else f"https://{val}"))
        elif cmd == "picture":        run(c.set_picture_mode(val))
        elif cmd == "sound":          run(c.set_sound_mode(val))
        elif cmd == "subs":           run(c.button("CC"))
        elif cmd == "sleep":          run(c.set_sleep_timer(int(val)))
        else:
            return jsonify({"error": f"Unknown command: {cmd}"}), 400

        return jsonify({"ok": True})
    except Exception as e:
        clients.pop(tv, None)  # reset connection on error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
