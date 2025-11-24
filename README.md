# Vital Mechanical Service Chatbot

A customer service chatbot for Vital Mechanical Service that embodies the company's core values and mission to provide helpful, accurate information to potential and existing customers.

## About Vital Mechanical Service

Since 2004, Vital Mechanical Service has been keeping Puget Sound's buildings running at peak performance. They provide expert maintenance, repair, and replacement for mechanical systems, plumbing, and controls.

### Core Values
- **Integrity** - Operating with honesty and strong moral principles
- **Positive Outlook** - Maintaining an optimistic, solution-focused attitude
- **Teamacity** - Combining teamwork with tenacity
- **Do the Right Thing** - Always choosing what's best for customers

### The Vital Way
A client-centric approach focused on:
- Saving customers time
- Anticipating customer needs
- Respecting customer property
- Communicating clearly

## Features

- **Context-Aware Responses** - Uses Claude AI to provide intelligent, context-aware answers
- **Company Knowledge** - Built-in knowledge of Vital Mechanical's services, values, and approach
- **Conversation Memory** - Maintains conversation history for natural dialogue
- **Professional Tone** - Reflects the company's professional, helpful, and solution-focused personality

## Installation

1. Clone or download this directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or on Windows:
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Command Line Demo

Run the interactive chatbot:
```bash
python chatbot.py
```

### As a Python Module

```python
from chatbot import VitalMechanicalChatbot

# Initialize the chatbot
bot = VitalMechanicalChatbot()

# Send a message
response = bot.chat("What services do you offer?")
print(response)

# Continue the conversation
response = bot.chat("Do you service commercial buildings?")
print(response)

# Reset conversation
bot.reset_conversation()
```

## Example Conversations

**Customer:** What services does Vital Mechanical provide?

**Bot:** We provide comprehensive mechanical services for commercial buildings, including:
- HVAC maintenance, repair, and replacement
- Refrigeration systems
- Plumbing services
- Building controls and automation
- Preventative maintenance programs
- And more...

**Customer:** What makes you different from other HVAC companies?

**Bot:** Great question! We've been serving the Puget Sound area since 2004, and we're more than just a service provider—we're a partner in keeping your building comfortable, safe, and efficient. Our approach, "The Vital Way," means we always put your best interests first by saving you time, anticipating your needs, respecting your property, and communicating clearly...

## Integration Options

This chatbot can be integrated into:

1. **Website Widget** - Add to the Vital Mechanical website for live customer support
2. **Email Support** - Use to draft responses to customer inquiries
3. **SMS/Text** - Integrate with Twilio for text-based support
4. **Slack/Teams** - Internal tool for staff to quickly access company information
5. **WhatsApp Business** - Customer support via WhatsApp

## Customization

### Updating Company Information

Edit `chatbot_config.py` to update:
- Services offered
- Core values
- Mission statement
- Notable clients
- Contact information

### Adjusting Chatbot Personality

Modify the `CHATBOT_SYSTEM_PROMPT` in `chatbot_config.py` to change:
- Tone and style
- Response length
- Level of formality
- Types of questions it handles

### Changing the AI Model

In `chatbot.py`, update the model parameter:
```python
response = self.client.messages.create(
    model="claude-sonnet-4-20250514",  # Change this
    # ... rest of parameters
)
```

## Best Practices

1. **Monitor Conversations** - Regularly review chatbot interactions to improve responses
2. **Update Information** - Keep company info current in `chatbot_config.py`
3. **Escalation Path** - Always provide a way for customers to reach a human
4. **Test Regularly** - Test with common customer questions to ensure quality

## License

This chatbot is designed specifically for Vital Mechanical Service.

## Support

For questions about the chatbot implementation, contact your development team.
For questions about Vital Mechanical services, visit https://www.vitalmechanical.com/
