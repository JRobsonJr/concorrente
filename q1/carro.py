class ThreadCarro:
  def __init__(self, capacidade, n, estado):
    self.capacidade = capacidade
    self.n = n
    self.estado = estado
  
  async def carregar(self):
    print('Carro (Carregando): Entrem, vamos passear!')
    
    for i in range(self.capacidade):
      self.estado.embarque_liberado.release()
    await self.estado.todas_dentro.acquire()
  
  def correr(self):
    print('Carro (Correndo): Coloquem o cinto de segurança...')
  
  async def descarregar(self):
    print('Carro (Descarregando): Até a próxima, pessoal!')
    
    for i in range(self.capacidade):
      self.estado.desembarque_liberado.release()
    await self.estado.todas_fora.acquire()

  async def rodar(self):
    for i in range(self.n // self.capacidade):
      print('')
      await self.carregar()
      self.correr()
      await self.descarregar()
    
    restantes = self.n % self.capacidade
    if (restantes > 0):
      print('\nO último carro não fechou. ' + str(restantes) + ' thread(s) vai(vão) ficar esperando... eternamente... :(')
    else:
      print('\nTodas as threads passageiras passearam com a thread carro hoje. :)')
