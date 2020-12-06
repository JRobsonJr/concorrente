import asyncio
import random

class Estado:
  def __init__(self):
    self.eating = 0
    self.ready_to_leave = 0
    self.mutex = asyncio.Lock()
    self.ok_to_leave = asyncio.Semaphore(0)

class ThreadAluno:
  def __init__(self, index, estado):
    self.index = index
    self.estado = estado
  
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
    
    async with self.estado.mutex: 
      self.estado.eating += 1
      if self.estado.eating == 2 and self.estado.ready_to_leave == 1:
        self.estado.ok_to_leave.release()
        self.estado.ready_to_leave -= 1
    
    await self.bebe()

    await self.estado.mutex.acquire()
    self.estado.eating -= 1
    self.estado.ready_to_leave += 1

    if self.estado.eating == 1 and self.estado.ready_to_leave == 1:
      self.estado.mutex.release()
      await self.estado.ok_to_leave.acquire()
    elif self.estado.eating == 0 and self.estado.ready_to_leave == 2:
      self.estado.ok_to_leave.release()
      self.estado.ready_to_leave -= 2
      self.estado.mutex.release()
    else:
      self.estado.ready_to_leave -= 1
      self.estado.mutex.release()
    
    await self.sai()

async def main():
  n = int(input())
  estado = Estado()
  alunos = [ThreadAluno(i, estado) for i in range(n)]
  
  await asyncio.gather(*(aluno.rodar() for aluno in alunos))

asyncio.run(main())
