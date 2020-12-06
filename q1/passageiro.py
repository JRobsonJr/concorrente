class ThreadPassageiro:
  def __init__(self, carro, id_passageiro, estado):
    self.carro = carro
    self.id_passageiro = id_passageiro
    self.estado = estado

  def __str__(self):
    return 'Passageiro ' + str(self.id_passageiro)

  async def embarcar(self):
    print('> ' + str(self) + ' (Embarcando): Partiu?')
    
    async with self.estado.mutex_entrada:
      self.estado.threads_dentro += 1
      if self.estado.threads_dentro == self.estado.capacidade:
        self.estado.todas_dentro.release()
        self.estado.threads_dentro = 0
  
  async def desembarcar(self):
    print('> ' + str(self) + ' (Desembarcando): Agradeço pela carona!')
    
    async with self.estado.mutex_saida:
      self.estado.threads_fora += 1

      if self.estado.threads_fora == self.estado.capacidade:
        self.estado.todas_fora.release()
        self.estado.threads_fora = 0

  async def rodar(self):
    await self.estado.embarque_liberado.acquire()
    await self.embarcar()
  
    await self.estado.desembarque_liberado.acquire()
    await self.desembarcar()
