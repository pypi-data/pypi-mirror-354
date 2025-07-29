# Email/message builder
def generate_email(question: str, answer: str, recipient: str) -> str:
    return f"""
Dear {recipient},

While reviewing publicly available data, I explored the following question:

"{question}"

The data suggests:
"{answer}"

Could you provide further context or clarification?

Kind regards,  
A Concerned Citizen
"""
