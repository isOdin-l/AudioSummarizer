from typing import List
from openai import OpenAI
import re

class LLM:
    def __init__(self):
        self.model = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="",
        )
     
        self.max_context_window = 160.000

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
    
    def create_cunks(self, data: str) -> List[str]:
        sentences = self.split_into_sentences(data)
        embedings = List(len(vector) for vector in self.model.embeddings.create(input=sentences, model="deepseek/deepseek-r1-0528:free"))

        chunks: List[str] = []
        chunks_tokens_len: List[int] = [0]
        current_chunk = str()

        i = 0
        max_tokens = self.max_context_window*0.4
        # добавляем предложения в чанки по длине их токенизированных предложений
        while i < len(sentences):
            if embedings[i] + chunks_tokens_len[-1] <= max_tokens:
                current_chunk += " " + sentences[i]
                chunks_tokens_len[-1] += embedings[i]
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
    
    async def send_data(self, data: dict) -> str:

        completion = self.model.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {
                "role": "user",
                "content": f"я тебе передам текст, а ты должен его суммаризировать, cохрани стилистический окрас текста в суммаризации. Вот текст: {data}"
                }
            ]
        )

        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    async def summirize(self, data: str) -> str: # data - текст из транскрибатора
        chunks = self.create_cunks(data=data)
        
        summarization = str()
        for i in range(len(chunks)):
            summarization += self.send_data(data=chunks[i])
        
        return summarization

SummirizerLLM = LLM()