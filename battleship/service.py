# coding=utf-8
"""
    This is a "main service" of the game. It is created on BattleshipServerFactory() start and has
    several LoopingCall's which prepare and send data to clients (players).
"""

try:
    import simplejson as json
except ImportError:
    import json
from battleshipgame import BattleshipGame
import time
from twisted.python import log

def make_response(code, **kwargs):
    d = {'code': code,}
    d.update(**kwargs)
    return d

class Battleship:
    """
      Main game class.
    """
    def __init__(self, max_clients):
        self.clients = {}
        self.max_clients = max_clients

        self.games = {}
        self.clients_waiting_list = []

        from twisted.internet import reactor
        from twisted.internet.task import LoopingCall

        self.lc = LoopingCall(self.sendDataToClients)
        self.lc.start(.05)

        self.waiting_list_lc = LoopingCall(self.checkWaitingList)
        self.waiting_list_lc.start(3)

    def initClient(self, client, addr):
        client.client_id = addr.port
        client.status = 'waiting'
        client.game_id = ''
        self.clients[addr.port] = client
        self.clients_waiting_list.append(addr.port)

        log_msg = 'class Battleship, method initClient: %s, %s:%s' % (addr.type, addr.host, addr.port,)
        log.msg(log_msg)
        
        return client

    def checkWaitingList(self):
        while len(self.clients_waiting_list) > 1:
            log.msg(self.clients_waiting_list)
            log.msg(self.clients[self.clients_waiting_list[0]])
            player1 = self.clients[self.clients_waiting_list[0]]
            player2 = self.clients[self.clients_waiting_list[1]]

            game_id = '{}-{}'.format(player1.client_id,
                                        player2.client_id)
            
            player1.game_id = game_id
            player2.game_id = game_id

            self.games[game_id] = BattleshipGame(player1,
                                                player2)

            self.clients_waiting_list.pop(0)
            self.clients_waiting_list.pop(0)
            
            self.sendPrestartMessage(player1)
            self.sendPrestartMessage(player2)
            
            log.msg('Battleship.checkWaitingList: created new game %s with players %s and %s' % (game_id, player1, player2))

    def sendPrestartMessage(self, client):
        client.status = 'prestart'
        client.writeData(make_message(code=15, message='prestart'))
      
    def connectionClosedByClient(self, client):
        if client.status == 'waiting':
            self.clients_waiting_list.remove(client_id)

        del self.client
        self.stopGame(client)

    def checkStartGame(self, game_id):
        player1, player2 = self.games[game_id].players_list()
        
        if player1.status == 'ready' and\
          player2.status == 'ready':
            self.startGame(game_id)
    
    def startGame(self, game_id):
        def m_message(player):
            return {'other_player': player.client_id,
                    }
        player1, player2 = self.games[game_id].players_list()
        player1.status = 'working'
        player2.status = 'working'

        player1.writeData(make_message(22, m_message(player2)))
        player2.writeData(make_message(22, m_message(player1)))
    
    def stopGame(self, client):
        for game in self.games:
            players = self.games[game].players_list()
            if client in players:
                for player in players:
                    player.game_id = None
                    player.status = 'prestart'
                    del player.data
                    del player.pole
                del game
        
    def dataReceived(self, client, data):
        if client.status == 'prestart':
            client.status = 'ready'
            self.checkStartGame(client.game_id)
        elif client.status == 'working':
            #client.data = data
            game_id = client.game_id
            game[game_id].data_receive(client, data)

    def sendDataToClients(self):
        for game in self.games:
            players = self.games[game].players_list()
            if players[0].status == 'working' and\
             players[1].status == 'working':
                for player in players:
                    while len(game.data) > 0:
                        player.writeData(game.data.pop(0))
                    while len(player.data) > 0:
                        player.writeData(player.data.pop(0))