# saranglebah

**saranglebah** lets you broadcast keystrokes from a **master** computer to one or many **slave** computers in real‑time over your local Wi‑Fi / LAN.

## Features
* 🔑 Instant keystroke mirroring (UDP, low‑latency)
* 🧠 Simple CLI: `saranglebah master` or `saranglebah slave`
* 📜 Python‑only, cross‑platform (Windows, macOS, Linux)
* 📓 Built‑in logging (`saranglebah.log` in current directory)

## Quick Start

```bash
# On every machine
python -m pip install -r requirements.txt

# On the master (replace IPs with your slaves)
saranglebah master --slaves 192.168.1.101 192.168.1.102 192.168.1.103 192.168.1.104

# On each slave
saranglebah slave
```

### Options

```bash
saranglebah master --help
saranglebah slave --help
```

## How It Works

* The **master** captures key‑press events with `pynput` and broadcasts them as
  small JSON packets over UDP.
* Each **slave** listens on the same port (default **5050**), decodes each
  packet, and replays the keystroke locally.
* Only key‑press events are sent; the slave issues both press & release to mimic
  a tap (sufficient for most workflows).

## Security

Traffic is local‑network UDP, unencrypted by default. For sensitive setups,
consider running over an isolated Wi‑Fi network or VPN.

## License

MIT
