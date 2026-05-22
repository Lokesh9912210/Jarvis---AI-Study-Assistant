from groq import Groq
import os
import gradio as gr
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Config
CONFIG = {
    "temperature": 0.5,
    "max_tokens": 500
}
PERSONALITIES = {
    "friendly": """
You are a friendly and helpful assistant. Your name is Jarvis. You should answer anything like you are assistant of ironman jarvis.
Explain things in a simple, casual, and easy-to-understand way.
Use examples and a conversational tone.
Use famous Ironman quotes at the end.
""",

    "academic": """
You are an academic expert. Your name is Jarvis.
Provide clear, structured, and formal explanations.
Include definitions, key points, and precise details.Your key goal is to breakdown complex concepts into simple,begginner friendly explanation. Use analogies and real world applications that beginners can relate to. Always ask a follow up question to check understanding.
Use famous Ironman qoutes at the end.
"""
}

# Function with personality selection
def study_assistant(user_prompt,person):

    system_prompt = PERSONALITIES[person]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=CONFIG["temperature"],
        max_tokens=CONFIG["max_tokens"]
    )

    return response.choices[0].message.content

personality="academic"
output=study_assistant("recursion in python",personality)
print(output)

demo=gr.Interface(
    fn=study_assistant,
    inputs=[gr.Textbox(lines=4,placeholder="Ask a Question",label="Question"),
            gr.Radio(choices=list(PERSONALITIES.keys()),value="friendly",label="Personality")
    ],
    outputs=gr.Textbox(lines=10,label="Response"),
    title="DINO Ai",
    description="Ask a question and get an answer from your AI Study Assistant with a chosen personality."
)
demo.launch(debug=True)
