import asyncio
import random

class Barreira:
  def __init__(self, n):
    self.n = n
    self.contador = 0
    self.barreira = asyncio.Semaphore(0)
    self.barreira2 = asyncio.Semaphore(1)
    self.mutex = asyncio.Lock()

  async def acquire_1(self):
    async with self.mutex:
      self.contador += 1
      if self.contador == self.n:
        await self.barreira2.acquire()
        self.barreira.release()
    
    await self.barreira.acquire()
    self.barreira.release()

  async def acquire_2(self):
    async with self.mutex:
      self.contador -= 1
      if self.contador == 0:
        await self.barreira.acquire()
        self.barreira2.release()
    
    await self.barreira2.acquire()
    self.barreira2.release()

class Estado:
  def __init__(self):
    self.barreira = Barreira(4)
    self.mutex = asyncio.Lock()
    self.ufcg = 0
    self.uepb = 0
    self.embarque_ufcg = asyncio.Semaphore(0)
    self.embarque_uepb = asyncio.Semaphore(0)

class ThreadAluno:
  def __init__(self, estado, id_aluno, universidade):
    self.estado = estado
    self.id_aluno = id_aluno
    self.eh_capitao = False
    self.universidade = universidade

  def __str__(self):
    return 'Aluno ' + str(self.universidade).upper() + ' ' + str(self.id_aluno)

  def boas_vindas(self):
    print('Estávamos aguardando, ' + str(self) + '!')

  def embarca(self):
    print(str(self) + ' está embarcando!')

  def rema(self):
    print(str(self) + ' está remando!')
  
  async def rodar(self):
    self.boas_vindas()
    
    await self.solicita_embarque()

    self.embarca()
    await self.estado.barreira.acquire_1()

    if self.eh_capitao:
      self.rema()
      self.estado.mutex.release()

    await self.estado.barreira.acquire_2()

class ThreadAlunoUFCG(ThreadAluno):
  def __init__(self, estado, id_aluno):
    super().__init__(estado, id_aluno, 'ufcg')
  
  async def solicita_embarque(self):
    await self.estado.mutex.acquire()
    self.estado.ufcg += 1
    
    if self.estado.ufcg == 4:
      for i in range(4): self.estado.embarque_ufcg.release()
      self.estado.ufcg = 0
      self.eh_capitao = True
    elif self.estado.ufcg == 2 and self.estado.uepb >= 2:
      for i in range(2): self.estado.embarque_ufcg.release()
      for i in range(2): self.estado.embarque_uepb.release()
      self.estado.uepb -= 2
      self.estado.ufcg = 0
      self.eh_capitao = True
    else:
      self.estado.mutex.release()

    await self.estado.embarque_ufcg.acquire()

class ThreadAlunoUEPB(ThreadAluno):
  def __init__(self, estado, id_aluno):
    super().__init__(estado, id_aluno, 'uepb')

  async def solicita_embarque(self):
    await self.estado.mutex.acquire()
    self.estado.uepb += 1
    
    if self.estado.uepb == 4:
      for i in range(4): self.estado.embarque_uepb.release()
      self.estado.uepb = 0
      self.eh_capitao = True
    elif self.estado.uepb == 2 and self.estado.ufcg >= 2:
      for i in range(2): self.estado.embarque_uepb.release()
      for i in range(2): self.estado.embarque_ufcg.release()
      self.estado.ufcg -= 2
      self.estado.uepb = 0
      self.eh_capitao = True
    else:
      self.estado.mutex.release()

    await self.estado.embarque_uepb.acquire()

def cria_aluno(estado, id_aluno):
  return [ThreadAlunoUFCG(estado, id_aluno), ThreadAlunoUEPB(estado, id_aluno)][random.randint(0, 1)]

async def main():
  n = int(input())
  estado = Estado()
  alunos = [cria_aluno(estado, i + 1) for i in range(n)]
  await asyncio.gather(*(aluno.rodar() for aluno in alunos))

asyncio.run(main())
