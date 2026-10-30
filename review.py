import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(base_url=os.environ["NEBIUS_BASE_URL"],
                api_key=os.environ["NEBIUS_API_KEY"])
MODEL = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"

def explain(code: str, violations: list[str]) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content":
             "You are a security reviewer. In 3 short bullets, explain what this "
             "code does and why the flagged permissions are risky. You cannot "
             "approve or reject; only explain."},
            {"role": "user", "content": f"Flags: {violations}\n\n```python\n{code}\n```"},
        ],
        max_tokens=400,
    )
    return resp.choices[0].message.content