import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Read C++ source code
with open("src/calculator.cpp", "r") as f:
    cpp_code = f.read()

# Read YAML instructions
with open("yaml/generate_tests.yaml", "r") as f:
    instructions = f.read()

# Compose the prompt
final_prompt = f"""
You are an expert C++ unit test generator using GoogleTest.
YAML Rules:
{instructions}

C++ Code:
{cpp_code}
"""

# Send to Hugging Face API
api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

response = requests.post(
    api_url,
    headers=headers,
    json={"inputs": final_prompt},
    params={"wait_for_model": "true"}
)

# Handle response
if response.status_code == 200:
    result = response.json()
    try:
        generated_code = result[0]["generated_text"]
        with open("tests/test_calculator.cpp", "w") as out:
            out.write(generated_code)
        print("✅ Test generated and saved to tests/test_calculator.cpp")
    except Exception as e:
        print("⚠️ Unexpected response format:", result)
else:
    print(f"❌ Error {response.status_code} - {response.text}")
