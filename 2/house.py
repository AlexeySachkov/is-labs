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
#pade start-runtime --port 8000 house.py --username 1 --password 1
#Python 3.8.5

''' 
Сделано
    Генерация людей.
    Обмен сообщениями между людьми и отцом. Предварительное удаление у человека энергии
    Добавлено первоначальное описание людей.
    Каждое обращение человека сопровождается списком свободных задач
частично сделано
    Распределение задач
    Продумано ACCEPT и reject. *особено reject*
Нужно
    Генерация задач
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
        display_message(
            self.aid.localname, f'''
            Я {self.sex}, мне {self.age} лет,
            моя энергия {self.energy},
            времени для работы {self.timeToWork},
            предпочтение {self.preferences}'''
            )
        self.call_later(randrange(10,25), self.send_proposal)
    def send_proposal(self):
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
        self.send(message)


    def react(self, message):
        super(Houseworker, self).react(message)
        # Продумать логику ACCEPT_PROPOSAL и reject
        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            #display_message(self.aid.localname,self.energy)
            info = pickle.loads(message.content)
            name = info['name']            
            time = info['timeToWork']
            energy = info['energy']
            self.energy -= energy
            self.timeToWork -= time
            #display_message(self.aid.localname,self.energy)
            #выполнил(А)
            display_message(self.aid.localname,
                f'''
                Я выполнил {name}. 
                У меня осталось {self.energy} энергии.
                У меня осталось {self.timeToWork} времени для работы''')
            self.call_later(randrange(10,int(time/20)+10), self.send_proposal)
        if message.performative == ACLMessage.REJECT_PROPOSAL:
            display_message(self.aid.localname,"Подходящей работы нет")

        if message.performative == ACLMessage.INFORM:
            if message.content == 0:
                display_message(self.aid.localname,"Задач больше нет ")
            

class Employer(Agent):
    def __init__(self, aid):
        super(Employer, self).__init__(aid=aid, debug=False)     

    def tasksToDo(self):
        tasks = []
        for i in range(randrange(2,10)):
            tasks.append([f'task{i}','any', 0, randrange(60 , 60*3, 5), randrange(110, 350, 10), randrange(1,3)])                
        return tasks
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
        self.tasks = self.tasksToDo()
        display_message(self.aid.localname,'Ну, граждане алкоголики, хулиганы, тунеядцы, кто хочет сегодня поработать?')

    def selectionTask(self, sex, age, energy, time, preferences):
        numberOfTasks = len(self.tasks)
        if numberOfTasks == 0:
            return 0, self.tasks
        for taskNum in range(numberOfTasks):
            task = self.tasks[taskNum]
            nameTask = task[0]
            sexTask = task[1]
            ageTask = task[2]
            energyTask = task[3]
            timeTask = task[4]
            countTask = task[5]
            if energy >= energyTask and time >= timeTask:
                #add check sex
                #add check age                         
                self.tasks[taskNum][5]-=1
                if self.tasks[taskNum][5] == 0:
                    self.tasks.remove(task)
                return [nameTask,energyTask,timeTask], self.tasks
            else:
                continue
        return 0, self.tasks
        # Идем по всем такскам и проверям на требования. (sex,age)
        # Проверяем есть ли требуемая энергия и требуемое время для выполнения задачи.
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
            #display_message(self.aid.localname, pickle.loads(message.content))
            #display_message(self.aid.localname, pickle.loads(message.content)['age'])
            #display_message(self.aid.localname, message)
            fromName = message.sender.name
            specifications = pickle.loads(message.content)
            sex = specifications['sex']
            age = specifications['age']
            timeToWork = specifications['timeToWork']
            energy = specifications['energy']
            preferences = specifications['preferences']
            #display_message(self.aid.localname, fromName)
            if self.tasks:
                display_message(self.aid.localname,f''' 
    Ответ для {message.sender.name} energy = {energy}, time = {timeToWork}
    Доступные задачи: 
    [name, sex, age, energy, time, count]''')
                for task in self.tasks:
                    print(task)
            message = ACLMessage()#reply = message.create_reply()
            if self.tasks:
                task, self.tasks =  self.selectionTask(sex, age, energy, timeToWork, preferences)
                if task != 0:
                    message.set_performative(ACLMessage.ACCEPT_PROPOSAL)
                    info = {
                        'name': task[0],
                        'energy': task[1],
                        'timeToWork': task[2],
                        
                    }
                    info_tasks = pickle.dumps(info, 0)
                    message.set_content(info_tasks)

                else:
                    message.set_performative(ACLMessage.REJECT_PROPOSAL)
            else:
                message.set_content(len(self.tasks))
                message.set_performative(ACLMessage.INFORM)
            message.add_receiver(fromName)
            # заглушка. Проверка уменьшении энергии у человека.
            # Будем выставлять 2 параметра: [energy, time]. Через dumps            
            self.send(message)

if __name__ == '__main__':
    agents = []
    
    with open('mansname.txt',encoding="utf-8") as f:
        mans = f.readlines()
    with open('womennames.txt',encoding="utf-8") as f:
        womens = f.readlines()
    quantity = randrange(2, len(mans)) + randrange(2, len(womens))
    quantity = 5
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