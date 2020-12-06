import asyncio
import random

class ThreadAluno:
  def __init__(self, id_aluno, estado):
    self.id_aluno = id_aluno
    self.estado = estado
  
  def __str__(self):
    return 'Aluno ' + str(self.id_aluno)

  async def espera(self):
    await asyncio.sleep(random.randint(0, 5))
  
  async def pega_bebida(self):
    await self.espera()
    print(str(self) + ': Garçom, traz uma bebida!')
    await self.espera()
  
  async def bebe(self):
    print(str(self) + ': Comecei a beber.')
    await self.espera()
    print(str(self) + ': Já estou remediado...')
    await self.espera()

  async def sai(self):
    print(str(self) + ': Tchau para quem fica!')
  
  async def rodar(self):
    await self.pega_bebida()
    
    async with self.estado.mutex: 
      self.estado.alunos_bebendo += 1
      if self.estado.alunos_bebendo == 2 and self.estado.alunos_remediados == 1:
        self.estado.fila_saida.release()
        self.estado.alunos_remediados -= 1
    
    await self.bebe()

    await self.estado.mutex.acquire()
    self.estado.alunos_bebendo -= 1
    self.estado.alunos_remediados += 1

    if self.estado.alunos_bebendo == 1 and self.estado.alunos_remediados == 1:
      self.estado.mutex.release()
      await self.estado.fila_saida.acquire()
    elif self.estado.alunos_bebendo == 0 and self.estado.alunos_remediados == 2:
      self.estado.fila_saida.release()
      self.estado.alunos_remediados -= 2
      self.estado.mutex.release()
    else:
      self.estado.alunos_remediados -= 1
      self.estado.mutex.release()
    
    await self.sai()
