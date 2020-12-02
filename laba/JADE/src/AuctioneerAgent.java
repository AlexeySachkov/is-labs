import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.Behaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class AuctioneerAgent extends Agent {
    private AID[] bidderAgents;

    private String itemName;
    private Integer itemPrice;

    @Override
    protected void setup() {
        System.out.println("Агент-аукционер присоединился");

        //Проверяем наличие аргументов аукционера
        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            itemName = (String) args[0];
            itemPrice = Integer.parseInt((String) args[1]);

            System.out.println("Добрый день, уважаемые покупатели! Сегодня я продаю \"" + itemName + "\". Начальная цена лота = " + itemPrice + " рублей");
            System.out.println("Пожалуйста, делайте ваши ставки!");

            //Если введены агрументы для аукционера, то получаем всех участников торгов, иначе выводим что ничего не выставленно на аукцион
            addBehaviour(new OneShotBehaviour() {
                @Override
                public void action() {

                    //Используем Yellow Pages
                    DFAgentDescription template = new DFAgentDescription();
                    ServiceDescription sd = new ServiceDescription();
                    sd.setType("auction-bidder");
                    template.addServices(sd);

                    try {
                        DFAgentDescription[] result = DFService.search(myAgent, template);

                        bidderAgents = new AID[result.length];
                        for (int i = 0; i < result.length; i++) {
                            bidderAgents[i] = result[i].getName();
                        }
                    } catch (FIPAException e) {
                        e.printStackTrace();
                    }

                    myAgent.addBehaviour(new AuctionPerformer());
                }
            });
        } else {
            System.out.println("Ничего не выставлено на аукцион");
            doDelete();
        }
    }

    private class AuctionPerformer extends Behaviour {
        private int step = 0;
        private Map<AID, Integer> receivedProposals = new HashMap<>();
        private int numExpectedProposals = 0;
        private MessageTemplate mt;
        private AID highestBidder = null;
        private int highestBid = 0;
        private int roundsWithNoOffers = 0;

        @Override
        public void action() {
            switch (step) {
                case 0:
                    // Повторно инициализируем ожидаемые предложения
                    receivedProposals = new HashMap<>();
                    numExpectedProposals = 0;

                    // Отправляем продаваемый товар и стартовую цену
                    ACLMessage cfp = new ACLMessage(ACLMessage.CFP);

                    for (int i = 0; i < bidderAgents.length; i++) {
                        if (highestBidder == null || (highestBidder != null && bidderAgents[i].compareTo(highestBidder) != 0)) {
                            cfp.addReceiver(bidderAgents[i]);

                            numExpectedProposals++;
                        }
                    }

                    if (highestBidder != null) {
                        cfp.setContent(itemName + "||" + highestBid);
                    } else {
                        cfp.setContent(itemName + "||" + itemPrice);
                    }

                    cfp.setConversationId("auction");
                    cfp.setReplyWith("cfp" + System.currentTimeMillis());

                    myAgent.send(cfp);

                    mt = MessageTemplate.and(
                            MessageTemplate.MatchConversationId("auction"),
                            MessageTemplate.MatchInReplyTo(cfp.getReplyWith()));

                    step = 1;
                    break;
                case 1:
                    ACLMessage reply = myAgent.receive(mt);

                    if (reply != null) {

                        switch (reply.getPerformative()) {
                            case ACLMessage.PROPOSE:
                              // Получаем ставку
                                receivedProposals.put(reply.getSender(), Integer.parseInt(reply.getContent()));

                                System.out.println(reply.getSender().getName() + " делает ставку " + reply.getContent() + " рублей");

                                // Повторная инициализация, если есть новые предложения от другого участника торгов
                                roundsWithNoOffers = 0;

                                break;
                            case ACLMessage.REFUSE:
                                // Агент не интересуется товаром
                                receivedProposals.put(reply.getSender(), null);

                                // Увеличиваем количество раундов без новых предложений от другого участника торгов
                                roundsWithNoOffers++;
                                break;
                        }

                        if (receivedProposals.size() == numExpectedProposals) {
                            step = 2;

                        }

                    } else {
                        block();
                    }
                    break;
                case 2:

                    //Проверяем ставки и сохраняем самую высокую
                    Iterator<Map.Entry<AID, Integer>> iter = receivedProposals.entrySet().iterator();
                    while (iter.hasNext()) {
                        Map.Entry<AID, Integer> item = iter.next();
                        if (item.getValue() != null && highestBid < item.getValue()) {
                            highestBidder = item.getKey();
                            highestBid = item.getValue();
                        }
                    }

                    if (highestBidder != null) {
                        System.out.println( " ЧТО?? Я слышу кто-то крикнул новую цену " + highestBid + " рублей?! \n Итак! \n Самая высокая ставка на данный момент: " + highestBid + " рублей от " + highestBidder.getName());
                    } else {
                        System.out.println("Недействительная ставка!");
                    }

                    // Отправить предложение принять ставку участника торгов, предложившему самую высокую цену

                    ACLMessage accept = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                    accept.addReceiver(highestBidder);
                    accept.setContent(itemName + "||" + highestBid);
                    accept.setConversationId("auction");
                    accept.setReplyWith("bid-ok" + System.currentTimeMillis());

                    myAgent.send(accept);

                    //Отклонить остальные ставки

                    receivedProposals.keySet().stream()
                            .filter(aid -> aid != highestBidder && receivedProposals.get(aid) != null)
                            .forEach(aid -> {
                                ACLMessage reject = new ACLMessage(ACLMessage.REJECT_PROPOSAL);
                                reject.addReceiver(highestBidder);
                                reject.setContent(itemName + "||" + receivedProposals.get(aid));
                                reject.setConversationId("auction");
                                reject.setReplyWith("bid-reject" + System.currentTimeMillis());

                                myAgent.send(reject);
                            });

                    step = 3;
                    break;
                case 3:

                    if (roundsWithNoOffers == 1) {
                        step = 4;
                    } else {
                        step = 0;
                    }
                    break;
                case 4:

                    for (int i = 1 ; i < 4 ; i++){

                        System.out.println(highestBid + " рублей   " + i);
                    }

                    System.out.println("Продано! " + itemName + " получает участник торгов " + highestBidder.getName() + " за " + highestBid + " рублей. Поздравляем!");

                    step = 5;
                    break;
            }
        }
        @Override
        public boolean done() {
            return (step == 5);
        }
    }
}