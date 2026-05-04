from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system", 
            "content": "You are a mental health support chatbot. Respond with empathy in 2-3 sentences."
        },
        {
            "role": "user", 
            "content": "I am feeling very sad today"
        }
    ],
    max_tokens=150
)

print("Groq says:")
print(completion.choices[0].message.content)