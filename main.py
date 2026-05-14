import os
import asyncio
import random
import logging
import re
from telethon import TelegramClient, events
from telethon.errors import RPCError
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
TELEFONE = os.getenv('TELEFONE')
SENHA_2FA = os.getenv('SENHA_2FA')
GATILHO_FRASE = os.getenv('GATILHO_FRASE')
LINK_INSTAGRAM = os.getenv('LINK_INSTAGRAM')

# Configuração do Cliente com reconexão automática reforçada
client = TelegramClient('sessao_clara', API_ID, API_HASH, 
                        connection_retries=None, 
                        retry_delay=5, 
                        auto_reconnect=True)

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
        for img in get_random_prints(random.randint(3, 5)):
            async with client.action(entity, 'photo'):
                await asyncio.sleep(random.randint(2, 4))
                await client.send_file(entity, img)
                save_interaction(chat_id, 'model', f"[Enviou Print: {img}]")
                
        # 5. Apresentação dos Planos
        async with client.action(entity, 'typing'):
            await asyncio.sleep(random.randint(4, 6))
            await client.send_message(entity, MSG_APRESENTA_PLANOS)
            save_interaction(chat_id, 'model', MSG_APRESENTA_PLANOS)
            
        await asyncio.sleep(2)
        await client.send_message(entity, TEXTO_VITALICIO)
        save_interaction(chat_id, 'model', TEXTO_VITALICIO)
        await asyncio.sleep(1)
        await client.send_message(entity, TEXTO_SEMESTRAL)
        save_interaction(chat_id, 'model', TEXTO_SEMESTRAL)
        await asyncio.sleep(1)
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
    save_interaction(chat_id, 'user', user_text)
    
    status = get_lead_status(chat_id)
    
    if user_text and GATILHO_FRASE.lower() in user_text.lower():
        logging.info(f"Gatilho ativado por {chat_id}")
        await disparar_fluxo(event, chat_id)
        return

    if status and ('vi_planos' in status or 'clicou_pagamento' in status):
        logging.info(f"IA processando para {chat_id}")
        history = get_chat_history(chat_id)
        
        ai_raw_response = await get_ai_response(chat_id, user_text, history)
        
        if "[IGNORAR]" in ai_raw_response:
            logging.info(f"IA decidiu ignorar a mensagem de {chat_id} (fora do script).")
            return

        messages_to_send = []
        new_status = status

        if "[COMPRAR_MENSAL]" in ai_raw_response:
            if 'clicou_pagamento' in status and status != 'clicou_pagamento_mensal':
                messages_to_send.append(MSG_MUDANCA_PLANO.format(plano="Mensal", link=LINK_PAGAMENTO_MENSAL))
            else:
                messages_to_send.append(MSG_FECHAMENTO_MENSAL.format(link=LINK_PAGAMENTO_MENSAL))
            new_status = 'clicou_pagamento_mensal'
        elif "[COMPRAR_SEMESTRAL]" in ai_raw_response:
            if 'clicou_pagamento' in status and status != 'clicou_pagamento_semestral':
                messages_to_send.append(MSG_MUDANCA_PLANO.format(plano="Semestral", link=LINK_PAGAMENTO_SEMESTRAL))
            else:
                messages_to_send.append(MSG_FECHAMENTO_SEMESTRAL.format(link=LINK_PAGAMENTO_SEMESTRAL))
            new_status = 'clicou_pagamento_semestral'
        elif "[COMPRAR_VITALICIO]" in ai_raw_response:
            if 'clicou_pagamento' in status and status != 'clicou_pagamento_vitalicio':
                messages_to_send.append(MSG_MUDANCA_PLANO.format(plano="Vitalício", link=LINK_PAGAMENTO_VITALICIO))
            else:
                messages_to_send.append(MSG_FECHAMENTO_VITALICIO.format(link=LINK_PAGAMENTO_VITALICIO))
            new_status = 'clicou_pagamento_vitalicio'
        else:
            if "[QUEBRA]" in ai_raw_response:
                messages_to_send = [m.strip() for m in ai_raw_response.split("[QUEBRA]") if m.strip()]
            else:
                messages_to_send = [m.strip() for m in ai_raw_response.split("\n\n") if m.strip()]
                if len(messages_to_send) == 1 and len(messages_to_send[0]) > 150:
                    messages_to_send = re.split(r'(?<=[.!?]) +', messages_to_send[0])

        if new_status != status:
            update_lead_status(chat_id, new_status)

        try:
            entity = await client.get_entity(chat_id)
            for msg in messages_to_send:
                async with client.action(entity, 'typing'):
                    wait_time = min(len(msg) * 0.06, 4) + random.uniform(0.5, 1.5)
                    await asyncio.sleep(wait_time)
                    await client.send_message(entity, msg)
                    save_interaction(chat_id, 'model', msg)
                    await asyncio.sleep(random.uniform(1.0, 2.5))
        except Exception as e:
            logging.error(f"Erro ao enviar resposta da IA para {chat_id}: {e}")
    else:
        logging.info(f"Usuário {chat_id} mandou mensagem mas ainda não ativou o fluxo.")

async def main():
    init_db()
    
    # Inicia o servidor web para manter o bot vivo na nuvem (Render/Railway/etc)
    keep_alive()
    
    while True:
        try:
            await client.start(phone=TELEFONE, password=SENHA_2FA)
            print("="*30)
            print("CLARA CLOUD READY (V10) ONLINE! 🚀☁️")
            print(f"Gatilho: '{GATILHO_FRASE}'")
            print("="*30)
            await client.run_until_disconnected()
        except Exception as e:
            logging.error(f"Erro na conexão do cliente: {e}. Tentando reconectar em 10 segundos...")
            await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
