# Complete Replit Deployment Guide
## Deploy Your Custom Chatbot Backend (Free!)

This guide will walk you through deploying the enhanced chatbot with full control and extensibility.

---

## 🎯 What You're Building

**Phase 1 (Now):** Chatbot with lead capture
**Phase 2 (Later):** Add booking system
**Phase 3 (Later):** Add quote generator

All running on YOUR backend that you control.

---

## ⏱️ Time Required

- **First-time setup:** 30-45 minutes
- **Deploying updates:** 2-3 minutes
- **Adding new features:** We'll walk through it together

---

## 📋 Prerequisites

1. **Anthropic API Key**
   - Go to https://console.anthropic.com
   - Sign up (free)
   - Create an API key
   - Copy it somewhere safe

2. **Replit Account**
   - Go to https://replit.com
   - Sign up with GitHub or email (free)

3. **GitHub Account** (you already have this!)
   - We'll deploy directly from your repo

---

## 🚀 STEP 1: Deploy to Replit (15 minutes)

### 1.1: Create New Repl from GitHub

1. **Go to Replit:** https://replit.com

2. **Click "+ Create Repl"**

3. **Choose "Import from GitHub"**

4. **Enter your repo URL:**
   ```
   https://github.com/launchmaniac/dev-website-chatbot-jw
   ```

5. **Wait for import** (30 seconds - 1 minute)

6. **Replit will automatically detect it's a Python project**

### 1.2: Configure Environment Variables

1. **Click the "Secrets" tab** (🔒 lock icon on left sidebar)

2. **Add your API key:**
   - Key: `ANTHROPIC_API_KEY`
   - Value: [paste your Anthropic API key]
   - Click "Add new secret"

3. **That's it for secrets!**

### 1.3: Install Dependencies

1. **Replit should auto-detect `requirements.txt`**

2. **If not, click the Shell tab and run:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Wait for installation** (1-2 minutes)

### 1.4: Configure the Run Command

1. **Click the ".replit" file** (or create it if it doesn't exist)

2. **Add this content:**
   ```toml
   run = "python api_server_enhanced.py"
   language = "python3"

   [env]
   PORT = "5000"
   ```

3. **Save the file**

### 1.5: Start the Server!

1. **Click the big green "Run" button** at the top

2. **You should see:**
   ```
   ✅ API key found
   🚀 Starting Enhanced Vital Mechanical Chatbot API
      Port: 5000
      Features: Lead Capture ✅ | Booking ⏳ | Quotes ⏳
   ```

3. **If you see errors:**
   - Check that ANTHROPIC_API_KEY is set correctly
   - Check that all files uploaded properly
   - Look for specific error messages

### 1.6: Get Your API URL

1. **Look for the "Webview" pane** (usually opens automatically)

2. **Your API URL will be something like:**
   ```
   https://dev-website-chatbot-jw.username.repl.co
   ```

3. **Copy this URL** - you'll need it!

4. **Test it by visiting:**
   ```
   https://your-url.repl.co/health
   ```

5. **You should see:**
   ```json
   {
     "status": "healthy",
     "service": "vital-mechanical-chatbot",
     "timestamp": "..."
   }
   ```

---

## 🧪 STEP 2: Test Your Backend (10 minutes)

### 2.1: Test the API Endpoints

Open the Replit Shell and test each endpoint:

**1. Health Check:**
```bash
curl https://your-url.repl.co/health
```

**2. Get Features:**
```bash
curl https://your-url.repl.co/api/features
```

**3. Test Chat (using curl):**
```bash
curl -X POST https://your-url.repl.co/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?", "session_id": "test123"}'
```

You should get a JSON response with the bot's answer!

### 2.2: Test Lead Capture

**Send a message that triggers lead capture:**
```bash
curl -X POST https://your-url.repl.co/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need HVAC service. My name is John Doe, email john@example.com, phone 555-1234", "session_id": "test123"}'
```

**Check if lead was captured:**
```bash
curl https://your-url.repl.co/api/leads
```

You should see your test lead!

### 2.3: Test the Widget

1. **In Replit, navigate to `web_widget_enhanced.html`**

2. **Edit line 323** (look for `API_ENDPOINT`):
   ```javascript
   const API_ENDPOINT = 'https://YOUR-REPL-URL.repl.co/api/chat';
   ```
   Replace with your actual Repl URL

3. **Save the file**

4. **Open the widget:**
   - Visit: `https://your-url.repl.co/widget`
   - OR click "Open website" in Replit

5. **Test the chat:**
   - Try "What services do you offer?"
   - Try "I need HVAC service" and provide contact info
   - Verify it works!

---

## 🌐 STEP 3: Deploy to Website (15 minutes)

### 3.1: Prepare the Embed Code

Create a file called `embed_code.html` with this content:

```html
<!-- Vital Mechanical Chatbot Widget -->
<div id="vital-chatbot-widget"></div>
<script>
  (function() {
    // Configuration
    const CHATBOT_API = 'https://YOUR-REPL-URL.repl.co/api/chat';
    const SESSION_ID = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

    // Load the widget
    const script = document.createElement('script');
    script.src = 'https://YOUR-REPL-URL.repl.co/static/widget.js';
    script.async = true;
    document.body.appendChild(script);
  })();
</script>
<link rel="stylesheet" href="https://YOUR-REPL-URL.repl.co/static/widget.css">
```

### 3.2: Add to Website

**For Wix:**
1. Open Wix Editor
2. Click Settings → Custom Code
3. Click "Add Custom Code"
4. Paste the embed code
5. Choose "Body - End"
6. Apply to all pages
7. Save and Preview

**For WordPress:**
1. Install "Insert Headers and Footers" plugin
2. Go to Settings → Insert Headers and Footers
3. Paste code in "Footer" section
4. Save

**For Custom Site:**
1. Add the embed code before `</body>` tag
2. Deploy

### 3.3: Test on Live Site

1. **Visit your website**
2. **Look for chat bubble** in bottom-right
3. **Test the chatbot:**
   - Ask questions
   - Try lead capture
   - Test on mobile

---

## 📊 STEP 4: Monitor & Manage (Ongoing)

### View Captured Leads

**Option 1: API Endpoint**
```
https://your-url.repl.co/api/leads
```

**Option 2: Download CSV**
```
https://your-url.repl.co/api/leads/export
```

**Option 3: Create Admin Dashboard (Later)**
We can build a simple dashboard to view/manage leads.

### View Statistics

```
https://your-url.repl.co/api/stats
```

Shows:
- Total leads
- Leads by urgency
- Leads by service type
- Recent activity

---

## 🔧 Maintenance & Updates

### Keeping Replit Alive

**Problem:** Free Replit instances sleep after inactivity.

**Solutions:**

1. **Upgrade to Always On** ($7/month per Repl)

2. **Use a Free Ping Service:**
   - Go to https://uptimerobot.com (free)
   - Add your Repl URL
   - Ping every 5 minutes
   - Keeps it awake for free

3. **Use Replit's Built-in Always On** (if available in your tier)

### Updating the Chatbot

1. **Make changes in GitHub repo**
2. **In Replit, click "Version Control"**
3. **Click "Pull"**
4. **Restart the server**

That's it!

---

## 🎨 Customization

### Change Colors

Edit `web_widget_enhanced.html`:
- Line 70: Change `#2563eb` (blue) to your color
- Save and refresh

### Change Greeting Message

Edit `chatbot_config.py`:
- Update `CHATBOT_SYSTEM_PROMPT`
- Save and restart server

### Add More Quick Questions

Edit `web_widget_enhanced.html`:
- Find the `quick-questions` section
- Add more buttons
- Save

---

## 🚀 PHASE 2: Adding Booking System (Future)

When you're ready to add booking:

1. **Choose booking system:**
   - Calendly API
   - Acuity Scheduling
   - Google Calendar API
   - Custom solution

2. **Enable the feature:**
   ```python
   chatbot.enable_feature("booking_enabled")
   ```

3. **Implement `_schedule_service()` function**
   - We'll code this together when ready

4. **Test thoroughly**

5. **Deploy update**

---

## 🚀 PHASE 3: Adding Quote System (Future)

When you're ready to add quotes:

1. **Design quote logic:**
   - Service type → base price
   - Building size → multiplier
   - Custom factors

2. **Enable the feature:**
   ```python
   chatbot.enable_feature("quotes_enabled")
   ```

3. **Implement `_request_quote()` function**
   - We'll code this together when ready

4. **Test thoroughly**

5. **Deploy update**

---

## ❗ Troubleshooting

### Chatbot Not Responding

1. **Check API key:**
   ```bash
   echo $ANTHROPIC_API_KEY
   ```

2. **Check server logs** in Replit Console

3. **Verify endpoint** is accessible:
   ```bash
   curl https://your-url.repl.co/health
   ```

### CORS Errors

- Already handled by `flask-cors`
- If issues persist, check browser console (F12)

### Lead Capture Not Working

1. **Check if `data` directory exists** in Replit
2. **Verify leads.json file** is being created
3. **Check API endpoint:** `/api/leads`

### Widget Not Appearing

1. **Check browser console** (F12) for errors
2. **Verify embed code** has correct API URL
3. **Check if scripts are blocked** by ad blockers
4. **Test in incognito mode**

---

## 🎉 Success Checklist

Before showing the owner:

- [ ] Backend deployed to Replit
- [ ] API endpoints working
- [ ] Widget appears on website
- [ ] Can send messages
- [ ] Responses are accurate
- [ ] Lead capture works
- [ ] Tested on desktop
- [ ] Tested on mobile
- [ ] No console errors
- [ ] Looks professional
- [ ] Ready to impress! 🚀

---

## 📞 Next Steps

1. **Deploy the backend** (follow steps above)
2. **Test thoroughly** (don't skip this!)
3. **Add to website** (start with test page)
4. **Monitor performance** (check stats daily)
5. **Iterate and improve** (add features as needed)

**When you're ready to add booking/quotes, we'll build those together!**

---

## 💡 Pro Tips

1. **Start simple:** Get the basic chatbot working first
2. **Test extensively:** Use it yourself for a few days
3. **Gather feedback:** Show to colleagues before the owner
4. **Document everything:** Keep notes on what works
5. **Plan phase 2:** Think about what features add most value

---

**Let's deploy this! Tell me when you're ready to start, and we'll go through it step by step together.** 🚀
