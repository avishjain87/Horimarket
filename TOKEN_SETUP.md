# 🚀 Horimarket - Telegram Bot + Railway Deployment

## ⚡ Quick Start (5 Minutes)

### Step 1: Get Telegram Bot Token
1. Open Telegram → Search **@BotFather**
2. Send `/newbot` command
3. Follow instructions to create bot
4. **Copy the token** (example: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Step 2: Get Your Chat ID
1. Message your bot with `/start`
2. Go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Replace `<YOUR_TOKEN>` with your actual token
4. Find your **chat_id** in the response

### Step 3: Create `.env` File
Create a `.env` file in the root directory:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=987654321
FLASK_ENV=production
PORT=5000
```

**Replace with your actual values:**
- `TELEGRAM_BOT_TOKEN` → Your token from BotFather
- `TELEGRAM_CHAT_ID` → Your chat ID from getUpdates

### Step 4: Run Locally

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Start Flask App:**
```bash
python app.py
```
Open: http://localhost:5000

**Start Telegram Bot (in another terminal):**
```bash
python bot.py
```

---

## 🚄 Deploy to Railway

### Option A: Via Railway Dashboard
1. Go to https://railway.app
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select **avishjain87/Horimarket**
4. Add Environment Variables:
   - `TELEGRAM_BOT_TOKEN` = Your token
   - `TELEGRAM_CHAT_ID` = Your chat ID
5. Railway auto-detects `Procfile` and deploys both services

### Option B: Via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link project
railway link

# Add environment variables
railway variables set TELEGRAM_BOT_TOKEN=your_token
railway variables set TELEGRAM_CHAT_ID=your_chat_id

# Deploy
railway up
```

---

## 📊 Services Deployed

**Web Service** (Flask API):
- URL: Your Railway domain
- Endpoints: `/api/markets`, `/api/analyze/<symbol>`, etc.

**Bot Service** (Telegram Bot):
- Sends market analysis every 5 minutes
- Runs during market hours (8 AM - 11 PM)

---

## 🔑 Important Notes

⚠️ **Never commit `.env` file to GitHub!** (Already in `.gitignore`)

✅ **Safe Methods:**
- Use Railway environment variables (recommended)
- Use GitHub Secrets for CI/CD
- Use local `.env` file only for development

---

## ✅ Verify Everything Works

**Check Flask is running:**
```bash
curl http://localhost:5000/api/health
```

**Check Bot is sending messages:**
- Monitor Railway logs
- Should see "Report sent successfully ✅"

---

## 📞 Support

**Need help?**
- Check logs in Railway dashboard
- Verify token is correct
- Ensure bot can access internet
- Check market hours (8-23)

**Happy Trading! 📈**
