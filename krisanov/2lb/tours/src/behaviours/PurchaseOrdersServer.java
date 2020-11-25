package behaviours;

import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.util.Hashtable;

public class PurchaseOrdersServer extends CyclicBehaviour {

    Hashtable<String, Integer> tours;

    public PurchaseOrdersServer(Hashtable<String, Integer> tours) {
        this.tours = tours;
    }

    @Override
    public void action() {
        MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.ACCEPT_PROPOSAL);
        ACLMessage msg = myAgent.receive(mt);
        if (msg != null) {
            String nameTour = msg.getContent();
            ACLMessage reply = msg.createReply();

            Integer price = tours.remove(nameTour);
            if (price != null) {
                reply.setPerformative(ACLMessage.INFORM);
                System.out.println(nameTour+" sold to agent "+msg.getSender().getName());
            } else {
                reply.setPerformative(ACLMessage.FAILURE);
                reply.setContent("not-available");
            }
            myAgent.send(reply);
        } else {
            block();
        }
    }
}
