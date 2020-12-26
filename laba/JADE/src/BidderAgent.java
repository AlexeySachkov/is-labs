import jade.core.Agent;
import jade.core.behaviours.Behaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.util.concurrent.ThreadLocalRandom;

public class BidderAgent extends Agent {
    private int wallet;

    @Override
    protected void setup() {

        setRandomWallet();

        addBehaviour(new BidRequestsServer());

        // Регистрируем агента с использованием Yellow Pages
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
        sd.setType("auction-bidder");
        sd.setName("MultiAgentSystem-auctions");
        dfd.addServices(sd);

        try {
            DFService.register(this, dfd);
        } catch (FIPAException e) {
            e.printStackTrace();
        }
        System.out.println(getAID().getName() + " готов купить предмет, выставленный на аукцион. С собой в кошельке у меня " + wallet + " рублей");
    }

    // Генерируем случайное число денег в кошельке участника торгов
    private void setRandomWallet() {
        int min = 100000;
        int max = 1000000;

        wallet = ThreadLocalRandom.current().nextInt(min, max);
    }

    //Завершаем работу агента
    @Override
    protected void takeDown() {
        try {
            DFService.deregister(this);
        } catch (FIPAException e) {
            e.printStackTrace();
        }

        System.out.println("Участник торгов " + getAID().getName() + " уходит с аукциона.");
    }

    private class BidRequestsServer extends Behaviour {
        private String itemName;
        private Integer itemPrice;

        @Override
        public void action() {
           // MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.CFP);
            ACLMessage msg = myAgent.receive();

            if (msg != null) {
                parseContent(msg.getContent());

                ACLMessage reply = msg.createReply();
                int bid;

                if (itemPrice < wallet / 2) {
                    //Делаем новую ставку на 5-10% выше полученного значения предыдущей ставки
                    bid = (int) (itemPrice + itemPrice * ((float) ThreadLocalRandom.current().nextInt(5, 10) / 10));

                    reply.setPerformative(ACLMessage.PROPOSE);
                    reply.setContent(String.valueOf(bid));
                } else {
                    reply.setPerformative(ACLMessage.REFUSE);
                }

                myAgent.send(reply);
            } else {
                block();
            }
        }

        private void parseContent(String content) {
            String[] split = content.split("\\|\\|");

            itemName = split[0];
            itemPrice = Integer.parseInt(split[1]);
        }

        // Завершаем поведение
        @Override
        public boolean done() {
            return false;
        }
    }
}