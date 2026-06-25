# SpacePoint - VPS Deployment Guide

This guide provides step-by-step instructions on deploying the SpacePoint website and its FastAPI admin dashboard backend on a Linux VPS (such as Ubuntu 20.04/22.04 LTS).

We will set up:
1. Python Virtual Environment.
2. **Systemd Service** to run the FastAPI app securely in the background.
3. **Nginx** as a reverse proxy.
4. **Certbot (Let's Encrypt)** for free SSL/HTTPS encryption.

---

## 📋 Prerequisites

*   A Linux VPS (Ubuntu 20.04 or 22.04 recommended).
*   A domain name pointing to your VPS IP address (e.g., `admin.spacepoint.ae` or `spacepoint.ae`).
*   SSH access to your server with `sudo` permissions.

---

## 🛠️ Step-by-Step Installation

### Step 1: Update System Packages & Install Dependencies
First, SSH into your VPS and update the system packages:
```bash
sudo apt update && sudo apt upgrade -y
```

Install Python, pip, virtualenv, Nginx, and Git:
```bash
sudo apt install -y python3-pip python3-venv python3-dev nginx git curl
```

---

### Step 2: Clone the Repository & Setup Directory
Navigate to `/var/www/` (common directory for web serving) and clone your repository (or copy your files here):
```bash
cd /var/www
# Replace with your actual repository URL or upload files directly
sudo git clone https://github.com/your-username/SpacePoint-LandingPage.git officialspacepoint
```

Change directory ownership to your login user (replace `ubuntu` with your username or `root:www-data` depending on setup):
```bash
sudo chown -R ubuntu:ubuntu /var/www/officialspacepoint
cd /var/www/officialspacepoint
```

Ensure the `/articles` folder exists and has proper write permissions (since the backend generates files here):
```bash
mkdir -p articles
chmod -R 775 articles
chmod 664 blog.html
```

---

### Step 3: Configure Python Virtual Environment
Create a virtual environment named `venv` inside the project root:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install required backend packages:
```bash
pip install --upgrade pip
pip install fastapi uvicorn jinja2 requests python-multipart
```

Deactivate the virtual environment for now:
```bash
deactivate
```

---

### Step 4: Configure Systemd Service
To keep the FastAPI server running persistently in the background and survive server reboots, create a systemd service file:

```bash
sudo nano /etc/systemd/system/officialspacepoint.service
```

Paste the following configuration into the editor (running on port `8004` to avoid conflicts):
```ini
[Unit]
Description=Official SpacePoint FastAPI Admin Backend
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/officialspacepoint
ExecStart=/var/www/officialspacepoint/venv/bin/uvicorn admin_backend.main:app --host 127.0.0.1 --port 8004
Restart=always
RestartSec=5
Environment="PATH=/var/www/officialspacepoint/venv/bin"

[Install]
WantedBy=multi-user.target
```
*Note: Ensure `User=root` and `Group=www-data` or your appropriate server user has read/write permissions to `/var/www/officialspacepoint`.*

Save and close the file (`Ctrl + O`, then `Enter`, then `Ctrl + X`).

Start the service and enable it to run on boot:
```bash
sudo systemctl daemon-reload
sudo systemctl start officialspacepoint
sudo systemctl enable officialspacepoint
```

Check the status of the service to verify it is running:
```bash
sudo systemctl status officialspacepoint
```

---

### Step 5: Configure Nginx Reverse Proxy
Create a new Nginx configuration file for your domain:
```bash
sudo nano /etc/nginx/sites-available/spacepoint.ae
```

Paste the following block (pointing to the admin backend on port `8004` to avoid port conflict):
```nginx
server {
    listen 80;
    server_name spacepoint.ae www.spacepoint.ae; # Add your domains here

    client_max_body_size 20M; # Allow image uploads up to 20MB

    location / {
        proxy_pass http://127.0.0.1:8004;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Save and exit.

Enable the configuration by creating a symlink:
```bash
sudo ln -s /etc/nginx/sites-available/spacepoint.ae /etc/nginx/sites-enabled/
```

Remove the default Nginx page (optional but recommended to avoid conflicts):
```bash
sudo rm /etc/nginx/sites-enabled/default
```

Test the Nginx configuration for syntax errors:
```bash
sudo nginx -t
```

If the test is successful, restart Nginx:
```bash
sudo systemctl restart nginx
```

---

### Step 6: Set Up SSL Certificate (HTTPS)
Install Certbot and its Nginx plugin:
```bash
sudo apt install -y certbot python3-certbot-nginx
```

Run Certbot to request and configure SSL certificates automatically:
```bash
sudo certbot --nginx -d spacepoint.ae -d admin.spacepoint.ae
```
Follow the interactive prompts (enter your email, agree to terms, and choose to **Redirect all HTTP traffic to HTTPS**).

Certbot will automatically update your Nginx configuration with the SSL certificates and configure auto-renewals.

---

## ⚡ Monitoring & Troubleshooting

### View Application Logs (Systemd)
To inspect the live FastAPI logs and database outputs:
```bash
sudo journalctl -u officialspacepoint -f
```

### Restart Application Server
If you push changes or manually update files:
```bash
sudo systemctl restart officialspacepoint
```

### Check Nginx Access/Error Logs
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```
