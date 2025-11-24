"""
Example questions and test scenarios for Vital Mechanical chatbot
Use this to test the chatbot's responses and ensure quality
"""

EXAMPLE_QUESTIONS = {
    "services": [
        "What services do you offer?",
        "Do you do HVAC repair?",
        "Can you help with our building's air conditioning?",
        "Do you service commercial refrigeration?",
        "What kind of preventative maintenance do you offer?",
        "Do you work on building controls and automation?",
        "Can you help with a tenant improvement project?",
        "Do you install heat pump water heaters?",
    ],

    "company_info": [
        "How long have you been in business?",
        "What makes Vital Mechanical different from other companies?",
        "What are your core values?",
        "Who are some of your clients?",
        "What is 'The Vital Way'?",
        "Where are you located?",
        "What area do you service?",
    ],

    "scheduling_pricing": [
        "How do I schedule a service call?",
        "What are your rates?",
        "Do you offer emergency service?",
        "How quickly can you respond to a service request?",
        "Do you have a maintenance contract program?",
        "How much does preventative maintenance cost?",
    ],

    "technical": [
        "My HVAC system isn't cooling properly, what should I do?",
        "How often should we have our HVAC system serviced?",
        "What's included in a preventative maintenance visit?",
        "Do you work on all brands of equipment?",
        "Can you help us improve our building's energy efficiency?",
        "Our building controls aren't working right, can you help?",
    ],

    "customer_concerns": [
        "Will you respect our property during service?",
        "How do you communicate with customers?",
        "What if we're not satisfied with the service?",
        "Do you guarantee your work?",
        "How do you handle after-hours emergencies?",
    ],

    "greetings": [
        "Hello",
        "Hi there",
        "Good morning",
        "I need some help",
        "Can you help me?",
    ]
}


def print_all_questions():
    """Print all example questions by category"""
    for category, questions in EXAMPLE_QUESTIONS.items():
        print(f"\n{category.upper().replace('_', ' ')}")
        print("=" * 50)
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")


if __name__ == "__main__":
    print("VITAL MECHANICAL CHATBOT - EXAMPLE TEST QUESTIONS")
    print("=" * 60)
    print_all_questions()
