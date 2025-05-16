# vision_agent.py
from PIL import Image
from langchain_community.llms import Ollama

llm = Ollama(model="granite-3b-vision")

def handle_image_query(prompt: str, image: Image.Image) -> str:
    return llm.invoke(input=prompt, images=[image]).strip()
