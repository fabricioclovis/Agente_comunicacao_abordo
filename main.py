from groq import Groq
import streamlit as st 
import time
import os



# pip install groq 



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

st.title("Conversa com o Neymar") 
pergunta  = st.text_input('pergunta:')

if st.button('enviar'):
    # if pergunta.strip():
        reposta =  client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        temperature=0.7,

        messages=[
        {
        'role':'system',
        'content':"Você é um piloto de avião experiente."
        },
        {
            'role':'user',
            'content': pergunta
            
        }
        ]
        )

        st.text(reposta.choices[0].message.content)
        time.sleep(0)

