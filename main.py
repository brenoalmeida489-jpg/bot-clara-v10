import os
import asyncio
import random
import logging
import re
from telethon import TelegramClient, events
from telethon.errors import RPCError
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Importações locais
from constants import *
from database import init_db, save_interaction, update_lead_status, get_lead_status, get_chat_history
from ai_service import get_ai_response
from web_server import keep_alive

# Configuração de Logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# Carregar variáveis de ambiente
load_dotenv()

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
STRING_SESSION = os.getenv('STRING_SESSION', '')
GATILHO_FRASE = os.getenv('GATILHO_FRASE', 'quero saber mais')
LINK_INSTAGRAM = os.getenv('LINK_INSTAGRAM', '')

# Configuração do Cliente com StringSession para evitar erros de IP no Render
if STRING_SESSION:
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, 
                            connection_retries=None, 
                            retry_delay=5, 
                            auto_reconnect=True)
else:
    client = TelegramClient('sessao_clara', API_ID, API_HASH, 
                            connection_retries=None, 
                            retry_delay=5, 
                            auto_reconnect=True)

def limpar(texto):
    if texto is None:
        return ""
    return re.sub(r'[^\w\s]', '', str(texto)).lower().strip()

def get_random_prints(count=3):
    prints_dir = 'prints'
    if not os.path.exists(prints_dir):
        return []
    try:
        files = [os.path.join(prints_dir, f) for f in os.listdir(prints_dir) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
        if not files:
            return []
        return random.sample(files, min(count, len(files)))
    except Exception:
        return []

async def disparar_fluxo(event, chat_id):
    try:
        try:
            entity = await client.get_entity(chat_id)
        except Exception as e:
            logging.warning(f"Não foi possível obter entidade para {chat_id}, tentando via event: {e}")
            entity = await event.get_chat()

        # 1. Boas-vindas
        async with client.action(entity, 'typing'):
            await asyncio.sleep(random.randint(2, 4))
            await client.send_message(entity, MSG_BOAS_VINDAS)
            save_interaction(chat_id, 'model', MSG_BOAS_VINDAS)
        
        # 2. Instagram
        async with client.action(entity, 'typing'):
            await asyncio.sleep(random.randint(3, 5))
            await client.send_message(entity, MSG_INSTAGRAM.format(link_instagram=LINK_INSTAGRAM))
            save_interaction(chat_id, 'model', MSG_INSTAGRAM.format(link_instagram=LINK_INSTAGRAM))
            
        # 3. Preparação para resultados
        async with client.action(entity, 'typing'):
            await asyncio.sleep(random.randint(3, 5))
            await client.send_message(entity, MSG_RESULTADOS)
            save_interaction(chat_id, 'model', MSG_RESULTADOS)
            
        # 4. Envio de Prints
        prints = get_random_prints(random.randint(2, 3))
        for img in prints:
            try:
                async with client.action(entity, 'photo'):
                    await asyncio.sleep(random.randint(2, 4))
                    await client.send_file(entity, img)
                    save_interaction(chat_id, 'model', f"[Enviou Print: {img}]")
            except Exception as e:
                logging.error(f"Erro ao enviar print {img}: {e}")
                
        # 5. Apresentação dos Planos
        async with client.action(entity, 'typing'):
            await asyncio.sleep(random.randint(4, 6))
            await client.send_message(entity, MSG_APRESENTA_PLANOS)
            save_interaction(chat_id, 'model', MSG_APRESENTA_PLANOS)
            
        await asyncio.sleep(random.uniform(2, 3))
        await client.send_message(entity, TEXTO_VITALICIO)
        save_interaction(chat_id, 'model', TEXTO_VITALICIO)
        await asyncio.sleep(random.uniform(1, 2))
        await client.send_message(entity, TEXTO_SEMESTRAL)
        save_interaction(chat_id, 'model', TEXTO_SEMESTRAL)
        await asyncio.sleep(random.uniform(1, 2))
        await client.send_message(entity, TEXTO_MENSAL)
        save_interaction(chat_id, 'model', TEXTO_MENSAL)
        
        # 6. Pergunta Final
        async with client.action(entity, 'typing'):
            await asyncio.sleep(random.randint(3, 5))
            await client.send_message(entity, MSG_PERGUNTA_PLANO)
            save_interaction(chat_id, 'model', MSG_PERGUNTA_PLANO)
            
        update_lead_status(chat_id, 'vi_planos')
        logging.info(f"Fluxo concluído para o usuário {chat_id}")
        
    except Exception as e:
        logging.error(f"Erro ao disparar fluxo para {chat_id}: {e}")

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if not event.is_private:
        return
    
    user_text = event.raw_text or ""
    chat_id = event.chat_id
    logging.info(f"Mensagem recebida de {chat_id}: {user_text}")
    save_interaction(chat_id, 'user', user_text)
    
    status = get_lead_status(chat_id)
    gatilho = GATILHO_FRASE if GATILHO_FRASE else "quero saber mais"

    if user_text and limpar(gatilho) in limpar(user_text):
        logging.info(f"Gatilho ativado por {chat_id}")
        await disparar_fluxo(event, chat_id)
    elif status == 'vi_planos':
        history = get_chat_history(chat_id)
        async with client.action(chat_id, 'typing'):
            response = await get_ai_response(user_text, history)
            await asyncio.sleep(random.uniform(2, 4))
            await client.send_message(chat_id, response)
            save_interaction(chat_id, 'model', response)

async def start_bot():
    # Inicializa o banco de dados
    try:
        init_db()
    except Exception as e:
        logging.error(f"Erro ao inicializar banco de dados: {e}")
        
    await client.start()
    logging.info("Userbot Clara iniciado e aguardando mensagens...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Inicia servidor web para o Render não derrubar o serviço
    keep_alive()
    
    # Rodar o bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
