from util import esperar

class ThreadCarro:
  '''
  - capacidade = Número de passageiros por viagem
  - n = Número de passageiros ao todo
  - estado = Objeto que guarda referências às estruturas úteis para o controle
    de concorrência
  '''
  def __init__(self, capacidade, n, estado):
    self.capacidade = capacidade
    self.n = n
    self.estado = estado 
  
  '''
  Libera C embarques às threads passageiras que estão esperando e aguarda o
  aviso de que todas já entraram.
  '''
  async def carregar(self):
    print('Carro (Carregando): Entrem, vamos passear!')
    
    for i in range(self.capacidade):
      self.estado.embarque_liberado.release()
    await self.estado.todas_dentro.acquire()
  
  '''
  Corrida do carro. Dura alguns segundos.
  '''
  async def correr(self):
    print('Carro (Correndo): Coloquem o cinto de segurança...')
    await esperar()

  '''
  Libera C desembarques às threads passageiras que estão no carro e aguarda o
  aviso de que todas já saíram.
  '''
  async def descarregar(self):
    print('Carro (Descarregando): Até a próxima, pessoal!')
    
    for i in range(self.capacidade):
      self.estado.desembarque_liberado.release()
    await self.estado.todas_fora.acquire()

  '''
  Rotina de execução da thread carro: faz n / capacidade viagens, que consistem
  em carregar, correr (que leva um tempinho) e descarregar.
  
  Se nem todas as threads passageiras conseguem passear (n / capacidade não é um
  número exato), indica na tela e não encerra a execução.
  '''
  async def rodar(self):
    for i in range(self.n // self.capacidade):
      print('')
      await self.carregar()
      await self.correr()
      await self.descarregar()
    
    restantes = self.n % self.capacidade
    if (restantes > 0):
      print('\nO último carro não fechou. ' + str(restantes) + ' thread(s) vai(vão) ficar esperando... eternamente... :(')
    else:
      print('\nTodas as threads passageiras passearam com a thread carro hoje. :)')
