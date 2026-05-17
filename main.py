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
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
STRING_SESSION = os.getenv('STRING_SESSION')
GATILHO_FRASE = os.getenv('GATILHO_FRASE', 'quero saber mais')
LINK_INSTAGRAM = os.getenv('LINK_INSTAGRAM', '')

if not API_ID or not API_HASH:
    logger.error("ERRO: API_ID ou API_HASH não configurados nas variáveis de ambiente!")
    exit(1)

API_ID = int(API_ID)

# Configuração do Cliente
if STRING_SESSION:
    logger.info("Usando STRING_SESSION para conexão...")
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, 
                            connection_retries=5, 
                            retry_delay=5, 
                            auto_reconnect=True)
else:
    logger.info("Usando sessão local (sessao_clara)...")
    client = TelegramClient('sessao_clara', API_ID, API_HASH, 
                            connection_retries=5, 
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
                logger.error(f"Erro ao enviar print {img}: {e}")
                
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
        logger.info(f"Fluxo concluído para o usuário {chat_id}")
        
    except Exception as e:
        logger.error(f"Erro ao disparar fluxo para {chat_id}: {e}")

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if not event.is_private:
        return
    
    user_text = event.raw_text or ""
    chat_id = event.chat_id
    logger.info(f"Mensagem recebida de {chat_id}: {user_text}")
    save_interaction(chat_id, 'user', user_text)
    
    status = get_lead_status(chat_id)
    gatilho = GATILHO_FRASE if GATILHO_FRASE else "quero saber mais"

    if user_text and limpar(gatilho) in limpar(user_text):
        logger.info(f"Gatilho ativado por {chat_id}")
        await disparar_fluxo(event, chat_id)
    elif status == 'vi_planos':
        history = get_chat_history(chat_id)
        async with client.action(chat_id, 'typing'):
            response = await get_ai_response(user_text, history)
            await asyncio.sleep(random.uniform(2, 4))
            await client.send_message(chat_id, response)
            save_interaction(chat_id, 'model', response)

async def start_bot():
    try:
        init_db()
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        
    logger.info("Conectando ao Telegram...")
    await client.connect()
    
    if not await client.is_user_authorized():
        logger.error("ERRO: Sessão não autorizada! Verifique a STRING_SESSION.")
        return
        
    logger.info("Userbot Clara ONLINE e aguardando mensagens!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Inicia servidor web para o Render
    keep_alive()
    
    # Rodar o bot
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.critical(f"Erro fatal: {e}")
