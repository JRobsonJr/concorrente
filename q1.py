import asyncio

class Shared:
  def __init__(self, C, n):
    self.C = C
    self.n = n
    self.mutex_entrada = asyncio.Lock()
    self.mutex_saida = asyncio.Lock()
    self.pessoas_dentro = 0
    self.pessoas_fora = 0
    self.embarque_liberado = asyncio.Semaphore(0)
    self.desembarque_liberado = asyncio.Semaphore(0)
    self.todos_dentro = asyncio.Semaphore(0)
    self.todos_fora = asyncio.Semaphore(0)

class ThreadCarro:
  def __init__(self, C, n, shared):
    self.C = C
    self.n = n
    self.shared = shared
  
  async def carregar(self):
    print('Carro: carregando!')
    
    for i in range(self.C):
      self.shared.embarque_liberado.release()
    await self.shared.todos_dentro.acquire()
  
  def correr(self):
    print('Carro: correndo!')
  
  async def descarregar(self):
    print('Carro: descarregando!')
    
    for i in range(self.C):
      self.shared.desembarque_liberado.release()
    await self.shared.todos_fora.acquire()

  async def rodar(self):
    for i in range(self.n // self.C):
      await self.carregar()
      self.correr()
      await self.descarregar()

      print('Viagem ' + str(i + 1) + ' completa!\n')

class ThreadPassageira:
  def __init__(self, carro, index, shared):
    self.carro = carro
    self.index = index
    self.shared = shared

  def embarcar(self):
    print('Passageira ' + str(self.index) + ': embarcando!')
  
  def desembarcar(self):
    print('Passageira ' + str(self.index) + ': desembarcando!')

  async def rodar(self):
    await self.shared.embarque_liberado.acquire()
    self.embarcar()
    
    async with self.shared.mutex_entrada:
      self.shared.pessoas_dentro += 1
      if self.shared.pessoas_dentro == self.shared.C:
        self.shared.todos_dentro.release()
        self.shared.pessoas_dentro = 0

    await self.shared.desembarque_liberado.acquire()
    self.desembarcar()
    
    async with self.shared.mutex_saida:
      self.shared.pessoas_fora += 1

      if self.shared.pessoas_fora == self.shared.C:
        self.shared.todos_fora.release()
        self.shared.pessoas_fora = 0

async def main():
  C = 2
  n = 6
  
  shared = Shared(C, n)
  carro = ThreadCarro(C, n, shared)
  passageiras = [ThreadPassageira(carro, i, shared) for i in range(n)]
  await asyncio.gather(carro.rodar(), *(passageira.rodar() for passageira in passageiras))

asyncio.run(main())
