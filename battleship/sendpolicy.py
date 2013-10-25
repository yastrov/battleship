# coding=utf-8
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Protocol
from twisted.python import log

class SendPolicyProtocol(Protocol):
    def connectionMade(self):
        """
          This methos send domain policy to client. Its nececary for flash-client
          
          TODO: move var policy to external file crossdomain.xml
        """
        log.msg('SendPolicyProtocol. Policy was sent to client')
        policy = "<cross-domain-policy><allow-access-from domain='*' to-ports='*' /></cross-domain-policy>"
        self.transport.write(policy + '\x00')

class SendPolicyFactory(ServerFactory):
    log.msg("SendPolicyFctory")
    protocol = SendPolicyProtocol

    def __init__(self, service):
        log.msg("SendPolicyFctory constructor")
        self.service = service