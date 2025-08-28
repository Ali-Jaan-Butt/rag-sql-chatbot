from database.insert_data import Insert_data
import gradio as gr
from generations import chatbot


try:
    insert = Insert_data()
    insert.insert_user_data()
except Exception as e:
    print("DB failure:", e)


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("<h1 style='text-align:center;'>🏦 Payment Method Guide Chatbot</h1>")
    gr.ChatInterface(
        fn=chatbot.chatbot,
        title="Ask Me About Payment Methods",
        theme="soft",
        examples=[
            "What is a payment method?",
            "What are the features of a current account?",
            "Your answer was amazing!",
            "That wasn't helpful."
        ],
    )

demo.launch(share=True)