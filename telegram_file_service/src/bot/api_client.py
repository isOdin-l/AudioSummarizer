import httpx
import json

async def send_audio_for_summarise(
    api_base_url: str,
    interaction_data: str,
    source_type: str,
    metadata: dict,
    file_bytes: bytes,
    file_name: str,
    mime_type: str,
):
    url = f"{api_base_url}/api/audio_summarise"
    data = {
        "interaction_data": interaction_data,
        "source_type": source_type,
        "metadata": json.dumps(metadata, ensure_ascii=False),
    }
    files = {
        "file": (file_name, file_bytes, mime_type),
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, data=data, files=files)
        r.raise_for_status()
        return r.json()  
