package behaviours;

import enums.Step;
import jade.core.AID;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class RequestPerformer extends Behaviour {
    private AID bestSeller;
    private int bestPrice, count = 0;;
    private MessageTemplate mt;
    private Step step = Step.FIRST;

    private final String nameTour;
    private final AID[] sellerAgents;

    public RequestPerformer(AID[] sellerAgents, String nameTour) {
        this.sellerAgents = sellerAgents;
        this.nameTour = nameTour;
    }

    @Override
    public void action() {
        switch (step) {
            case FIRST:
                ACLMessage cfp = new ACLMessage(ACLMessage.CFP);
                for (int i = 0; i < sellerAgents.length; ++i) {
                    cfp.addReceiver(sellerAgents[i]);
                }
                cfp.setContent(nameTour);
                cfp.setConversationId("book-trade");
                cfp.setReplyWith("cfp"+System.currentTimeMillis());
                myAgent.send(cfp);
                mt = MessageTemplate.and(MessageTemplate.MatchConversationId("book-trade"),
                        MessageTemplate.MatchInReplyTo(cfp.getReplyWith()));
                step = Step.SECOND;
                break;
            case SECOND:
                ACLMessage reply = myAgent.receive(mt);
                if (reply != null) {
                    if (reply.getPerformative() == ACLMessage.PROPOSE) {
                        int price = Integer.parseInt(reply.getContent());
                        if (bestSeller == null || price < bestPrice) {
                            bestPrice = price;
                            bestSeller = reply.getSender();
                        }
                    }
                    count++;
                    if (count >= sellerAgents.length) {
                        step = Step.THIRD;
                    }
                } else {
                    block();
                }
                break;
            case THIRD:
                ACLMessage order = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                order.addReceiver(bestSeller);
                order.setContent(nameTour);
                order.setConversationId("book-trade");
                order.setReplyWith("order"+System.currentTimeMillis());
                myAgent.send(order);
                mt = MessageTemplate.and(MessageTemplate.MatchConversationId("book-trade"),
                        MessageTemplate.MatchInReplyTo(order.getReplyWith()));
                step = Step.FOURTH;
                break;
            case FOURTH:
                reply = myAgent.receive(mt);
                if (reply != null) {
                    if (reply.getPerformative() == ACLMessage.INFORM) {
                        System.out.println(nameTour+" successfully purchased from agent "+reply.getSender().getName());
                        System.out.println("Price = "+bestPrice);
                        myAgent.doDelete();
                    } else {
                        System.out.println("Attempt failed: requested book already sold.");
                    }

                    step = Step.FIFTH;
                } else {
                    block();
                }
                break;
        }
    }

    @Override
    public boolean done() {
        if (step == Step.THIRD && bestSeller == null) {
            System.out.println("Attempt failed: " + nameTour + " not available for sale");
        }
        return ((step == Step.THIRD && bestSeller == null) || step == Step.FIFTH);
    }
}
