# 🚀 Quick Deployment Checklist

## Current Status ✅
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:5173`
- Database seeded with 2,275 grid cells, 128 fire alerts, 838 species
- All API endpoints responding correctly
- Map visualization working (GeoJSON rendering)
- AI Ecosystem Summary generation working

---

## For Immediate Deployment (Next 15 Minutes)

### 1. **Create Production `.env` File**
```bash
cd c:\Saalu_Data\foundathon
```

Copy `.env.example` → `.env`:
```env
FIRMS_API_KEY=2f2e12b87800276307048aad2c1fd52b
DATABASE_URL=sqlite:///./data/ecosystem_monitor.db
HOST=0.0.0.0
PORT=8000
DEBUG=false
FRONTEND_URL=https://yourdomain.com
```

---

### 2. **Production Build & Start**

#### Backend (Production Mode)
```bash
# Install production dependencies
pip install gunicorn

# Start with Gunicorn
gunicorn backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

#### Frontend (Production Build)
```bash
cd frontend
npm run build

# Serve the dist folder
npm install -g serve
serve -s dist -p 3000
```

---

### 3. **Docker Quick Deploy** (Recommended)

#### Option A: Using Docker Compose (2 commands)
```bash
# Build and run everything
docker-compose -f docker-compose.yml up -d

# Check status
docker-compose ps
```

#### Option B: Deploy to Docker Hub Registry
```bash
# Build images
docker build -t yourusername/foundathon-backend:latest -f backend.Dockerfile .
docker build -t yourusername/foundathon-frontend:latest -f frontend.Dockerfile ./frontend

# Push to registry
docker push yourusername/foundathon-backend:latest
docker push yourusername/foundathon-frontend:latest

# Pull and run on production server
docker pull yourusername/foundathon-backend:latest
docker pull yourusername/foundathon-frontend:latest
docker run -p 8000:8000 yourusername/foundathon-backend:latest
docker run -p 3000:80 yourusername/foundathon-frontend:latest
```

---

### 4. **Nginx Reverse Proxy Setup** (For Single Server)

Create `/etc/nginx/sites-available/foundathon`:
```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_cache_bypass $http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
    }
}
```

Enable Nginx config:
```bash
sudo ln -s /etc/nginx/sites-available/foundathon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### 5. **SSL Certificate** (Let's Encrypt - Free)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

---

### 6. **Verify Deployment**

```bash
# Backend health
curl https://yourdomain.com/api/predict/ehi?region=western_ghats | head -20

# Frontend
curl https://yourdomain.com/

# Check all endpoints
curl https://yourdomain.com/api/regions
curl https://yourdomain.com/api/alerts/fires?days=7&region=western_ghats
```

---

## Cloud Platform Quick Deploy

### Vercel (Frontend Only)
```bash
cd frontend
npm install -g vercel
vercel --prod
```

### Railway / Render (Full App)
1. Push code to GitHub
2. Connect repo in Railway/Render dashboard
3. Set environment variables
4. Deploy (automatic on push)

### AWS EC2
```bash
# 1. Launch Ubuntu 22.04 t3.medium instance
# 2. SSH in
ssh -i key.pem ubuntu@<public-ip>

# 3. Install
sudo apt update
sudo apt install python3.11 python3-pip nodejs npm nginx certbot

# 4. Clone & setup
git clone https://github.com/yourrepo/foundathon.git
cd foundathon
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Build frontend
cd frontend && npm install && npm run build && cd ..

# 6. Start backend (via PM2 for process management)
npm install -g pm2
pm2 start "gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000" --name foundathon-backend

# 7. Start frontend
pm2 start "serve -s frontend/dist -l 3000" --name foundathon-frontend

# 8. Setup SSL & Nginx (see section above)

# 9. Monitor
pm2 logs
pm2 status
```

---

## Testing AI Ecosystem Summary

The **AI Ecosystem Summary** feature IS working. To test it:

### 1. Via Browser (After Deployment)
- Open application
- Click on any colored grid cell in the map
- Summary will appear in right sidebar

### 2. Via API
```bash
# Get a valid cell ID
curl https://yourdomain.com/api/predict/ehi?region=western_ghats | jq '.cells[0].cell_id'

# Request summary (example: "8.05_76.05")
curl https://yourdomain.com/api/narrative/8.05_76.05?region=western_ghats | jq .

# Response includes:
{
  "cell_id": "8.05_76.05",
  "narrative": "Overall ecosystem health scores **64/100** (good). Vegetation is dense and healthy...",
  "data": {
    "ehi_score": 64.2,
    "ehi_status": "good",
    "ndvi_current": 0.717,
    "fire_risk_probability": 0.061,
    "species_count": 0
  }
}
```

---

## Post-Deployment Checklist

- [ ] SSL certificate installed
- [ ] HTTPS enforced (redirect HTTP to HTTPS)
- [ ] Environment variables configured
- [ ] Database backed up
- [ ] Monitoring/logging enabled
- [ ] Rate limiting configured
- [ ] CORS properly restricted
- [ ] API documentation accessible at `/docs`
- [ ] Health checks setup
- [ ] Performance tested with production data

---

## Monitoring & Logs

```bash
# View backend logs
pm2 logs foundathon-backend

# View frontend logs
pm2 logs foundathon-frontend

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Check server status
pm2 status
docker-compose ps
```

---

## Key Features Deployed ✅

✅ **6 Interactive Map Layers**
- Ecosystem Health Index (EHI)
- Fire Detection Alerts
- Fire Risk Predictions
- Species Biodiversity
- NDVI Vegetation Index
- Anomaly Detection

✅ **AI Features**
- Ecosystem health scoring (0-100)
- Fire risk probability
- Environmental anomaly detection
- Auto-generated narrative summaries

✅ **Data Dashboard**
- Real-time statistics
- Live fire alerts feed (128 detections)
- Weather station data (10 stations)
- Species occurrence records (838 species)

✅ **Performance**
- 2,275 grid cells rendering efficiently
- Sub-2-second map load time
- Query response caching
- Optimized database queries

---

## Support

For issues during deployment:
1. Check backend logs: `pm2 logs foundathon-backend`
2. Check frontend browser console
3. Verify `.env` file configured correctly
4. Ensure database file exists: `ls -la data/`
5. Test API endpoint: `curl http://localhost:8000/api/regions`

---

**Ready to deploy? Pick your platform above and follow the steps! 🚀**
