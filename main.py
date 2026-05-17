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



API_ID = int(os.getenv('API_ID'))

API_HASH = os.getenv('API_HASH')

STRING_SESSION = os.getenv('STRING_SESSION')

GATILHO_FRASE = os.getenv('GATILHO_FRASE')

LINK_INSTAGRAM = os.getenv('LINK_INSTAGRAM')



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
      
    files = [os.path.join(prints_dir, f) for f in os.listdir(prints_dir) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
  
    return random.sample(files, min(count, len(files)))
  


async def disparar_fluxo(event, chat_id):
  
    try:
      
        try:
          
            entity = await client.get_entity(chat_id)
          
        except Exception as e:
          
            logging.warning(f"Não foi possível obter entidade para {chat_id} via get_entity, tentando via event: {e}")
          
            entity = await event.get_chat()
          


        # 1. Boas-vindas

        async with client.action(entity, 'typing'):
          
            await asyncio.sleep(random.randint(4, 7))
          
            await client.send_message(entity, MSG_BOAS_VINDAS)
          
            save_interaction(chat_id, 'model', MSG_BOAS_VINDAS)
          


        # 2. Instagram

        async with client.action(entity, 'typing'):
          
            await asyncio.sleep(random.randint(5, 8))
          
            await client.send_message(entity, MSG_INSTAGRAM.format(link_instagram=LINK_INSTAGRAM))
          
            save_interaction(chat_id, 'model', MSG_INSTAGRAM.format(link_instagram=LINK_INSTAGRAM))
          


        # 3. Preparação para resultados

        async with client.action(entity, 'typing'):
          
            await asyncio.sleep(random.randint(5, 9))
          
            await client.send_message(entity, MSG_RESULTADOS)
          
            save_interaction(chat_id, 'model', MSG_RESULTADOS)
          


        # 4. Envio de Prints

        for img in get_random_prints(random.randint(3, 5)):
          
            async with client.action(entity, 'photo'):
              
                await asyncio.sleep(random.randint(4, 8))
              
                await client.send_file(entity, img)
              
                save_interaction(chat_id, 'model', f"[Enviou Print: {img}]")
              


        # 5. Apresentação dos Planos

        async with client.action(entity, 'typing'):
          
            await asyncio.sleep(random.randint(6, 10))
          
            await client.send_message(entity, MSG_APRESENTA_PLANOS)
          
            save_interaction(chat_id, 'model', MSG_APRESENTA_PLANOS)
          


        await asyncio.sleep(random.uniform(3, 5))
      
        awa
















































