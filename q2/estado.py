from asyncio import Lock, Semaphore
from barreira import Barreira

class Estado:
  def __init__(self):
    self.barreira = Barreira(4)
    self.mutex = Lock()
    self.ufcg = 0
    self.uepb = 0
    self.embarque_ufcg = Semaphore(0)
    self.embarque_uepb = Semaphore(0)
