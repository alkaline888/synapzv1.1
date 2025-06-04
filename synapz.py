import os
import json
import importlib.util
import asyncio
from telethon import TelegramClient, events
import syn_utils  # C++ module via pybind11

CRED_FILE = "files/creds.json"
MODULE_DIR = "files/modules"
client = None
modules = {}

# Ensure files/modules exists
os.makedirs(MODULE_DIR, exist_ok=True)

def load_creds():
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, "r") as f:
            return json.load(f)
    else:
        creds = {
            "api_id": input("Enter API ID: "),
            "api_hash": input("Enter API Hash: "),
            "phone": input("Enter Phone Number: ")
        }
        with open(CRED_FILE, "w") as f:
            json.dump(creds, f, indent=4)
        return creds

def register_module(code):
    lines = code.splitlines()
    meta = {k: "unknown" for k in ["name", "author", "description"]}
    body_lines = []

    for line in lines:
        if line.startswith("#$"):
            try:
                k, v = line[2:].split("=", 1)
                meta[k.strip()] = v.strip()
            except:
                pass
        else:
            body_lines.append(line)

    mod_name = meta["name"]
    if not mod_name:
        print("❌ No module name declared.")
        return

    try:
        exec("\n".join(body_lines), globals())
        modules[mod_name] = meta
        print(f"✅ Loaded {mod_name} by {meta['author']}")
    except Exception as e:
        print(f"❌ Error in {mod_name}: {e}")

async def setup_telethon():
    global client
    creds = load_creds()
    client = TelegramClient("session", creds["api_id"], creds["api_hash"])
    await client.start(creds["phone"])
    return client

@events.register(events.NewMessage(outgoing=True, pattern=r"^\.ping$"))
async def ping_handler(event):
    await event.reply("🏓 Pong!")

@events.register(events.NewMessage(outgoing=True, pattern=r"^\.register$"))
async def register_handler(event):
    count = 0
    for fname in os.listdir(MODULE_DIR):
        if fname.endswith(".py"):
            with open(os.path.join(MODULE_DIR, fname), "r") as f:
                code = f.read()
            register_module(code)
            await event.reply(f"🔁 loaded {fname}")
            count += 1
    await event.reply(f"✅ {count} module(s) registered.")

@events.register(events.NewMessage(outgoing=True, pattern=r"^\.menu$"))
async def menu_handler(event):
    await event.reply("📥 Choose: .loadurl <URL>")

@events.register(events.NewMessage(outgoing=True, pattern=r"^\.loadurl (.+)$"))
async def loadurl_handler(event):
    url = event.pattern_match.group(1)
    try:
        meta = syn_utils.download_and_parse_module(url)
        code = meta.get("content", "")
        register_module(code)
        await event.reply(f"✅ Module {meta.get('name')} loaded")
    except Exception as e:
        await event.reply(f"❌ Failed: {e}")

def main():
    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(setup_telethon())
    client.add_event_handler(ping_handler)
    client.add_event_handler(register_handler)
    client.add_event_handler(menu_handler)
    client.add_event_handler(loadurl_handler)
    print("🤖 Synapz userbot running.")
    client.run_until_disconnected()

if __name__ == "__main__":
    main()
