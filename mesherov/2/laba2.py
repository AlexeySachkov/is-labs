#"Игра на повышение"
#Агент GameMaster - управляет игрой и знает секретное число
#Агент Player - играет в игру, выдает случайные числа от 0 до 15
#GameMaster зная секретное число, складывает передаваемые числа Player 
#Если сумма случайных чисел меньше, чем загаданное число то Player предлагается загадать еще
#Если загаданные числа Player в сумме дают на одной из попыток секретное число, то он выигрывает
#Если загаданные числа Player в сумме дают больше чем секретное число, то он проигрывает
import json
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import random
a=random.randint(0,100)
#print(f"Загаданное число")
class GameMaster(Agent):
    def __init__(self, aid):
        super(GameMaster, self).__init__(aid=aid, debug=False)
        self.hiddenNumber = a
        display_message(self.aid.localname,f"Загаданное число {a}")

    def react(self, message):
        super(GameMaster, self).react(message)        
        if message.performative == ACLMessage.PROPOSE:
            content = json.loads(message.content)
            numberPlayer = int(content['numberPlayer'])
            display_message(self.aid.localname, "Got Value: {}".format(numberPlayer))
            message = ACLMessage()
            if numberPlayer > self.hiddenNumber:
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="Player@localhost:8011"))
                display_message(self.aid.localname, "LOSE")
            elif numberPlayer == self.hiddenNumber:
                message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                message.add_receiver(AID(name="Player@localhost:8011"))
                display_message(self.aid.localname, "You WIN")
            elif numberPlayer < self.hiddenNumber :
                message.set_performative(ACLMessage.REJECT_PROPOSAL)
                message.add_receiver(AID(name="Player@localhost:8011"))
                display_message(self.aid.localname, "try next")
            self.send(message)


class Player(Agent):
    def __init__(self, aid):
        super(Player, self).__init__(aid=aid, debug=False)
        #self.counter = 0
        self.numberPlayer = 0

    def on_start(self):
        super().on_start()
        self.call_later(10, self.sendValue)
        
    def sendValue(self):
        display_message(self.aid.localname, "Sending Value")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.set_content(json.dumps({'numberPlayer': self.numberPlayer}))
        message.add_receiver(AID(name="GameMaster@localhost:8022"))
        self.send(message)

    def react(self, message):
        super(Player, self).react(message)

        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            pass
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            b=random.randint(0,15)
            self.numberPlayer = self.numberPlayer + b
            display_message(self.aid.localname,b)
            self.sendValue()



if __name__ == '__main__':

    agents = list()

    
    player = Player(AID(name="Player@localhost:8011"))
    gameMaster = GameMaster(AID(name="GameMaster@localhost:8022"))

    agents.append(player)
    agents.append(gameMaster)

    start_loop(agents)

# [GameMaster] 30/11/2020 01:53:39.830 --> Загаданное число72
# [ams@localhost:8000] 30/11/2020 01:53:39.867 --> Agent Player@localhost:8011 successfully identified.
# [ams@localhost:8000] 30/11/2020 01:53:39.868 --> Agent GameMaster@localhost:8022 successfully identified.
# [Player@localhost:8011] 30/11/2020 01:53:39.871 --> Identification process done.
# [GameMaster@localhost:8022] 30/11/2020 01:53:39.872 --> Identification process done.
# [Player] 30/11/2020 01:53:49.849 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.853 --> Got Value: 0
# [GameMaster] 30/11/2020 01:53:49.854 --> try next
# [Player] 30/11/2020 01:53:49.858 --> 12
# [Player] 30/11/2020 01:53:49.866 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.871 --> Got Value: 12
# [GameMaster] 30/11/2020 01:53:49.881 --> try next
# [Player] 30/11/2020 01:53:49.885 --> 8
# [Player] 30/11/2020 01:53:49.886 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.891 --> Got Value: 20
# [GameMaster] 30/11/2020 01:53:49.892 --> try next
# [Player] 30/11/2020 01:53:49.895 --> 10
# [Player] 30/11/2020 01:53:49.895 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.900 --> Got Value: 30
# [GameMaster] 30/11/2020 01:53:49.901 --> try next
# [Player] 30/11/2020 01:53:49.903 --> 13
# [Player] 30/11/2020 01:53:49.914 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.918 --> Got Value: 43
# [GameMaster] 30/11/2020 01:53:49.919 --> try next
# [Player] 30/11/2020 01:53:49.923 --> 14
# [Player] 30/11/2020 01:53:49.929 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.933 --> Got Value: 57
# [GameMaster] 30/11/2020 01:53:49.934 --> try next
# [Player] 30/11/2020 01:53:49.937 --> 4
# [Player] 30/11/2020 01:53:49.938 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.948 --> Got Value: 61
# [GameMaster] 30/11/2020 01:53:49.949 --> try next
# [Player] 30/11/2020 01:53:49.952 --> 3
# [Player] 30/11/2020 01:53:49.953 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.956 --> Got Value: 64
# [GameMaster] 30/11/2020 01:53:49.964 --> try next
# [Player] 30/11/2020 01:53:49.968 --> 15
# [Player] 30/11/2020 01:53:49.969 --> Sending Value
# [GameMaster] 30/11/2020 01:53:49.972 --> Got Value: 79
# [GameMaster] 30/11/2020 01:53:49.980 --> LOSE
