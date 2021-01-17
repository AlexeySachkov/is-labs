package ru.nntu;

import com.google.gson.Gson;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import java.util.HashMap;

public class ManagerBehaviour extends CyclicBehaviour {
    HashMap<String, Order> optimalTaxi = new HashMap<>();
    int maxPrice = 10;
    int minPrice = 7;
    int price = (int) Math.round(Math.random()*(maxPrice-minPrice) + minPrice);
    int companyId;

    ManagerBehaviour(int companyId){
        this.companyId = companyId;
    }

    @Override
    public void action(){
        ACLMessage message = myAgent.receive();
        if (message != null) {
            // Обработка сообщений от клиентов.
            if (message.getSender().getLocalName().matches("Client(.*)")){
                // Сообщение с информацией о маршруте. Пересылаем всем таксистам.
                if (message.getPerformative() == ACLMessage.INFORM){
                    ACLMessage messageToDriver = new ACLMessage(ACLMessage.INFORM);
                    for (int i = 1; i <= new Company().getCountDrivers(companyId); i++)
                        messageToDriver.addReceiver(new AID("Driver_" + companyId + "_" + i, AID.ISLOCALNAME));
                    messageToDriver.setContent(message.getContent());
                    System.out.println(myAgent.getLocalName() + " -> " + "ALL_Driver:" + " Поступил новый заказ.");
                    myAgent.send(messageToDriver);
                }
                // Подтверждение поездки. Пересылаем нужному водителю.
                if (message.getPerformative() == ACLMessage.ACCEPT_PROPOSAL){
                    ACLMessage messageToDriver = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                    String driver = new Gson().fromJson(message.getContent(), Order.class).getTaxi();
                    messageToDriver.addReceiver(new AID(driver, AID.ISLOCALNAME));
                    messageToDriver.setContent(message.getContent());
                    optimalTaxi.remove(driver);
                    System.out.println(myAgent.getLocalName() + " ->" + driver +  ": " + "Клиент подтвердил условия поездки.");
                    myAgent.send(messageToDriver);

                }
                // Отказ от поездки. также пересылаем нужному водителю.
                if (message.getPerformative() == ACLMessage.REJECT_PROPOSAL){
                    ACLMessage messageToDriver = new ACLMessage(ACLMessage.REJECT_PROPOSAL);
                    String client = new Gson().fromJson(message.getContent(), String.class);
                    Order driver =optimalTaxi.remove(client);
                    messageToDriver.addReceiver(new AID(driver.getTaxi(), AID.ISLOCALNAME));
                    System.out.println(myAgent.getLocalName() + " -> " + driver.getTaxi() +  ": " + "Клиент отказался от поездки.");
                    myAgent.send(messageToDriver);
                }
            }
            // Обработка сообщений от таксистов.
            if (message.getSender().getLocalName().matches("Driver(.*)")){
                // Поиск самого ближайшего таксиста к клиенту. Полученные данные о времени и стоимости пересылаются клиенту.
                if (message.getPerformative() == ACLMessage.PROPOSE){
                    Order order = new Gson().fromJson(message.getContent(), Order.class);
                    if (optimalTaxi.get(order.getClient()) == null){
                        optimalTaxi.put(order.getClient(), order);
                    }
                    else{
                        /* Если текущий оптимальный вариант проигрывает по времени полученному от таксиста предложению,
                        то полученное предложение становится оптимальным. Ждем ответа от всех таксистов.
                         */
                        if (optimalTaxi.get(order.getClient()).getWaitingTime() > order.getWaitingTime()){
                            ACLMessage messageToDriver = new ACLMessage(ACLMessage.REJECT_PROPOSAL);
                            messageToDriver.addReceiver(new AID(optimalTaxi.get(order.getClient()).getTaxi(), AID.ISLOCALNAME));
                            System.out.println(myAgent.getLocalName() + " -> " + optimalTaxi.get(order.getClient()).getTaxi() + ": Найден автомобиль, ближе к клиенту.");
                            myAgent.send(messageToDriver);
                            order.setVariables(optimalTaxi.get(order.getClient()).getVariables());
                            optimalTaxi.put(order.getClient(), order);
                        }
                        else{
                            ACLMessage messageToDriver = new ACLMessage(ACLMessage.REJECT_PROPOSAL);
                            messageToDriver.addReceiver(new AID(order.getTaxi(), AID.ISLOCALNAME));
                            System.out.println(myAgent.getLocalName() + " -> " + order.getTaxi() + " Найден автомобиль, ближе к клиенту.");
                            myAgent.send(messageToDriver);
                            order = optimalTaxi.get(order.getClient());
                            order.setVariables(1);
                            optimalTaxi.put(order.getClient(), order);

                        }
                    }
                    // Отправка сообщения пользователю.
                    if (optimalTaxi.get(order.getClient()).getVariables() == new Company().getCountDrivers(companyId)){
                        ACLMessage messageToClient = new ACLMessage(ACLMessage.PROPOSE);
                        messageToClient.addReceiver(new AID(order.getClient(), AID.ISLOCALNAME));
                        Order content = optimalTaxi.get(order.getClient());
                        content.setPrice(Data.getTime(content.getFrom(), content.getTo())*price);
                        messageToClient.setContent(new Gson().toJson(optimalTaxi.get(order.getClient())));
                        System.out.println(myAgent.getLocalName() + " -> " + order.getClient() + ": Ближайший автомобиль будет через " + content.getWaitingTime() + " минут. Стоимость поездки: " + content.getPrice());
                        myAgent.send(messageToClient);
                    }
                }
            }
        }
    }

}

