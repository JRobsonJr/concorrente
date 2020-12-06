import asyncio

class Estado:
  def __init__(self, capacidade, n):
    self.capacidade = capacidade
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
  def __init__(self, capacidade, n, estado):
    self.capacidade = capacidade
    self.n = n
    self.estado = estado
  
  async def carregar(self):
    print('Carro: carregando!')
    
    for i in range(self.capacidade):
      self.estado.embarque_liberado.release()
    await self.estado.todos_dentro.acquire()
  
  def correr(self):
    print('Carro: correndo!')
  
  async def descarregar(self):
    print('Carro: descarregando!')
    
    for i in range(self.capacidade):
      self.estado.desembarque_liberado.release()
    await self.estado.todos_fora.acquire()

  async def rodar(self):
    for i in range(self.n // self.capacidade):
      await self.carregar()
      self.correr()
      await self.descarregar()

      print('Viagem ' + str(i + 1) + ' completa!\n')

class ThreadPassageira:
  def __init__(self, carro, index, estado):
    self.carro = carro
    self.index = index
    self.estado = estado

  def embarcar(self):
    print('Passageira ' + str(self.index) + ': embarcando!')
  
  def desembarcar(self):
    print('Passageira ' + str(self.index) + ': desembarcando!')

  async def rodar(self):
    await self.estado.embarque_liberado.acquire()
    self.embarcar()
    
    async with self.estado.mutex_entrada:
      self.estado.pessoas_dentro += 1
      if self.estado.pessoas_dentro == self.estado.capacidade:
        self.estado.todos_dentro.release()
        self.estado.pessoas_dentro = 0

    await self.estado.desembarque_liberado.acquire()
    self.desembarcar()
    
    async with self.estado.mutex_saida:
      self.estado.pessoas_fora += 1

      if self.estado.pessoas_fora == self.estado.capacidade:
        self.estado.todos_fora.release()
        self.estado.pessoas_fora = 0

async def main():
  capacidade = 2
  n = 6
  
  estado = Estado(capacidade, n)
  carro = ThreadCarro(capacidade, n, estado)
  passageiras = [ThreadPassageira(carro, i, estado) for i in range(n)]
  await asyncio.gather(carro.rodar(), *(passageira.rodar() for passageira in passageiras))

asyncio.run(main())
