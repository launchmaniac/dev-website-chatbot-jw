"""
Enhanced Chatbot with Tool/Function Calling Capabilities
This version can be extended with booking, quoting, and other features
"""

import os
from anthropic import Anthropic
from chatbot_config import COMPANY_INFO, CHATBOT_SYSTEM_PROMPT, CONTACT_INFO
from typing import Optional, Dict, Any, List
import json


class EnhancedVitalMechanicalChatbot:
    """
    Enhanced chatbot with extensible tool/function calling
    Can integrate with booking systems, quote generators, etc.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the enhanced chatbot

        Args:
            api_key: Anthropic API key
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be provided or set in environment")

        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.system_prompt = self._build_system_prompt()

        # Tool definitions (we'll expand these)
        self.tools = self._define_tools()

        # Feature flags (turn features on/off easily)
        self.features = {
            "booking_enabled": False,  # Set to True when booking integration ready
            "quotes_enabled": False,   # Set to True when quote system ready
            "lead_capture_enabled": True,  # Always capture leads
        }

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

IMPORTANT: When customers express interest in scheduling service or getting a quote, you can help them directly using the available tools. Always offer to help schedule or get a quote when appropriate.
"""
        return enhanced_prompt

    def _define_tools(self) -> List[Dict[str, Any]]:
        """
        Define tools/functions the chatbot can use
        These are Claude's function calling capabilities
        """
        tools = [
            {
                "name": "capture_lead",
                "description": "Capture customer contact information when they express interest in service. Use this when a customer wants to be contacted, schedule service, or get a quote.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Customer's name"
                        },
                        "email": {
                            "type": "string",
                            "description": "Customer's email address"
                        },
                        "phone": {
                            "type": "string",
                            "description": "Customer's phone number"
                        },
                        "service_interest": {
                            "type": "string",
                            "description": "What service they're interested in (HVAC, plumbing, etc.)"
                        },
                        "message": {
                            "type": "string",
                            "description": "Additional details about their needs"
                        },
                        "urgency": {
                            "type": "string",
                            "enum": ["emergency", "urgent", "normal", "flexible"],
                            "description": "How urgent is their need"
                        }
                    },
                    "required": ["name", "service_interest", "message"]
                }
            }
        ]

        # Add booking tool if enabled
        if self.features.get("booking_enabled"):
            tools.append({
                "name": "schedule_service",
                "description": "Schedule a service appointment for the customer",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "customer_name": {"type": "string"},
                        "customer_email": {"type": "string"},
                        "customer_phone": {"type": "string"},
                        "service_type": {
                            "type": "string",
                            "enum": ["HVAC Repair", "HVAC Maintenance", "Plumbing", "Refrigeration", "Controls", "Emergency Service"]
                        },
                        "preferred_date": {
                            "type": "string",
                            "description": "Preferred date in YYYY-MM-DD format"
                        },
                        "preferred_time": {
                            "type": "string",
                            "description": "Preferred time (morning, afternoon, evening)"
                        },
                        "description": {"type": "string"}
                    },
                    "required": ["customer_name", "service_type", "description"]
                }
            })

        # Add quote tool if enabled
        if self.features.get("quotes_enabled"):
            tools.append({
                "name": "request_quote",
                "description": "Generate a quote request for the customer",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "customer_name": {"type": "string"},
                        "customer_email": {"type": "string"},
                        "customer_phone": {"type": "string"},
                        "service_type": {"type": "string"},
                        "building_type": {
                            "type": "string",
                            "enum": ["office", "retail", "healthcare", "education", "industrial", "other"]
                        },
                        "building_size": {"type": "string"},
                        "project_description": {"type": "string"}
                    },
                    "required": ["customer_name", "service_type", "project_description"]
                }
            })

        return tools

    def chat(self, user_message: str) -> Dict[str, Any]:
        """
        Send a message and get a response
        Now returns structured data including any tool calls

        Args:
            user_message: The customer's message

        Returns:
            Dict with response and any actions taken
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get response from Claude with tool support
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=self.system_prompt,
            tools=self.tools,
            messages=self.conversation_history
        )

        # Process response
        result = {
            "response": "",
            "actions": [],
            "needs_user_info": False
        }

        # Handle tool calls
        if response.stop_reason == "tool_use":
            for content_block in response.content:
                if content_block.type == "tool_use":
                    # Execute the tool
                    tool_result = self._execute_tool(
                        content_block.name,
                        content_block.input
                    )

                    result["actions"].append({
                        "tool": content_block.name,
                        "input": content_block.input,
                        "result": tool_result
                    })

                    # Add tool use and result to conversation
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": response.content
                    })

                    self.conversation_history.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": json.dumps(tool_result)
                        }]
                    })

                    # Get final response after tool use
                    final_response = self.client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1024,
                        system=self.system_prompt,
                        tools=self.tools,
                        messages=self.conversation_history
                    )

                    result["response"] = final_response.content[0].text

                    self.conversation_history.append({
                        "role": "assistant",
                        "content": final_response.content[0].text
                    })

        else:
            # Regular text response
            result["response"] = response.content[0].text

            self.conversation_history.append({
                "role": "assistant",
                "content": response.content[0].text
            })

        return result

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool/function call
        This is where we integrate with real systems

        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool

        Returns:
            Result of the tool execution
        """
        if tool_name == "capture_lead":
            return self._capture_lead(tool_input)
        elif tool_name == "schedule_service":
            return self._schedule_service(tool_input)
        elif tool_name == "request_quote":
            return self._request_quote(tool_input)
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

    def _capture_lead(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Capture lead information
        For now, saves to a file. Later: integrate with CRM, email, database, etc.
        """
        try:
            # For now, append to a JSON file
            lead_file = "leads.json"

            import datetime
            lead_data = {
                **data,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "new"
            }

            # Read existing leads
            leads = []
            if os.path.exists(lead_file):
                with open(lead_file, 'r') as f:
                    leads = json.load(f)

            # Add new lead
            leads.append(lead_data)

            # Save back
            with open(lead_file, 'w') as f:
                json.dump(leads, f, indent=2)

            return {
                "success": True,
                "message": "Lead captured successfully. We'll contact you soon!",
                "lead_id": len(leads)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _schedule_service(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule a service appointment
        PLACEHOLDER - integrate with actual booking system later
        """
        # TODO: Integrate with calendar API, booking system, etc.
        return {
            "success": True,
            "message": "Service request received. We'll confirm your appointment within 24 hours.",
            "appointment_id": "TEMP-" + str(hash(str(data)))[:8]
        }

    def _request_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a quote request
        PLACEHOLDER - integrate with quote system later
        """
        # TODO: Integrate with quote generation system
        return {
            "success": True,
            "message": "Quote request received. We'll provide a detailed quote within 48 hours.",
            "quote_id": "QUOTE-" + str(hash(str(data)))[:8]
        }

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

    def enable_feature(self, feature_name: str):
        """Enable a feature (booking, quotes, etc.)"""
        if feature_name in self.features:
            self.features[feature_name] = True
            self.tools = self._define_tools()  # Rebuild tools

    def disable_feature(self, feature_name: str):
        """Disable a feature"""
        if feature_name in self.features:
            self.features[feature_name] = False
            self.tools = self._define_tools()  # Rebuild tools


def main():
    """Demo the enhanced chatbot"""
    print("=" * 60)
    print("Enhanced Vital Mechanical Chatbot with Tool Support")
    print("=" * 60)
    print("\nFeatures: Lead capture, extensible for booking & quotes")
    print("Type 'quit' to exit\n")

    try:
        chatbot = EnhancedVitalMechanicalChatbot()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set ANTHROPIC_API_KEY environment variable")
        return

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['quit', 'exit']:
            print("\nThank you!")
            break

        if not user_input:
            continue

        try:
            result = chatbot.chat(user_input)

            # Show actions taken
            if result["actions"]:
                print("\n[Actions Taken]:")
                for action in result["actions"]:
                    print(f"  - {action['tool']}: {action['result'].get('message', 'Executed')}")

            # Show response
            print(f"\nBot: {result['response']}")

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
