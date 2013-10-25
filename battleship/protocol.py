# coding=utf-8
"""
    Instance of this class creates for every connected user by the TictactoeServerFactory().
"""

from twisted.internet.protocol import Protocol
try:
    import simplejson as json
except ImportError:
    import json
from twisted.python import log
import time

class BattleshipProtocol(Protocol):
    """
      This protocol using for ordinary clients
    """
    def connectionLost(self, reason):
        log.msg('BattleshipProtocol.connectionLost. Connection lost for client %s' % (self.client_id))
        self.factory.battleship_service.connectionClosedByClient(self.client_id)
        
    def connectionMade(self):
        log.msg('BattleshipProtocol.connectionMade. New connection %s, sending client_id to new client' % (self.client_id,))
        self.writeData({'code': 1, 
                        'id' :self.client_id})

    def dataReceived(self, raw_data):
        log.msg('BattleshipProtocol.dataReceived receive: %s' %raw_data)
        raw_data = raw_data.replace('\x00', '')
        received_data = json.loads(raw_data)
        self.factory.battleship_service.dataReceived(self, received_data)

    def writeData(self, data):
        sdata = json.dumps(data)
        self.transport.write(sdata + '\x00')