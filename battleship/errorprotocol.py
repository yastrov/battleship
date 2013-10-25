# coding=utf-8
from twisted.internet.protocol import Protocol
from twisted.python import log
from service import make_response

class ErrorBattleshipProtocol(Protocol):
    """
      This protocol using, if too much connection to server
    """
    def connectionMade(self):
        log.msg('new error connection (too much connections)')
        msg = make_response(code=12, message='connection failed, too much connections')
        self.writeData(msg)
        self.transport.loseConnection()

    def writeData(self, data):
        self.transport.write(json.dumps(data) + '\x00')