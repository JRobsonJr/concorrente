from asyncio import Lock, Semaphore

class Estado:
  def __init__(self):
    self.alunos_bebendo = 0
    self.alunos_remediados = 0
    self.mutex = Lock()
    self.fila_saida = Semaphore(0)
