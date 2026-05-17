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

TELEFONE = os.getenv('TELEFONE')

SENHA_2FA = os.getenv('SENHA_2FA')

STRING_SESSION = os.getenv('STRING_SESSION')

GATILHO_FRASE = os.getenv('GATILHO_FRASE', 'Olá')

LINK_INSTAGRAM = os.getenv('LINK_INSTAGRAM', '')



if not API_ID or not API_HASH:
    
    logger.error("ERRO: API_ID ou API_HASH não configurados!")
    
    exit(1)
    


API_ID = int(API_ID)



# Configuração do Cliente

if STRING_SESSION and len(STRING_SESSION.strip()) > 50:
    
    logger.info("Usando STRING_SESSION para conexão...")
    
    session = StringSession(STRING_SESSION)
    
else:
    
    logger.info("Usando sessão local (sessao_clara)...")
    
    session = 'sessao_clara'
    


client = TelegramClient(session, API_ID, API_HASH, 
                        
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
            
        except Exception:
            
            entity = await event.get_chat()
            


        # 1. Boas-vindas

        async with client.action(entity, 'typing'):
            
            await asyncio.sleep(random.randint(4, 7))
            
            await client.send_message(entity, MSG_BOAS_VINDAS)
            
            save_interaction(chat_id, 'model', MSG_BOAS_VINDAS)
            


        # 2. Inst




































