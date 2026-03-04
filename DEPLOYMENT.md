# 🚀 Deployment Guide - AI Hiring Assistant v0.1

Complete guide for deploying the AI Hiring Assistant to various environments.

## 📍 Deployment Options

| Option | Time | Cost | Skill Level | Best For |
|--------|------|------|-------------|----------|
| **Local Development** | 5 mins | Free | Beginner | Testing, Development |
| **Docker Locally** | 10 mins | Free | Beginner | Production-like testing |
| **Heroku** | 15 mins | Free-$7/mo | Beginner | Quick cloud hosting |
| **Railway** | 15 mins | $5/mo | Beginner | Modern deployment |
| **Render** | 15 mins | Free-$7/mo | Beginner | Simple hosting |
| **AWS (EC2)** | 30 mins | $5-20/mo | Intermediate | Professional setup |
| **DigitalOcean** | 20 mins | $5-12/mo | Intermediate | Reliable cloud |
| **Google Cloud Run** | 20 mins | Pay-per-use | Intermediate | Serverless option |
| **Docker Hub + K8s** | 45 mins | Varies | Advanced | Large scale |

---

## ⚡ Option 1: Local Deployment (5 minutes)

### Prerequisites
- Python 3.10+
- OpenAI API Key

### Steps

```bash
# 1. Navigate to project
cd c:\Users\Lenovo\Documents\learningFolder\Multiagentp1\crewai-project

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 6. Start API server (Terminal 1)
python -m src.api.main

# 7. Start Streamlit UI (Terminal 2)
streamlit run src/ui/streamlit_app.py
```

### Access
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501

---

## 🐳 Option 2: Docker Local Deployment (10 minutes)

### Prerequisites
- Docker Desktop installed
- OpenAI API Key

### Steps

```bash
# 1. Create .env file
copy .env.example .env
# Edit .env and add OPENAI_API_KEY

# 2. Build Docker images
docker-compose build

# 3. Start services
docker-compose up -d

# 4. Check logs
docker-compose logs -f api
docker-compose logs -f ui

# 5. Stop services (when done)
docker-compose down
```

### Access
- **API**: http://localhost:8000
- **Streamlit UI**: http://localhost:8501

### Useful Commands

```bash
# View all running containers
docker-compose ps

# Stop specific service
docker-compose stop api

# Remove all services and volumes
docker-compose down -v

# Rebuild without cache
docker-compose build --no-cache
```

---

## ☁️ Option 3: Heroku Deployment (15 minutes)

### Prerequisites
- Heroku Account (free)
- Heroku CLI installed
- OpenAI API Key

### Steps

```bash
# 1. Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login to Heroku
heroku login

# 3. Create Heroku app
heroku create your-app-name

# 4. Add environment variables
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set OPENAI_MODEL_NAME=gpt-4-turbo-preview

# 5. Create Procfile
echo "web: python -m src.api.main" > Procfile

# 6. Commit changes
git add Procfile
git commit -m "Add Heroku Procfile"

# 7. Deploy to Heroku
git push heroku main

# 8. View logs
heroku logs --tail

# 9. Open app
heroku open
```

### Create Procfile Content:
```
web: python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
worker: streamlit run src/ui/streamlit_app.py --server.port=$PORT
```

### Access
- **API**: https://your-app-name.herokuapp.com
- **API Docs**: https://your-app-name.herokuapp.com/docs

---

## 🚂 Option 4: Railway Deployment (15 minutes)

Railway is modern, simple, and offers free tier with GitHub integration.

### Prerequisites
- GitHub Account
- Railway Account (free - https://railway.app)
- OpenAI API Key

### Steps

```bash
# 1. Push code to GitHub (already done)
git push origin main

# 2. Go to Railway.app
# 3. Click "New Project"
# 4. Select "Deploy from GitHub repo"
# 5. Select your repository: Annaa74/Crew-Ai-Multi-agent-system
# 6. Authorize Railway
# 7. Click "Deploy Now"

# 8. Add Environment Variables
# In Railway Dashboard → Variables:
OPENAI_API_KEY=your_key_here
OPENAI_MODEL_NAME=gpt-4-turbo-preview
API_HOST=0.0.0.0
API_PORT=8000

# 9. Set Start Command
# Build: pip install -r requirements.txt
# Start: python -m src.api.main
```

### Access
- **API**: https://your-project.railway.app
- **API Docs**: https://your-project.railway.app/docs

---

## 🎨 Option 5: Render Deployment (15 minutes)

### Prerequisites
- Render Account (free - https://render.com)
- GitHub Account
- OpenAI API Key

### Steps

```bash
# 1. Go to render.com
# 2. Click "New +" → "Web Service"
# 3. Connect GitHub repository
# 4. Select: Annaa74/Crew-Ai-Multi-agent-system
# 5. Fill in details:
#    - Name: hiring-assistant
#    - Environment: Python 3
#    - Build Command: pip install -r requirements.txt
#    - Start Command: python -m src.api.main
#    - Instance Type: Free

# 6. Add Environment Variables
# OPENAI_API_KEY=your_key_here
# OPENAI_MODEL_NAME=gpt-4-turbo-preview

# 7. Click "Create Web Service"
# 8. Wait for deployment (2-3 minutes)
```

### Access
- **API**: https://hiring-assistant.onrender.com
- **API Docs**: https://hiring-assistant.onrender.com/docs

---

## 🌥️ Option 6: AWS EC2 Deployment (30 minutes)

### Prerequisites
- AWS Account
- EC2 instance (t3.micro free tier)
- OpenAI API Key

### Setup Steps

```bash
# 1. Launch EC2 Instance
# - Amazon Linux 2 or Ubuntu 22.04
# - Security Group: Allow ports 80, 443, 8000, 8501
# - Key Pair: Download and save

# 2. Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Update system
sudo yum update -y  # Amazon Linux
# OR
sudo apt update && sudo apt upgrade -y  # Ubuntu

# 4. Install Python and Git
sudo yum install python3-pip git -y
# OR
sudo apt install python3-pip git -y

# 5. Clone repository
git clone https://github.com/Annaa74/Crew-Ai-Multi-agent-system.git
cd Crew-Ai-Multi-agent-system

# 6. Install dependencies
pip install -r requirements.txt

# 7. Set environment variables
echo 'export OPENAI_API_KEY=your_key' >> ~/.bashrc
echo 'export OPENAI_MODEL_NAME=gpt-4-turbo-preview' >> ~/.bashrc
source ~/.bashrc

# 8. Install and start services with supervisor
sudo pip install supervisor

# Create supervisor config
sudo vi /etc/supervisor/conf.d/hiring-api.conf
```

### Supervisor Config:
```ini
[program:hiring-api]
command=/usr/bin/python3 -m src.api.main
directory=/home/ec2-user/Crew-Ai-Multi-agent-system
user=ec2-user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/hiring-api.log

[program:hiring-ui]
command=/usr/bin/streamlit run src/ui/streamlit_app.py --server.port=8501
directory=/home/ec2-user/Crew-Ai-Multi-agent-system
user=ec2-user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/hiring-ui.log
```

```bash
# 9. Start services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all

# 10. Setup Nginx reverse proxy
sudo yum install nginx -y
sudo systemctl start nginx
```

### Access
- **API**: http://your-instance-ip:8000
- **Streamlit UI**: http://your-instance-ip:8501

---

## 🌊 Option 7: DigitalOcean Droplet (20 minutes)

### Prerequisites
- DigitalOcean Account ($5/mo)
- OpenAI API Key

### Steps

```bash
# 1. Create Droplet
# - 512MB RAM / 1vCPU / 10GB SSD
# - Ubuntu 22.04 LTS
# - Add SSH key

# 2. SSH into droplet
ssh root@your-droplet-ip

# 3. Create non-root user
adduser appuser
usermod -aG sudo appuser

# 4. Update system
apt update && apt upgrade -y

# 5. Install Python and dependencies
apt install python3-pip python3-venv git -y

# 6. Clone repo
su - appuser
git clone https://github.com/Annaa74/Crew-Ai-Multi-agent-system.git
cd Crew-Ai-Multi-agent-system

# 7. Create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 8. Create systemd service
sudo tee /etc/systemd/system/hiring-api.service > /dev/null <<EOF
[Unit]
Description=AI Hiring Assistant API
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/home/appuser/Crew-Ai-Multi-agent-system
Environment="OPENAI_API_KEY=your_key"
ExecStart=/home/appuser/Crew-Ai-Multi-agent-system/venv/bin/python -m src.api.main
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 9. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable hiring-api
sudo systemctl start hiring-api

# 10. Check status
sudo systemctl status hiring-api
```

### Access
- **API**: http://your-droplet-ip:8000
- **API Docs**: http://your-droplet-ip:8000/docs

---

## 🔧 Deployment Checklist

### Before Deploying
- [ ] Code committed to GitHub
- [ ] `.env.example` created with all required variables
- [ ] `requirements.txt` updated
- [ ] OPENAI_API_KEY obtained from https://platform.openai.com/api-keys
- [ ] `README_v0.1.md` updated with metrics
- [ ] Tests pass locally
- [ ] Docker builds successfully

### After Deploying
- [ ] Health check passes: `/health` returns status 200
- [ ] API documentation loads: `/docs`
- [ ] Can create job analysis POST to `/api/v1/jobs/analyze`
- [ ] Can create resume analysis POST to `/api/v1/resumes/analyze`
- [ ] Streamlit UI loads (if deployed)
- [ ] Vector database persists data
- [ ] Logs accessible for debugging

---

## 📊 Performance Monitoring

### Health Checks

```bash
# Test API health
curl http://localhost:8000/health

# Test job analysis (after deploying)
curl -X POST http://localhost:8000/api/v1/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "TEST-001",
    "job_title": "Test Engineer",
    "job_text": "We need a Python developer with 5 years experience"
  }'

# View API documentation
open http://localhost:8000/docs
```

### Monitor Logs

```bash
# Docker
docker-compose logs -f api

# Heroku
heroku logs --tail

# EC2 / DigitalOcean
tail -f /var/log/hiring-api.log
```

---

## 🔐 Production Security

### Required Steps
1. **Use environment variables** for all secrets
2. **Enable HTTPS** with SSL certificate
3. **Set up authentication** for API
4. **Configure rate limiting**
5. **Enable CORS** only for trusted domains
6. **Backup vector database** regularly
7. **Monitor API usage** and costs

### Example Production Setup

```bash
# 1. Install SSL certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --nginx -d your-domain.com

# 2. Configure Nginx with SSL
sudo vi /etc/nginx/sites-available/hiring-api
```

### Nginx Config:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'crewai'"

**Solution:**
```bash
pip install --upgrade crewai crewai-tools
```

### Issue: "OPENAI_API_KEY not found"

**Solution:**
```bash
# Local
export OPENAI_API_KEY=sk-your-key-here
# OR add to .env file

# Docker
# Add to docker-compose.yml environment section

# Cloud (Heroku/Railway/Render)
# Add via dashboard → Environment Variables
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process and restart
kill -9 <PID>
python -m src.api.main
```

### Issue: "Vector database not persisting"

**Solution:**
```bash
# Check data directory exists
ls -la data/chroma/

# Fix permissions
chmod -R 755 data/

# Clear and recreate
rm -rf data/chroma/
curl http://localhost:8000/api/v1/admin/clear-db
```

---

## 💰 Cost Estimation

### Monthly Costs (Approximately)

| Option | Base | API Calls | Total |
|--------|------|-----------|-------|
| **Local** | $0 | $5-50 | ~$10 |
| **Heroku** | $7 | $5-50 | ~$15 |
| **Railway** | $5 | $5-50 | ~$12 |
| **Render** | $7 | $5-50 | ~$15 |
| **AWS** | $5 | $5-50 | ~$12 |
| **DigitalOcean** | $5 | $5-50 | ~$12 |
| **Google Cloud Run** | $0 | $5-50 | ~$8 |

*API costs depend on usage (OpenAI charges per request)*

---

## 🎯 Recommended Setup by Use Case

### **Development Team**
→ **Docker locally + GitHub**
- Easy testing and collaboration
- No cloud costs during development

### **Small Business / MVP**
→ **Railway or Render**
- Simple deployment
- Auto-scaling included
- Minimal configuration

### **Production / Professional**
→ **AWS EC2 + RDS + S3**
- Full control
- Scalable infrastructure
- Industry standard

### **Serverless / Cost-Optimized**
→ **Google Cloud Run + Firestore**
- Pay only for usage
- Auto-scales to zero
- Fast deployment

---

## 📚 Next Steps

1. **Choose deployment option** based on your needs
2. **Follow the step-by-step guide** above
3. **Test the API** with the health check endpoint
4. **Monitor performance** and costs
5. **Set up CI/CD** with GitHub Actions (already configured!)
6. **Scale up** when needed

---

## 🆘 Need Help?

- **GitHub Issues**: Report problems
- **API Docs**: http://localhost:8000/docs
- **Logs**: Check deployment logs for errors
- **Community**: See original crewAI repo for questions

---

**v0.1.0** | Ready to deploy! 🚀
