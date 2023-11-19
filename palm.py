import google.generativeai as palm

API_KEY = ""

palm.configure(api_key=API_KEY)

examples = [
    ("Hello!", "Hi there!"),
    ("How are you doing", "I am doing well! How are you feeling today?"),
]

prompt = input("Welcome to the chatbot! Please chat with me about anything! \n")


response = palm.chat(
    messages=prompt,
    temperature=1,
    context="Speak like a therapy chatbot - ask a question related to the conversation as needed, but be empathetic and kind",
    examples=examples,
)
for message in response.messages:
    print(message["author"], message["content"])

while True:
    s = input()
    response = response.reply(s)
    print(response.last)
