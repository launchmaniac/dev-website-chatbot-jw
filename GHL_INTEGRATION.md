# GoHighLevel Integration Guide
## Connect Chatbot Lead Capture to GHL Workflows

**When to use this:** After the owner sees the chatbot and wants lead capture enabled.

---

## 🎯 Overview

Instead of building separate email/SMS systems, we'll send captured leads directly to your existing GHL account. Then GHL workflows handle:
- SMS to coordinator
- Email notifications
- Adding to CRM
- Creating opportunities
- Any other automations

**Benefits:**
- ✅ No additional SMS costs (you already pay for GHL)
- ✅ Everything in one system
- ✅ Coordinator can respond in GHL inbox
- ✅ Automatic CRM entry
- ✅ Can build complex workflows

---

## 🔧 Setup Steps

### Step 1: Get GHL Webhook URL (5 minutes)

1. **Log into GoHighLevel**

2. **Go to Settings → Integrations → Webhooks**

3. **Create New Webhook:**
   - Name: "Chatbot Lead Capture"
   - Method: POST
   - Copy the webhook URL (looks like: `https://services.leadconnectorhq.com/hooks/xxx`)

### Step 2: Update Chatbot Config (2 minutes)

In your Replit deployment, add environment variable:

```
GHL_WEBHOOK_URL = https://services.leadconnectorhq.com/hooks/YOUR_ACTUAL_URL
```

### Step 3: Enable Lead Capture Feature (1 minute)

In `chatbot_enhanced.py`, update:

```python
self.features = {
    "booking_enabled": False,
    "quotes_enabled": False,
    "lead_capture_enabled": True,  # Turn this ON
}
```

Restart the server.

---

## 📋 What Data Gets Sent to GHL

When a lead is captured, this JSON is sent to your webhook:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234",
  "service_interest": "HVAC Repair",
  "message": "My AC isn't cooling properly",
  "urgency": "urgent",
  "timestamp": "2025-01-15T10:30:00",
  "source": "website_chatbot"
}
```

---

## 🔄 GHL Workflow Setup

### Basic Workflow (5 minutes to set up)

**Trigger:** Webhook received

**Actions:**
1. **Create/Update Contact**
   - Name: {{name}}
   - Email: {{email}}
   - Phone: {{phone}}
   - Source: Website Chatbot

2. **Add Tag:** "Chatbot Lead"

3. **Send SMS to Coordinator**
   - To: [Your coordinator's number]
   - Message:
     ```
     🔔 New Lead from Website

     Name: {{name}}
     Service: {{service_interest}}
     Urgency: {{urgency}}

     Message: {{message}}

     Contact: {{phone}}
     ```

4. **Send Email to Coordinator**
   - To: [Coordinator email]
   - Subject: "New Lead: {{service_interest}}"
   - Body: [Format as you like]

5. **Create Opportunity** (optional)
   - Pipeline: Service Requests
   - Stage: New Lead
   - Value: [Based on service type]

### Advanced Workflow (10 minutes to set up)

Add conditional logic:

**If urgency = "emergency":**
- Send SMS to emergency coordinator
- Create high-priority opportunity
- Send immediate phone notification

**If urgency = "normal":**
- Send email only
- Add to regular pipeline
- Follow up in 24 hours

**If service_interest contains "commercial":**
- Route to commercial team
- Tag as commercial lead
- Different follow-up sequence

---

## 🧪 Testing the Integration

### Test 1: Send Test Lead from Chatbot

1. **Go to your chatbot** (on test page or live site)

2. **Trigger lead capture:**
   - "I need HVAC service"
   - Provide test contact info

3. **Check GHL:**
   - New contact created?
   - SMS received?
   - Email received?
   - Opportunity created?

### Test 2: Manual Webhook Test

Use this curl command to test webhook directly:

```bash
curl -X POST https://services.leadconnectorhq.com/hooks/YOUR_URL \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "555-9999",
    "service_interest": "Test Service",
    "message": "This is a test lead",
    "urgency": "normal",
    "timestamp": "2025-01-15T10:00:00",
    "source": "manual_test"
  }'
```

---

## 📊 Monitoring & Analytics

### In GHL Dashboard

**Track:**
- Number of chatbot leads
- Conversion rate (lead → booked job)
- Response time (lead captured → first contact)
- Revenue from chatbot leads

**Reports to Create:**
1. **Chatbot Leads by Day**
   - Filter: Tag = "Chatbot Lead"
   - Group by: Created Date

2. **Chatbot Lead Conversion**
   - Pipeline: Service Requests
   - Source: Website Chatbot
   - Status: Won/Lost

3. **Response Time**
   - Time from lead created → first coordinator contact

---

## 💡 Pro Tips

### Tip 1: Different Numbers for Different Urgencies

Set up routing logic:
- Emergency → Text emergency number
- Urgent → Text primary coordinator
- Normal → Email only

### Tip 2: Auto-Response to Customer

Add action in GHL workflow:
- Send SMS to {{phone}}
- Message: "Thanks for contacting Vital Mechanical! We received your request and will call you within 24 hours."

### Tip 3: Time-Based Routing

- After hours? → Send to on-call coordinator
- Business hours? → Send to regular coordinator
- Weekend? → Different workflow

### Tip 4: Lead Scoring

Assign scores based on:
- Urgency = emergency: +50 points
- Commercial property: +30 points
- Specific service request: +20 points
- Complete contact info: +10 points

---

## 🚨 Troubleshooting

### Webhook Not Receiving Data

**Check:**
1. Is GHL_WEBHOOK_URL set correctly in environment?
2. Is lead_capture_enabled = True?
3. Check Replit logs for errors
4. Test webhook URL directly with curl

### SMS Not Sending

**Check:**
1. Is coordinator phone number correct in GHL workflow?
2. Is SMS action enabled in workflow?
3. Check GHL SMS logs
4. Verify phone number format (include country code)

### Contact Not Being Created

**Check:**
1. Does contact already exist? (might be updating)
2. Check required fields in GHL
3. Verify webhook data format matches GHL expectations

---

## 💰 Cost Analysis

**Using GHL for notifications:**
- SMS: $0 (already included in your GHL plan)
- Email: $0 (already included)
- Webhook: $0 (unlimited)
- CRM: $0 (already included)

**Total additional cost: $0**

Compare to building separate:
- Twilio SMS: ~$0.01/message
- SendGrid: $0 (free tier)
- Custom CRM integration: Hours of work

**GHL integration is FREE and easier!**

---

## 📝 Quick Reference

**Enable lead capture:**
```python
# In chatbot_enhanced.py
self.features["lead_capture_enabled"] = True
```

**Add GHL webhook:**
```bash
# In Replit Secrets
GHL_WEBHOOK_URL = https://services.leadconnectorhq.com/hooks/xxx
```

**Test manually:**
```bash
curl -X POST [GHL_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com"...}'
```

---

## 🎯 Next Steps After Setup

1. ✅ Test with multiple scenarios
2. ✅ Monitor for a few days
3. ✅ Gather coordinator feedback
4. ✅ Optimize workflow based on usage
5. ✅ Add additional automations as needed

**Once this is working smoothly, you can explore:**
- Phase 2: Calendar integration (auto-booking)
- Phase 3: Quote generation
- Phase 4: Full CRM automation

---

**Ready to set this up? It should take about 15-20 minutes total once the owner gives the green light!**
