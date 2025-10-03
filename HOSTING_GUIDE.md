# 🚀 Hosting Guide - Background Service Deployment

## 🎯 **Hosting Options for Background Process**

Since this is a **background service** that needs to run 24/7, here are the best hosting options:

## 🏆 **Recommended Options (Best Value):**

### **1. DigitalOcean Droplet ($5/month)**
```bash
# Setup Steps:
1. Create DigitalOcean account
2. Create new droplet (Ubuntu 22.04)
3. SSH into server
4. Install Python 3.9+
5. Upload your code
6. Install dependencies
7. Run as background service
```

**Pros:**
- ✅ **Full control** over the environment
- ✅ **Reliable** - 99.99% uptime
- ✅ **Cost-effective** - $5/month
- ✅ **Easy scaling** if needed
- ✅ **SSH access** for monitoring

**Setup Command:**
```bash
# On your DigitalOcean server:
git clone your-repo
cd ImageTextGenerator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python simple_alt_generator.py
```

### **2. Railway (Free Tier Available)**
```bash
# Setup Steps:
1. Connect GitHub repository
2. Railway auto-detects Python
3. Sets environment variables
4. Deploys automatically
5. Runs as background service
```

**Pros:**
- ✅ **Free tier** available
- ✅ **Automatic deployment** from Git
- ✅ **Easy environment management**
- ✅ **Built-in monitoring**
- ✅ **No server management**

**Deployment:**
```bash
# Just push to GitHub:
git add .
git commit -m "Deploy to Railway"
git push origin main
# Railway handles the rest!
```

### **3. Render (Free Tier Available)**
```bash
# Setup Steps:
1. Connect GitHub repository
2. Create new "Background Worker"
3. Set build command: pip install -r requirements.txt
4. Set start command: python simple_alt_generator.py
5. Deploy
```

**Pros:**
- ✅ **Free tier** for background workers
- ✅ **GitHub integration**
- ✅ **Automatic deployments**
- ✅ **Built-in logging**
- ✅ **SSL certificates**

## 💰 **Cost Comparison:**

| Hosting Option | Monthly Cost | Free Tier | Setup Complexity |
|----------------|--------------|-----------|------------------|
| **DigitalOcean** | $5 | ❌ | Medium |
| **Railway** | $0-5 | ✅ | Easy |
| **Render** | $0-7 | ✅ | Easy |
| **AWS EC2** | $0-10 | ✅ | Complex |
| **Google Cloud** | $0-10 | ✅ | Complex |

## 🚀 **Quick Deployment Options:**

### **Option A: Railway (Easiest)**
1. **Push code to GitHub**
2. **Connect to Railway**
3. **Set environment variables**
4. **Deploy automatically**

### **Option B: Render (Also Easy)**
1. **Push code to GitHub**
2. **Create Background Worker on Render**
3. **Set build/start commands**
4. **Deploy**

### **Option C: DigitalOcean (Most Control)**
1. **Create droplet**
2. **SSH into server**
3. **Install and run manually**

## 🔧 **Environment Variables Setup:**

### **Required Variables:**
```bash
# Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS='{"type":"service_account",...}'

# Zoho Sheets (when you get credentials)
ZOHO_CLIENT_ID=your_zoho_client_id
ZOHO_CLIENT_SECRET=your_zoho_client_secret
ZOHO_REFRESH_TOKEN=your_zoho_refresh_token

# Optional Settings
SCHEDULE_TIME=09:00
LOG_LEVEL=INFO
```

## 📊 **System Requirements:**

### **Minimum Requirements:**
- **CPU**: 1 core
- **RAM**: 512MB
- **Storage**: 1GB
- **Python**: 3.9+

### **Recommended:**
- **CPU**: 1-2 cores
- **RAM**: 1GB
- **Storage**: 2GB
- **Python**: 3.9+

## 🔄 **Running as Background Service:**

### **On Linux/Mac (DigitalOcean, VPS):**
```bash
# Using systemd (recommended):
sudo nano /etc/systemd/system/alt-text-generator.service

[Unit]
Description=SEO Alt Text Generator
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/ImageTextGenerator
ExecStart=/path/to/ImageTextGenerator/.venv/bin/python simple_alt_generator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start:
sudo systemctl enable alt-text-generator
sudo systemctl start alt-text-generator
```

### **On Cloud Platforms (Railway, Render):**
- **Automatic** - platform handles background process
- **Auto-restart** on crashes
- **Logging** built-in
- **Monitoring** available

## 📋 **Deployment Checklist:**

### **Pre-Deployment:**
- ✅ **Code tested locally**
- ✅ **Environment variables ready**
- ✅ **API keys obtained**
- ✅ **Sheet IDs configured**
- ✅ **Dependencies listed in requirements.txt**

### **During Deployment:**
- ✅ **Set environment variables**
- ✅ **Install dependencies**
- ✅ **Test configuration loading**
- ✅ **Verify API connections**
- ✅ **Start background service**

### **Post-Deployment:**
- ✅ **Monitor logs for errors**
- ✅ **Test daily schedule**
- ✅ **Verify sheet processing**
- ✅ **Set up monitoring/alerts**

## 🚨 **Monitoring & Maintenance:**

### **Log Monitoring:**
```bash
# Check logs (if using systemd):
sudo journalctl -u alt-text-generator -f

# Check logs (if running manually):
tail -f background_service.log
```

### **Health Checks:**
```bash
# Check if service is running:
ps aux | grep simple_alt_generator

# Test API connections:
python test_simple.py
```

### **Maintenance Tasks:**
- **Weekly**: Check logs for errors
- **Monthly**: Review processing statistics
- **Quarterly**: Update dependencies
- **As needed**: Add new sheets to configuration

## 🎯 **Recommended Deployment Strategy:**

### **For Production Use:**
1. **Start with Railway/Render** (free tier)
2. **Test thoroughly** for 1-2 weeks
3. **Monitor performance** and reliability
4. **Upgrade to paid tier** if needed
5. **Consider DigitalOcean** for more control

### **For Development/Testing:**
1. **Use free tiers** (Railway/Render)
2. **Test with sample data**
3. **Verify daily automation**
4. **Monitor logs and performance**

## 📞 **Support & Troubleshooting:**

### **Common Issues:**
1. **Service not starting** - Check environment variables
2. **API errors** - Verify API keys and permissions
3. **Sheet access denied** - Check service account permissions
4. **Memory issues** - Upgrade to higher tier

### **Getting Help:**
- **Check logs** for error messages
- **Verify API connections** with test script
- **Contact hosting support** for platform issues
- **Review documentation** for configuration help

## 🎉 **Ready to Deploy!**

**Choose your hosting option:**
- 🚀 **Railway** - Easiest deployment, free tier
- 🚀 **Render** - Also easy, good free tier
- 🚀 **DigitalOcean** - Most control, $5/month

**All options will run your background service 24/7 and process sheets daily!**

---

**Next Steps:**
1. Choose hosting option
2. Set up environment variables
3. Deploy the service
4. Test with your sheets
5. Monitor daily automation
