# coding=utf-8
"""
    This factory creates BattleshipProtocol() instances for every
    connected users. If number of connected users reach the value max_clients then this factory creates instance
    of ErrorBattleshipProtocol() for new users.

    Also this class, on own initialization, creates instance of the class Battleship which is a game main loop.

    See method buildProtocol() in current class and method initClient() in class Battleship().
"""
from twisted.internet.protocol import ServerFactory

from protocol import BattleshipProtocol
from service import Battleship
from errorprotocol import ErrorBattleshipProtocol

from twisted.python import log

class BattleshipServerFactory(ServerFactory):
    """
      Battleship server factory. Process incoming client requests
    """

    protocol = BattleshipProtocol

    def __init__(self, max_clients, service):
        """
          Battleship server factory constructor
        """
        log.msg('Battleship server initialized')
        
        # parameters
        self.battleship_service = Battleship(max_clients)
        self.service = service

    def buildProtocol(self, addr):
        """
          This method is calling when new client connected
          Create new protocol BattleshipProtocol if clients < max_clients
          or
          send error to client, if clients >= max_clients
        """
        if len(self.battleship_service.clients) < self.battleship_service.max_clients:
            p = self.protocol()
            p.factory = self
            p = self.battleship_service.initClient(p, addr)
            log.msg('class BattleshipServerFactory, method buildProtocol: protocol was built')
            return p
        else:
            """
              If count of players more then self.max_clients then close connections for all new clients
            """
            p = ErrorBattleshipProtocol()
            p.factory = self
            return p