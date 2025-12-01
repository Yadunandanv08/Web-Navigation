from google.genai import types

def chat_completion(self, history, model_name=None):
    model_name = model_name or self.model_name
    return self.client.models.generate_content(
        model=f'models/{model_name}',
        contents=history,
        config=types.GenerateContentConfig(
            temperature=0
        )
    )





