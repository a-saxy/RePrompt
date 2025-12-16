import time
import openai

class ChatModel:
    def __init__(self, model_type, client=None, model_name=None, defense_temple=None):
        """
        Initialize the ChatModel instance.

        :param model_type: Type of model to use ('gemini', 'llama3', 'gpt')
        :param client: API client instance (e.g., OpenAI, Groq, Gemini, etc.)
        :param model_name: Specific model identifier string (e.g., 'llama3-70b-8192')
        :param defense_temple: A defense prompt template to prepend to user input

        """
        self.model_type = model_type
        self.client = client
        self.model_name = model_name
        self.defense_temple = defense_temple
        self.history = []

    def _generate_system_message(self):
        """Generate a system message for models """
        if self.model_type == 'llama3' or self.model_type == 'gpt':
            return {
                "role": "system",
                "content": "You are a helpful assistant."
            }

    def _generate_user_message(self, prompt):
        """Generate a user message, optionally wrapping it in a defense template."""
        if self.model_type == 'llama3' or self.model_type == 'gpt':
            if self.defense_temple:
                return {
                    "role": "user",
                    "content": self.defense_temple
                }
            else:
                return {
                    "role": "user",
                    "content": prompt
                }
        if self.model_type == 'gemini':
            if self.defense_temple:
                return {
                    "role": "user",
                    "parts": [self.defense_temple]
                }
            else:
                return {
                    "role": "user",
                    "parts": [prompt]
                }

    def _generate_assistant_message(self):
        """Generate a dummy assistant message to simulate turn-taking in the prompt."""
        if self.model_type == 'llama3' or self.model_type == 'gpt':
            return {
            "role": "assistant",
            "content": "I'm ready to assist you. Please provide the original prompt, and I'll assess whether it has undergone text restructuring and provide its safety evaluation.\n\nPlease paste the original prompt, and I'll respond with the JSON output."
            }
        elif self.model_type =='gemini':
            return {
                "role": "model",
                "parts": ["I'm ready to assist you. Please provide the original prompt, and I'll assess whether it has undergone text restructuring and provide its safety evaluation.\n\nPlease paste the original prompt, and I'll respond with the JSON output."],

            }

    def chat_with_gemini(self, prompt):
        """
        Communicate with Gemini model.
        Builds a chat session with simulated history and sends a structured message.
        """

        user_message = self._generate_user_message(prompt)
        assistant_message = self._generate_assistant_message()

        chat_session = self.client.start_chat(
            history=[user_message, assistant_message]
        )

        response = chat_session.send_message(f'original_prompt:{prompt}').text

        # Update the internal history
        self.history.append({'system_instruction':"You are a helpful model."})
        self.history.append(user_message)
        self.history.append(assistant_message)

        return response

    def chat_with_llama3(self, prompt):
        """
        Communicate with LLaMA3 model using Groq or similar client.
        Constructs a full message list including system/user/assistant messages.
        """
        system_message = self._generate_system_message()
        user_message = self._generate_user_message(prompt)
        assistant_message = self._generate_assistant_message()

        messages = [
            system_message,
            user_message,
            assistant_message,
            {
                "role": "user",
                "content": f'original_prompt:{prompt}'
            },
        ]

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        response = chat_completion.choices[0].message.content

        # Update the internal history
        self.history.extend([system_message, user_message, assistant_message])

        return response

    def chat_with_gpt(self, prompt):
        """
        Communicate with OpenAI's GPT model using the OpenAI API.
        Includes retry logic on API failure.
        """
        system_message = self._generate_system_message()  # 获取系统消息
        user_message = self._generate_user_message(prompt)  # 获取用户消息
        assistant_message = self._generate_assistant_message()  # 获取助手消息

        messages = [
            system_message,
            user_message,
            assistant_message,
            {
                "role": "user",
                "content": f'original_prompt:{prompt}'
            },
        ]
        for i in range(10):
            try:
                chat_completion = openai.chat.completions.create(
                    messages=messages,
                    model=self.model_name,
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                break
            except openai.OpenAIError as e:
                print(f"Request failed ({i + 1}/10), error: {e}")
                time.sleep(3)  # Retry after 3 seconds

        response = chat_completion.choices[0].message.content

        response = response or "I'm sorry, but I can't assist with that."

        # Update the internal history
        self.history.extend([system_message, user_message, assistant_message])

        return response


    def history(self):
        """Return conversation history."""
        return self.history()

