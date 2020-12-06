from util import esperar

class ThreadPassageiro:
  '''
  - id_passageiro = Diferencia passageiros para compreensão da execução
  - estado = Objeto que guarda referências às estruturas úteis para o controle
    de concorrência
  '''
  def __init__(self, id_passageiro, estado):
    self.id_passageiro = id_passageiro
    self.estado = estado

  def __str__(self):
    return 'Passageiro ' + str(self.id_passageiro)

  '''
  Rotina de embarque do passageiro; aguarda aviso do carro de que pode embarcar,
  e então atualiza número de passageiros. Se é a última a entrar, avisa ao carro
  que pode dar a partida.
  '''
  async def embarcar(self):
    await self.estado.embarque_liberado.acquire()

    print('> ' + str(self) + ' (Embarcando): Partiu?')
    
    async with self.estado.mutex_entrada:
      self.estado.threads_dentro += 1
      if self.estado.threads_dentro == self.estado.capacidade:
        self.estado.todas_dentro.release()
        self.estado.threads_dentro = 0
  
  '''
  Rotina de desembarque do passageiro; aguarda aviso do carro de que pode desembarcar,
  e então atualiza número de passageiros que saíram. Se é a última a sair, avisa
  ao carro que pode terminar sua execução.
  '''
  async def desembarcar(self):
    await self.estado.desembarque_liberado.acquire()
    
    print('> ' + str(self) + ' (Desembarcando): Agradeço pela carona!')
    
    async with self.estado.mutex_saida:
      self.estado.threads_fora += 1

      if self.estado.threads_fora == self.estado.capacidade:
        self.estado.todas_fora.release()
        self.estado.threads_fora = 0

  '''
  Rotina de execução da thread passageiro; basicamente,
  aguarda um pouco, embarca, aguarda um pouco e desembarca.
  '''
  async def rodar(self):
    await esperar()
    await self.embarcar()
    await esperar()
    await self.desembarcar()
