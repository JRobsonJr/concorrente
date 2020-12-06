from asyncio import Semaphore, Lock

'''
Barreira baseada na Reusable barrier do Little Book of Semaphores (3.7).
'''
class Barreira:
  def __init__(self, n):
    self.n = n # Número de threads aguardadas
    self.contador = 0 # Número de threads até o momento
    self.barreira_1 = Semaphore(0) # Proteção de entrada da barreira
    self.barreira_2 = Semaphore(1) # Proteção de saída da barreira
    self.mutex = Lock() # Protege acesso à variável contador

  '''
  Aguarda entrada na barreira.
  '''
  async def acquire_1(self):
    async with self.mutex:
      self.contador += 1
      if self.contador == self.n:
        await self.barreira_2.acquire()
        self.barreira_1.release()
    
    await self.barreira_1.acquire()
    self.barreira_1.release()

  '''
  Aguarda saída da barreira.
  '''
  async def acquire_2(self):
    async with self.mutex:
      self.contador -= 1
      if self.contador == 0:
        await self.barreira_1.acquire()
        self.barreira_2.release()
    
    await self.barreira_2.acquire()
    self.barreira_2.release()
