# coding=utf-8
"""
This file is a start point for the game. Run this file from command line something like this:

    twistd --python battleshipserver.py

or:

    twistd --python --reactor=poll battleshipserver.py

or for debug:

    twistd --nodaemon --python battleshipserver.py
"""

from battleship.serverfactory import BattleshipServerFactory
from battleship.sendpolicy import SendPolicyFactory

from twisted.application import internet, service
from settings import host, port, policy_port, max_clients

top_service = service.MultiService()

battleship_service = service.Service()
battleship_service.setServiceParent(top_service)

factory = BattleshipServerFactory(max_clients, battleship_service)
tcp_service = internet.TCPServer(port, factory, interface=host)
tcp_service.setServiceParent(top_service)

policy_factory = SendPolicyFactory(battleship_service)
tcp_policy_service = internet.TCPServer(policy_port, policy_factory, interface=host)
tcp_policy_service.setServiceParent(top_service)

application = service.Application("battleshipserver")

# this hooks the collection we made to the application
top_service.setServiceParent(application)