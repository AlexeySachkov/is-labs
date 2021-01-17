package ru.nntu;

import com.google.gson.Gson;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.tools.introspector.gui.MyDialog;

import java.util.Date;

public class TaxiBehaviour extends CyclicBehaviour {
    private int currentZone = (int) Math.round(Math.random()*(Data.getCountAreas()-1));;
    // Время, которое таксист занят, время поездки с клиентом.
    private int time = 0;
    private long lastTime = new Date().getTime();
    // simulationTime (мс). Каждые 10 секунд параметр time уменьшается на 1. Скорость симуляции.
    private final int simulationTime = 10000;
    private boolean free = true;

    @Override
    public void action(){
        // Симуляция поездки с клиентом.
        if (new Date().getTime() - lastTime >= simulationTime && time > 0){
            time--;
            lastTime = new Date().getTime();
        }
        ACLMessage message = myAgent.receive();
        if (message != null) {
            // Определяем, за какое время таксист доберется до клиента.
            if (message.getPerformative() == ACLMessage.INFORM){
                Order order = new Gson().fromJson(message.getContent(), Order.class);
                ACLMessage reply = new ACLMessage(ACLMessage.PROPOSE);
                reply.addReceiver(message.getSender());
                int waitingTime;
                if (free){
                    waitingTime = time+Data.getTime(currentZone, order.getFrom());
                    free = false;}
                else waitingTime = Integer.MAX_VALUE;
                order = new Order(order.getFrom(), order.getTo(), waitingTime, order.getClient(), myAgent.getLocalName());
                reply.setContent(new Gson().toJson(order));

                System.out.println(myAgent.getLocalName() + "->" + message.getSender().getLocalName() +  ": Я смогу забрать клиента через: " + order.getWaitingTime() + " минут.");

                myAgent.send(reply);
                }
            // Если клиент принял предложение, то добавляем симуляцию поездки.
            if (message.getPerformative() == ACLMessage.ACCEPT_PROPOSAL){
                Order order = new Gson().fromJson(message.getContent(), Order.class);
                time += Data.getTime(order.getFrom(), order.getTo());
                currentZone = order.getTo();
                free = true;
            }
            if (message.getPerformative() == ACLMessage.REJECT_PROPOSAL)
                free = true;
            }
        }
    }



