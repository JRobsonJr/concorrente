from aluno import ThreadAluno

class ThreadAlunoUEPB(ThreadAluno):
  def __init__(self, estado, id_aluno):
    super().__init__(estado, id_aluno, 'uepb')

  '''
  Rotina de solicitar embarque, que inclui verificar se o barco pode ser formado
  (se há 2 de cada universidade ou 4 da mesma).
  '''
  async def solicita_embarque(self):
    await self.estado.mutex.acquire()
    self.estado.uepb += 1
    
    if self.estado.uepb == 4:
      for i in range(4): self.estado.embarque_uepb.release()
      self.estado.uepb = 0
      self.eh_remador = True
    elif self.estado.uepb == 2 and self.estado.ufcg >= 2:
      for i in range(2): self.estado.embarque_uepb.release()
      for i in range(2): self.estado.embarque_ufcg.release()
      self.estado.ufcg -= 2
      self.estado.uepb = 0
      self.eh_remador = True
    else:
      self.estado.mutex.release()

    await self.estado.embarque_uepb.acquire()
