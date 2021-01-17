package ru.nntu;

import com.google.gson.Gson;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import java.util.ArrayList;

// Поведение клиента
public class ClientBehaviour extends CyclicBehaviour{
    // Максимальное время, которое клиент готов ожидать такси.
    private final int maxWaitingTime = 30;
    private int step = 0;
    private final ArrayList<Order> offers = new ArrayList<>();
    @Override
    public void action(){
        ACLMessage msg = myAgent.receive();
        if (step == 0){
            // Выбираем маршрут поездки и отправляем сообщение всем диспетчерам.
            ACLMessage message = new ACLMessage(ACLMessage.INFORM);
            for (int i = 1; i <= new Company().getCountCompany(); i++)
                message.addReceiver(new AID("Manager_" + i, AID.ISLOCALNAME));
            Order order = createRoute();
            order.setClient(myAgent.getLocalName());
            message.setContent(new Gson().toJson(order));
            System.out.println(myAgent.getLocalName() + " -> ALL_Manager: Я еду из области "  + order.getFrom() + " в " + order.getTo() + ".");
            myAgent.send(message);
            step++;
        }
        else {
            if (msg != null) {
                // Выбираем оптимальный вариант из предложенных диспетчерами.
                // Для лучшего варианта подтверждаем поездку, остальным отправляем сообщение с отказом от поездки.
                // Если время ожидания превышает максимальное заданное, то всем отправляем сообщение об отказе от поездки.
                if (msg.getPerformative() == ACLMessage.PROPOSE){
                    offers.add(new Gson().fromJson(msg.getContent(), Order.class));
                    if (offers.size() == new Company().getCountCompany()){
                        Order bestOrder = offers.get(0);
                        for (Order order: offers){
                            if (order.getWaitingTime()*10 + order.getPrice() < bestOrder.getWaitingTime()*10 + bestOrder.getPrice() && order.getWaitingTime() <= maxWaitingTime)
                                bestOrder = order;
                        }
                        if (bestOrder.getWaitingTime() <= maxWaitingTime) {
                            ACLMessage messageAccept = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                            messageAccept.addReceiver(new AID("Manager_" + bestOrder.getTaxi().split("_")[1], AID.ISLOCALNAME));
                            messageAccept.setContent(new Gson().toJson(bestOrder));
                            System.out.println(myAgent.getLocalName() + " -> " + "Manager_" + bestOrder.getTaxi().split("_")[1] + ": Я ожидаю такси.");
                            myAgent.send(messageAccept);
                        }
                        ACLMessage messageReject = new ACLMessage(ACLMessage.REJECT_PROPOSAL);
                        String out = "";
                        for (Order order: offers){
                            if (!bestOrder.equals(order) || bestOrder.getWaitingTime() > maxWaitingTime){
                                messageReject.addReceiver(new AID("Manager_" + order.getTaxi().split("_")[1], AID.ISLOCALNAME));
                                out = out + "Manager_" + order.getTaxi().split("_")[1] + " ";
                            }
                        }
                        messageReject.setContent(new Gson().toJson(myAgent.getLocalName()));
                        System.out.println(myAgent.getLocalName() + " -> " + out.substring(0, out.length()-1) + ":  " + "Я хочу отменить поездку.");
                        myAgent.send(messageReject);
                    }
                }
            }
        }
    }

    // Генерация случайного маршрута.
    public static Order createRoute(){
        return new Order((int) Math.round(Math.random()*(Data.getCountAreas()-1)), (int) Math.round(Math.random()*(Data.getCountAreas()-1)));
    }
}
