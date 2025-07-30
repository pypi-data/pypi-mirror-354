## ZoomeyeSearch
A powerful CLI tool that uses ZoomEye to search exposed services, gather intelligence, and automate reconnaissance.

### 📦 Docker Usage for `ZoomeyeSearch`

### ZoomeyeSearch Docker Help Menu
```
pugal@ubuntu:~/ZoomeyeSearch$ sudo docker run -it --rm zoomeyesearch --help
 ______                                              _____                           _     
|___  /                                             / ____|                         | |    
   / /   ___    ___   _ __ ___    ___  _   _   ___ | (___    ___   __ _  _ __   ___ | |__  
  / /   / _ \  / _ \ | '_ ` _ \  / _ \| | | | / _ \ \___ \  / _ \ / _` || '__| / __|| '_ \ 
 / /__ | (_) || (_) || | | | | ||  __/| |_| ||  __/ ____) ||  __/| (_| || |   | (__ | | | |
/_____| \___/  \___/ |_| |_| |_| \___| \__, | \___||_____/  \___| \__,_||_|    \___||_| |_|
                                        __/ |                                              
                                       |___/                                               

                     - RevoltSecurities

[10:59:09]  [WARN]: unable to get the latest version of zoomeyesearch
╭───────────────────────╮
│                       │
│    ZOOMEYE 🔎 HELP    │
│                       │
╰───────────────────────╯
DESCRIPTION

ZoomEye is a powerful cybersecurity search engine that enables searching for exposed devices, services, and vulnerabilities.
This CLI tool provides programmatic access to ZoomEye's capabilities for reconnaissance and threat intelligence.

GLOBAL OPTIONS

┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Option            ┃ Description                                         ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -fields, --fields │ Comma-separated list of fields to return in results │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -facet, --facet   │ Comma-separated list of facets to group results by  │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -mp, --max-page   │ Maximum number of pages to fetch (default: 5)       │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -limit, --limit   │ Maximum number of results to fetch (default: 2000)  │
├───────────────────┼─────────────────────────────────────────────────────┤
│ -o, --output      │ Output file to save results                         │
└───────────────────┴─────────────────────────────────────────────────────┘
MODES (zoomeye <global-options> <mode>)

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Mode        ┃ Description                                                      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ auth        │ Configure and save your ZoomEye API key for authenticated access │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ login       │ Verify your ZoomEye access level and API key validity            │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ asn         │ Search by Autonomous System Number (ASN)                         │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ ip          │ Search by IP address                                             │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ domain      │ Search by domain name                                            │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ org         │ Search by organization name                                      │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ cidr        │ Search by CIDR range                                             │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ service     │ Search by service name                                           │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ product     │ Search by product name                                           │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ enumerate   │ Enumerate subdomains or associated domains                       │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ geosearch   │ Search by geographic location (country, city, subdivision)       │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ faviconhash │ Search by favicon hash                                           │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ ssl         │ Advanced SSL certificate search                                  │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ stats       │ Get statistics for a specific field                              │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ search      │ Perform a raw ZoomEye search query                               │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ gpt         │ Access ZoomEye GPT features                                      │
├─────────────┼──────────────────────────────────────────────────────────────────┤
│ update      │ Check for updates to the ZoomEyesearch CLI tool                  │
└─────────────┴──────────────────────────────────────────────────────────────────┘
USAGE
zoomeye <global-options> <mode> 
```

#### 🔧 Build the Docker Image

```bash
sudo docker build -t zoomeyesearch .
```

#### 📖 Show Help Menu

```bash
sudo docker run -it --rm zoomeyesearch --help
```

---

### 🔐 Authenticate with ZoomEye

```bash
sudo docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/.zoomeyesearch:/root/.zoomeyesearch \
  -v $(pwd)/.config/Zoomeye:/root/.config/Zoomeye \
  zoomeyesearch auth
```

---

### 🔑 Login to ZoomEye

```bash
sudo docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/.zoomeyesearch:/root/.zoomeyesearch \
  -v $(pwd)/.config/Zoomeye:/root/.config/Zoomeye \
  zoomeyesearch login
```

---

### 🔎 Run a Scan (e.g., domain scan)

```bash
sudo docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/.zoomeyesearch:/root/.zoomeyesearch \
  -v $(pwd)/.config/Zoomeye:/root/.config/Zoomeye \
  zoomeyesearch --limit 5 domain -d hackerone.com
```

---

### 💾 Saving Output File

The `--output test.txt` will write inside the container by default.

To persist it on your host system, mount a local volume like so:

```bash
sudo docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/data \
  -v $(pwd)/.zoomeyesearch:/root/.zoomeyesearch \
  -v $(pwd)/.config/Zoomeye:/root/.config/Zoomeye \
  zoomeyesearch --output /data/test.txt --limit 2 domain -d hackerone.com
```

This saves `test.txt` to your current directory (`$(pwd)` on host).
