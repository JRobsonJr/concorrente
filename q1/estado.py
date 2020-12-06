from asyncio import Lock, Semaphore

class Estado:
  def __init__(self, capacidade, n):
    self.capacidade = capacidade
    self.n = n
    self.mutex_entrada = Lock()
    self.mutex_saida = Lock()
    self.threads_dentro = 0
    self.threads_fora = 0
    self.embarque_liberado = Semaphore(0)
    self.desembarque_liberado = Semaphore(0)
    self.todas_dentro = Semaphore(0)
    self.todas_fora = Semaphore(0)
