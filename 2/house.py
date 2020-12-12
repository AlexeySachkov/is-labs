'''
ЗАДАЧА ЕЩЕ НЕ ВЫПОЛНЕНА. ЕЩЕ В РАЗРАБОТКЕ.
Кратко: Отец раздает задачи. Люди их выполняют. Программа заканчивается если никто не может выполнить больше задачи, например, они кончились.
Полно:
В общем и целом, есть дом (большой). В доме есть отец семейства, который очень важный, но сам работать не любит.
Отец любит и умеет раздавать задачи по дому. Задачи по дому (!)могут(!) иметь требования в виде возраста и/или пола.
Кроме того, задачи требую время на выполнения и "добавляют" усталости исполнителю.
Есть множество людей(исполнители) живущих в этом доме.
Они готовы выполнять задачи пока не устанут либо пока не останется свободных задач, по которым они подходят по требованиям (пол, возраст).
У людей есть пол и возраст, а так же максимальное время, которое они готовы работать, и бодрость (бодрость уменьшается, а значит усталость растет).
Еще у людей есть предпочтение (одно):
    Человек любит работать и готов выполнить любую задачу (any)
    Человек хочет самую "быстровыполнимую" задачу (Fast-paced)
    Человек хочет самую сложную (по усталости) задачу (Complex)
    Человек берется за самую сложную и долговыполнимую задачу . Расщитывается по time*hard (ComplexLong)
'''
#pade start-runtime --port 8000 house.py
#Python 3.8.5

''' 
Сделано
    Генерация людей.
    Обмен сообщениями между людьми и отцом. Предварительное удаление у человека энергии
Нужно
    Генерация задач
    Распределение задач
    Продумать ACCEPT и reject. *особено reject*
'''


from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from random import randrange, choice
import pickle


class Houseworker(Agent):
    def __init__(self, aid,sex,age,timeToWork,energy,preferences):
        super(Houseworker, self).__init__(aid=aid, debug=False)
        self.sex = sex
        self.age = age
        self.timeToWork = timeToWork
        self.energy = energy
        self.preferences = preferences
        #print(aid.name,'\t',self.sex,self.age,self.timeToWork,self.energy,self.preferences, sep='\t')
    def on_start(self):
        super().on_start()
        self.call_later(10, self.send_proposal)
    def send_proposal(self):
        #display_message(self.aid.localname, "!!!!!!!!!!!!!!!!!!!")
        message = ACLMessage()
        message.set_performative(ACLMessage.PROPOSE)
        message.add_receiver(AID(name="Employer@localhost:8011"))
        info = {
            'sex': self.sex,
            'age': self.age,
            'timeToWork': self.timeToWork,
            'energy': self.energy,
            'preferences': self.preferences
            }
        info_dump = pickle.dumps(info,0)
        message.set_content(info_dump)
        
        #print(message)
        self.send(message)


    def react(self, message):
        super(Houseworker, self).react(message)
        # Продумать логику ACCEPT_PROPOSAL и reject
        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            display_message(self.aid.localname,self.energy)
            self.energy -=message.content
            display_message(self.aid.localname,self.energy)
            display_message(self.aid.localname,"GOOD")
            pass

class Employer(Agent):
    def __init__(self, aid):
        super(Employer, self).__init__(aid=aid, debug=False)
        tasks = self.tasksToDo()

    def tasksToDo(self):
        pass
        # Генерируем список задач по дому
        # example task - name, sex, age, energy, time, count
        # Все параметры рандом
        # Name - название работы. Из файла.
        # Требования:   sex =  [0,1,2] = 0-любой, 1-man, 2-woman
        #               age = [0,[a,b]] = 0-любой, [a,b] от а до b (a<b)
        # Условия/обязаности/затраты
        #                 10<energy<150
        #                 5<time<120
        # count - количество работы. [1,5]               
                           
    def on_start(self):
        super().on_start()
        
        display_message(self.aid.localname,
            "Ну, граждане алкоголики, хулиганы, тунеядцы, кто хочет сегодня поработать?"
            )
    def selectionTask(self, tasks, sex, age, preferences):
        pass
        # Идем по всем такскам и проверям на требования. (sex,age)
        # Если подходит то,
        #   Смотрим на preferences 
        #       'Any' = берем первую подходящую,
        #       Остальные ('Fast-paced', 'Complex', 'ComplexLong') ищем максимально подходящую (без сортировки). За N
        #   count -=1
        #   Если count == 0 -> Удаляем задачу из тасков
        # return task, tasks (выбранная таска, обновленный список тасок)
        # если таска не выбрана то возвращаем 0,tasks

    def react(self, message):
        super(Employer, self).react(message)
        if message.performative == ACLMessage.PROPOSE:

            display_message(self.aid.localname, pickle.loads(message.content))
            #display_message(self.aid.localname, pickle.loads(message.content)['age'])
            #display_message(self.aid.localname, message)
            fromname = message.sender.name
            display_message(self.aid.localname, fromname)
            message = ACLMessage()#reply = message.create_reply()
            # task, self.tasks =  selectionTask(arguments)
            # task !=0, то ACCEPT_PROPOSAL, иначе reject
            message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
            message.add_receiver(fromname)
            # заглушка. Проверка уменьшении энергии у человека.
            # Будем выставлять 2 параметра: [energy, time]. Через dumps
            message.set_content(randrange(1, 60)) 
            self.send(message)

            
            



if __name__ == '__main__':

    agents = []
    
    with open('mansname.txt',encoding="utf-8") as f:
        mans = f.readlines()
    with open('womennames.txt',encoding="utf-8") as f:
        womens = f.readlines()
    quantity = randrange(2, len(mans)) + randrange(2, len(womens))

    ids = set()
    while len(ids)!=quantity:
        ids.add(str(randrange(100, 1000)))
    ids = sorted(ids)

    #generete houseworker
    for i in range(quantity):
        rnd = choice([True, False])
        sex = 'man' if rnd else 'women'
        name = mans[randrange(0, len(mans))] if rnd else womens[randrange(0, len(womens))]
        name = name[:len(name)-1] # -1 = delete '\n'
        age = randrange(10, 85)
        #Young people have less time to work (many different other activities)
        timeToWork = randrange(60 + age * 3, 60*8, 5) #minutes / 60*8 max time = work day
        #Younger people have more energy
        energy = randrange(110 - age, 1050 - age * 5, 10)
        preferences =  choice(['Any', 'Fast-paced','Complex','ComplexLong']) #Любая, Быстрая, Сложная, Быстрая*Сложная
        houseworker =Houseworker(
            AID(name=name+ids[i]+'@localhost:8'+ids[i]),
            sex=sex,
            age=age,
            timeToWork=timeToWork,
            energy=energy,
            preferences=preferences
        )
        agents.append(houseworker)
     
    '''agents.append(Houseworker(
            AID(name='name'+'2'+'@localhost:8022'),
            sex='man',
            age=55,
            timeToWork=345,
            energy=645
        ))
    agents.append(Houseworker(
            AID(name='na3me'+'23'+'@localhost:8023'),
            sex='man',
            age=525,
            timeToWork=3415,
            energy=6425
        )) '''    
    employerName = "Employer@localhost:8011"    
    employer = Employer(AID(name=employerName))    
    agents.append(employer)

    start_loop(agents)