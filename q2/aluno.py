class ThreadAluno:
  def __init__(self, estado, id_aluno, universidade):
    self.estado = estado
    self.id_aluno = id_aluno
    self.eh_capitao = False
    self.universidade = universidade

  def __str__(self):
    return 'Aluno ' + str(self.universidade).upper() + ' ' + str(self.id_aluno)

  def boas_vindas(self):
    print(str(self) + ': Cheguei!')

  def embarca(self):
    print(str(self) + ' (Embarcando): Vamos?')

  def rema(self):
    print(str(self) + ' (Remando): Simbora, pessoal!')
  
  async def rodar(self):
    self.boas_vindas()
    await self.solicita_embarque()

    self.embarca()
    await self.estado.barreira.acquire_1()

    if self.eh_capitao:
      self.rema()
      self.estado.mutex.release()

    await self.estado.barreira.acquire_2()
