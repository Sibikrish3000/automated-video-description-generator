from openai import OpenAI
import io
import base64
from utils.logger import get_logger

class VLMInferencer:
    def __init__(self, api_key: str, model: str = "gpt-4o", base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.logger = get_logger(self.__class__.__name__)
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
    def infer(self, prompt, images):
        # Convert PIL images to base64-encoded strings
        image_b64 = []
        for img in images:
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            b64_str = base64.b64encode(buf.read()).decode('utf-8')
            image_b64.append(b64_str)
        # Prepare OpenAI API call
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                *[{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}} for b64 in image_b64]
            ]}
        ]
        self.logger.info(f"Sending {len(images)} images to OpenAI {self.model}.")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=256
        )
        # print(response)
        if response == None:
            self.logger.error("No response from LLM.")
            return None
        description = response.choices[0].message.content
        self.logger.info("Received description from VLM.")
        return description 