import os
from groq import Groq
from dotenv import load_dotenv
from constants import INSTRUCAO_CLARA

load_dotenv()

client_groq = Groq(api_key=os.getenv('GROQ_API_KEY'))
MODEL = os.getenv('IA_MODEL', 'llama-3.3-70b-versatile')

async def get_ai_response(user_id, user_message, history):
    try:
        messages = [{"role": "system", "content": INSTRUCAO_CLARA}]
        
        # Adiciona histórico (converte 'user' e 'model' para os termos da Groq se necessário)
        for h in history:
            role = "assistant" if h['role'] == 'model' else "user"
            messages.append({"role": role, "content": h['content']})
            
        # Adiciona a mensagem atual
        messages.append({"role": "user", "content": user_message})
        
        completion = client_groq.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        print(f"Erro na Groq: {e}")
        return "Opa, craque! Deu uma oscilada aqui, mas me diz: bora forrar hoje ou vai deixar passar? 🚀"
