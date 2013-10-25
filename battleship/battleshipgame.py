# coding=utf-8

def make_response(code, **kwargs):
    d = {'code': code,}
    d.update(**kwargs)
    return d

class BattleshipGame:
    """
      One game.
    """

    def __init__(self, player1, player2, size=3):
        self.player1 = player1
        self.player2 = player2
        self.statuses = ['prestart', 'start', 'finish', 'error']
        self.status = self.statuses[0] # wait for both players click "start button"
        self.prestatus = [False, False]
        self.current_player = player1 # player, who can do something
        self.player1.pole = []
        self.player2.pole = []
        self.player1.data = []
        self.player2.data = []
        self.size = size
        self.data = [] # Message for all clients

    def players_list(self):
        return [self.player1, self.player2]

    def players_id_list(self):
        return [self.player1.client_id, self.player2.client_id]

    def set_status(self, status):
        if status in self.statuses:
            self.status = status
        else:
            pass

    def data_receive(self, player, data):
        code = data['code']
        if code == 21:
            #Add Ship
            ships = data.get('ships', None)
            if ships is not None:
                for ship in ships:
                    if ship[0] >= self.size or\
                        ship[1] >= self.size:
                        player.data.append( make_response(code=12) )
                    else:
                        player.pole.append(ship)
                player.data.append(make_response(code=11))
            else:
                player.data.append( make_response(code=12))
        elif code == 22:
            #Resend my Ships
            player.data.append( make_response(17, ships=player.pole) )
        elif code == 23:
            # Start Game
            self.prestatus.pop(0)
            self.prestatus.appned(True)
            if all(self.prestatus):
                self.status = self.statuses[0]
                self.data.append(make_response(code=18))
        elif code == 24:
            #Stop game
            self.status = self.statuses[2]
            self.data.append( make_response(18) )
        elif code == 25:
            if self.status != self.statuses[0]:
                player.data.append( make_response(12))
            return
            coord = (data['x'], data['y'])
            if player == self.current_player:
                # Player have rights to make step
                if player == self.player1:
                    if coord in self.player2.pole:
                        #Nice step
                        player.data.append( make_response(20))
                        self.player2.pole.remove(coord)
                        self.player2.data.append(make_response(16, ships=[coord,]))
                    else:
                        #Bad step
                        player.data.append( make_response(21))
                        self.current_player = self.player2
                    if len(self.player2.pole) == 0:
                        self.data.append( make_response(14, winner=self.player1.client_id))
                else:
                    if coord in self.player1.pole:
                        #Nice step
                        player.data.append( make_response(20))
                        self.player1.pole.remove(coord)
                        self.player1.data.append(make_response(16, ships=[coord,]))
                    else:
                        #Bad step
                        player.data = make_response(21)
                        self.current_player = self.player1
                    if len(self.player1.pole) == 0:
                        self.data .append( make_response(14, winner=self.player2.client_id))
            else:
                player.data.append( make_response(13))