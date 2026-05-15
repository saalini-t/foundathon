# Ecosystem & Biodiversity Monitoring Platform - Deployment Guide

## Project Summary
**AI-Powered Biodiversity & Environmental Intelligence for Western Ghats**
- Real-time ecosystem health monitoring
- Fire detection & risk prediction  
- Species biodiversity tracking
- NDVI vegetation analysis
- Weather observation integration

---

## System Requirements

### Backend
- **Python 3.11+**
- **FastAPI** 0.104+
- **SQLAlchemy** 2.0+
- **Uvicorn** ASGI server

### Frontend
- **Node.js 18+**
- **React 18+**
- **TypeScript**
- **Vite 5+**

---

## Deployment Steps

### Step 1: Environment Setup

Create `.env` file in the project root:

```bash
# ============================================
# Western Ghats Ecosystem Monitor - Environment
# ============================================

# NASA FIRMS API Key (get from https://firms.modaps.eosdis.nasa.gov/api/)
FIRMS_API_KEY=your_nasa_api_key_here

# Database (SQLite for local, PostgreSQL for production)
DATABASE_URL=sqlite:///./data/ecosystem_monitor.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# CORS (update frontend URL for production)
FRONTEND_URL=http://localhost:5173
```

**For Production**, update:
```env
FRONTEND_URL=https://yourdomain.com
DEBUG=false
DATABASE_URL=postgresql://user:password@host/dbname
```

---

### Step 2: Backend Deployment

#### A. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### B. Initialize Database
```bash
python -m backend.scripts.seed_demo
```

#### C. Run Backend Server

**Development:**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Production (using Gunicorn + Uvicorn):**
```bash
pip install gunicorn
gunicorn backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

**Verify Backend:**
```bash
curl http://localhost:8000/api/predict/ehi?region=western_ghats
```
Expected: JSON with EHI scores for 2,275 grid cells

---

### Step 3: Frontend Deployment

#### A. Install Dependencies
```bash
cd frontend
npm install
```

#### B. Build for Production
```bash
npm run build
```

Output: `dist/` folder with optimized static files

#### C. Run Frontend

**Development:**
```bash
npm run dev
# Runs on http://localhost:5173
```

**Production - Static Hosting:**
```bash
# Option 1: Serve dist/ folder with any static server
npm install -g serve
serve -s dist -l 5173

# Option 2: Deploy dist/ to CDN or static hosting
# (Vercel, Netlify, AWS S3 + CloudFront, etc.)
```

---

## Deployment Architectures

### Option 1: Single Server (AWS EC2 / DigitalOcean / VPS)

```
┌─────────────────────────────────┐
│   Server (Linux VM)             │
├─────────────────────────────────┤
│ Nginx (Reverse Proxy)           │
│  - Port 80 (HTTP)               │
│  - Port 443 (HTTPS)             │
├─────────────────────────────────┤
│ Frontend (Gunicorn + Vite)      │
│  - Port 3000 (internal)         │
├─────────────────────────────────┤
│ Backend (Gunicorn + Uvicorn)    │
│  - Port 8000 (internal)         │
├─────────────────────────────────┤
│ Database (SQLite/PostgreSQL)    │
└─────────────────────────────────┘
```

**Nginx Configuration Example:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Docker Deployment

**Dockerfile.backend:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "backend.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

**Dockerfile.frontend:**
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: sqlite:///./data/ecosystem_monitor.db
      FIRMS_API_KEY: ${FIRMS_API_KEY}
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
      - frontend
```

**Deploy Docker:**
```bash
docker-compose up -d
```

### Option 3: Cloud Platforms

#### Vercel (Frontend)
```bash
npm install -g vercel
cd frontend
vercel --prod
```

Environment variables needed:
```
VITE_API_URL=https://api.yourdomain.com
```

#### Render / Railway / Fly.io (Backend)
- Connect GitHub repo
- Set environment variables
- Deploy automatically on push

---

## API Endpoints

### Map & Data
- `GET /api/map/boundary?region=western_ghats` - Western Ghats boundary GeoJSON
- `GET /api/regions` - Available regions

### Predictions
- `GET /api/predict/ehi?region=western_ghats` - Ecosystem Health Index for all cells
- `GET /api/predict/fire-risk?region=western_ghats` - Fire risk predictions
- `GET /api/predict/anomalies?region=western_ghats` - Anomaly detection

### Alerts & Data
- `GET /api/alerts/fires?days=7&region=western_ghats` - Fire alerts (last N days)
- `GET /api/data/stats?region=western_ghats` - Summary statistics
- `GET /api/data/species/summary?limit=50&region=western_ghats` - Top species
- `GET /api/data/weather/current?region=western_ghats` - Current weather

### Narratives
- `GET /api/narrative/{cell_id}?region=western_ghats` - AI-generated ecosystem summary

---

## Monitoring & Maintenance

### Health Checks
```bash
# Backend health
curl http://localhost:8000/openapi.json

# Frontend health
curl http://localhost:5173/
```

### Logs
```bash
# Backend
tail -f /var/log/foundathon/backend.log

# Frontend  
tail -f /var/log/foundathon/frontend.log
```

### Database Backup
```bash
# SQLite backup
cp data/ecosystem_monitor.db data/ecosystem_monitor.db.backup.$(date +%s)

# PostgreSQL backup (production)
pg_dump ecosystem_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

---

## Performance Optimization

### Frontend
- ✅ GeoJSON rendering for 2,275+ grid cells (optimized from individual rectangles)
- ✅ TanStack Query caching for API responses
- ✅ Lazy loading of map layers
- ✅ Code splitting with Vite

### Backend
- ✅ SQLAlchemy query caching
- ✅ NDVI connector vectorized operations
- ✅ Parallel ML model computation (EHI, fire risk, anomalies)
- ✅ Database indexing on frequently queried fields

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # macOS/Linux

# Kill process
taskkill /PID <PID> /F  # Windows
kill -9 <PID>           # macOS/Linux
```

### CORS Errors
Update `.env` FRONTEND_URL to match your deployment domain

### Database Errors
```bash
# Reset database
rm data/ecosystem_monitor.db
python -m backend.scripts.seed_demo
```

### API 500 Errors
Check backend logs:
```bash
python -m uvicorn backend.main:app --reload --log-level debug
```

---

## Security Checklist

- [ ] HTTPS enabled (Let's Encrypt SSL)
- [ ] API rate limiting configured
- [ ] CORS properly restricted to frontend domain
- [ ] Environment variables not committed to Git
- [ ] Database credentials stored securely
- [ ] API authentication (consider JWT for production)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (SQLAlchemy ORM handles this)

---

## Production Deployment Example (AWS EC2)

```bash
#!/bin/bash
# deploy.sh

# 1. SSH into EC2 instance
# ssh -i key.pem ubuntu@<instance-ip>

# 2. Clone repository
git clone https://github.com/your-org/foundathon.git
cd foundathon

# 3. Install dependencies
sudo apt update
sudo apt install python3.11 python3-pip nodejs npm nginx

# 4. Create .env file
cat > .env << EOF
FIRMS_API_KEY=your_key_here
DATABASE_URL=sqlite:///./data/ecosystem_monitor.db
FRONTEND_URL=https://yourdomain.com
DEBUG=false
EOF

# 5. Backend setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m backend.scripts.seed_demo

# 6. Frontend build
cd frontend
npm install
npm run build
cd ..

# 7. Start backend (systemd service)
sudo tee /etc/systemd/system/foundathon-backend.service > /dev/null <<EOL
[Unit]
Description=Foundathon Backend
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/foundathon
ExecStart=/home/ubuntu/foundathon/venv/bin/gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
EOL

# 8. Start frontend (serve dist folder)
cd frontend/dist
python3 -m http.server 3000 &

# 9. Configure Nginx
# (use the Nginx config example above)

# 10. Enable SSL
sudo snap install certbot --classic
sudo certbot certonly --nginx -d yourdomain.com

# 11. Start services
sudo systemctl start foundathon-backend
sudo systemctl enable foundathon-backend
sudo systemctl restart nginx
```

---

## Support & Documentation

- **API Docs:** `http://localhost:8000/docs` (Swagger UI)
- **GitHub:** [your-repo-url]
- **Issues:** Report on GitHub
- **Contact:** support@foundathon.io

