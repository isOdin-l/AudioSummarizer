from typing import List
from openai import OpenAI
import re

class LLM:
    def __init__(self):
        self.model = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="<OPENROUTER_API_KEY>",
        )
                
        self.max_context_window = 31.000

    def split_into_sentences(self, text: str) -> List[str]:
        text = re.sub(r'(\d)\.(\d)', r'\1<NUM>\2', text)
        text = re.sub(r'\.{2,}', '<ELLIPSIS>', text)

        sentences = re.split(r'(?<=[.!?])\s+(?=["«А-ЯA-Z])', text)

        sentences = [
            s.replace('<NUM>', '.')
            .replace('<ELLIPSIS>', '...')
            .strip()
            for s in sentences
        ]

        return [s for s in sentences if s]
    
    def create_cunks(self, data: dict) -> List[str]: # TODO: Поменять
        sentences = self.model.split_into_sentences(data["prompt"])

        chunks: List[str] = []
        chunks_tokens_len: List[int] = [0]
        current_chunk = str()

        i = 0
        max_tokens = self.model.max_context_window*0.4
        # добавляем предложения в чанки по длине их токенизированных предложений
        while i < len(sentences):
            sentence_tokens = self.model.craete_tokens(sentences[i]) # Токенизируем предложение 
            
            if len(sentence_tokens) + chunks_tokens_len[-1] <= max_tokens:
                current_chunk += " " + sentences[i]
                chunks_tokens_len[-1] += len(sentence_tokens)
                i+=1
            else:
                chunks_tokens_len.append(0)
                chunks.append(current_chunk)
                current_chunk = ""

        if current_chunk != "":
            chunks.append(current_chunk)
            # chunks_tokens_len[-1] = len(self.model.craete_tokens(current_chunk))

        print(len(chunks), chunks_tokens_len)
        return chunks
    
    async def send_data(self, data: dict) -> dict:

        completion = self.chat.completions.create(
            model="qwen/qwen3-235b-a22b:free",
            messages=[
                {
                "role": "user",
                "content": data
                }
            ]
        )
        print(completion.choices[0].message.content)