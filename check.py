from dotenv import load_dotenv
load_dotenv()
import os 
from openai import OpenAI

client = OpenAI(base_url=os.environ["NEBIUS_BASE_URL"],
                api_key=os.environ["NEBIUS_API_KEY"])

for m in client.models.list().data:
    if "nemotron" in m.id.lower():
        print(m.id) 


        
