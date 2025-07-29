import requests

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append(Message(role, content))

    def get_messages(self):
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]

    def clear_history(self):
        self.messages = []

class linalg:
    def __init__(self):
        self.chat_history = ChatHistory()

    def ans(self, content, role='user'):
        self.chat_history.add_message(role, content)
        response = self.llm()
        return response

    def llm(self):
        res = requests.post(
            "http://193.109.69.92:8001/ans",
            json={
                "api_key": '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',
                'model_type': 'claude-sonnet-4-20250514',
                'max_tokens': 8000,
                'system_prompt': '',
                "messages": self.chat_history.get_messages(),
                "temperature": 0.5,
                "top_p": 0.95,  
                "top_k": 40     
            }
        )


        if res.status_code == 200:
            response = res.json()['response']
            self.chat_history.add_message("assistant", response)  # Use self.chat_history
            return response
        else:
            return f'{res.status_code}: {res.text}'

    def clear_history(self):
        self.chat_history.clear_history()
