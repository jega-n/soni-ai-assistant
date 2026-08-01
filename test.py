import ollama
import time

messages = [
    {
        "role": "system",
        "content": "Return only JSON."
    },
    {
        "role": "user",
        "content": "Open calculator."
    }
]

start = time.perf_counter()

response = ollama.chat(
    model="qwen2.5:3b",
    messages=messages
)

print(time.perf_counter() - start)
print(response["message"]["content"])