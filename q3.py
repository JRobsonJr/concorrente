import asyncio
import random

class Shared:
  def __init__(self):
    self.eating = 0
    self.ready_to_leave = 0
    self.mutex = asyncio.Lock()
    self.ok_to_leave = asyncio.Semaphore(0)

class ThreadAluno:
  def __init__(self, index, shared):
    self.index = index
    self.shared = shared
  
  async def espera(self):
    a = int(random.random() * 10)
    await asyncio.sleep(a)
  
  async def pega_bebida(self):
    await self.espera()
    print('Garçom, traz uma bebida para Aluno ' + str(self.index) + '!')
  
  async def bebe(self):
    print('Aluno ' + str(self.index) + ' está bebendo!')
    await self.espera()
    print('Aluno ' + str(self.index) + ' está remediado.')

  async def sai(self):
    print('Até a próxima, Aluno ' + str(self.index) + '!')
  
  async def rodar(self):
    await self.pega_bebida()
    
    async with self.shared.mutex: 
      self.shared.eating += 1
      if self.shared.eating == 2 and self.shared.ready_to_leave == 1:
        self.shared.ok_to_leave.release()
        self.shared.ready_to_leave -= 1
    
    await self.bebe()

    await self.shared.mutex.acquire()
    self.shared.eating -= 1
    self.shared.ready_to_leave += 1

    if self.shared.eating == 1 and self.shared.ready_to_leave == 1:
      self.shared.mutex.release()
      await self.shared.ok_to_leave.acquire()
    elif self.shared.eating == 0 and self.shared.ready_to_leave == 2:
      self.shared.ok_to_leave.release()
      self.shared.ready_to_leave -= 2
      self.shared.mutex.release()
    else:
      self.shared.ready_to_leave -= 1
      self.shared.mutex.release()
    
    await self.sai()

async def main():
  n = int(input())
  shared = Shared()
  alunos = [ThreadAluno(i, shared) for i in range(n)]
  
  await asyncio.gather(*(aluno.rodar() for aluno in alunos))

asyncio.run(main())
