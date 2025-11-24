"""
Vital Mechanical Service Chatbot
A customer service chatbot that embodies the company's core values and mission
"""

import os
from anthropic import Anthropic
from chatbot_config import COMPANY_INFO, CHATBOT_SYSTEM_PROMPT, CONTACT_INFO


class VitalMechanicalChatbot:
    """
    Chatbot for Vital Mechanical Service customer inquiries
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the chatbot with Anthropic API

        Args:
            api_key: Anthropic API key (if None, reads from ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be provided or set in environment")

        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []

        # Build enhanced system prompt with company info
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt with company information"""

        # Format core values
        values_text = "\n".join([
            f"- {v['name']}: {v['description']}"
            for v in COMPANY_INFO['core_values']
        ])

        # Format services
        services_text = "\n".join([
            f"- {s['category']}: {s['description']}"
            for s in COMPANY_INFO['services']
        ])

        # Format mission commitments
        commitments_text = "\n".join([
            f"- {c}" for c in COMPANY_INFO['mission']['commitments']
        ])

        # Build complete system prompt
        enhanced_prompt = f"""{CHATBOT_SYSTEM_PROMPT}

COMPANY DETAILS:

Founded: {COMPANY_INFO['founded']}
Location: {COMPANY_INFO['location']}
Tagline: {COMPANY_INFO['tagline']}

Core Values:
{values_text}

Mission Statement: {COMPANY_INFO['mission']['statement']}
Our Commitments:
{commitments_text}

Company Philosophy: {COMPANY_INFO['philosophy']}

Services We Provide:
{services_text}

Notable Clients Include: {', '.join(COMPANY_INFO['notable_clients'])}

What Makes Us Different:
{chr(10).join(['- ' + d for d in COMPANY_INFO['differentiators']])}

Contact Information:
- Website: {CONTACT_INFO['website']}
- Service Area: {CONTACT_INFO['service_area']}
- Phone: {CONTACT_INFO['phone']}
- Email: {CONTACT_INFO['email']}

When customers ask about scheduling service, pricing, or need immediate assistance, guide them to contact us via our website or provide the contact information above.
"""
        return enhanced_prompt

    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response

        Args:
            user_message: The customer's message

        Returns:
            The chatbot's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get response from Claude
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        # Extract assistant's response
        assistant_message = response.content[0].text

        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset_conversation(self):
        """Clear conversation history to start fresh"""
        self.conversation_history = []

    def get_conversation_history(self):
        """Get the full conversation history"""
        return self.conversation_history


def main():
    """
    Demo/test function for the chatbot
    """
    print("=" * 60)
    print("Vital Mechanical Service - Customer Service Chatbot")
    print("=" * 60)
    print("\nWelcome! I'm here to help answer your questions about")
    print("Vital Mechanical Service. Type 'quit' to exit.\n")

    # Initialize chatbot
    try:
        chatbot = VitalMechanicalChatbot()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    # Chat loop
    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nThank you for contacting Vital Mechanical Service!")
            print("Have a great day!")
            break

        if not user_input:
            continue

        try:
            response = chatbot.chat(user_input)
            print(f"\nVital Mechanical Bot: {response}")
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or contact us directly at https://www.vitalmechanical.com/")


if __name__ == "__main__":
    main()
