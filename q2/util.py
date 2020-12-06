import asyncio
import random

'''
Função utilitária utilizada para ajudar o código a não executar todo de vez.
Adiciona um pequeno intervalo de 1 a 5 segundos entre operações.
'''
async def esperar():
  await asyncio.sleep(random.randint(1, 5))