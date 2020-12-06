from asyncio import Semaphore, Lock

class Barreira:
  def __init__(self, n):
    self.n = n
    self.contador = 0
    self.barreira_1 = Semaphore(0)
    self.barreira_2 = Semaphore(1)
    self.mutex = Lock()

  async def acquire_1(self):
    async with self.mutex:
      self.contador += 1
      if self.contador == self.n:
        await self.barreira_2.acquire()
        self.barreira_1.release()
    
    await self.barreira_1.acquire()
    self.barreira_1.release()

  async def acquire_2(self):
    async with self.mutex:
      self.contador -= 1
      if self.contador == 0:
        await self.barreira_1.acquire()
        self.barreira_2.release()
    
    await self.barreira_2.acquire()
    self.barreira_2.release()
