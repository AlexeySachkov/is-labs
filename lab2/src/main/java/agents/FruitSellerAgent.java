package agents;

import jade.core.Agent;
import jade.core.behaviours.*;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;

import java.util.*;

public class FruitSellerAgent extends Agent {
    //The catalogue of Fruit for sale (maps the name of a Fruit to its price)
    private Hashtable catalogue;
    //The GUI by means of which the user can add Fruit in the catalogue
    private FruitSellerGui myGui;

    //Put agent initializations here
    protected void setup() {
        // Create the catalogue
        catalogue = new Hashtable();

        //Create and show the GUI
        myGui = new FruitSellerGui(this);
        myGui.show();

        //Register the Fruit-selling service in the yellow pages
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
        sd.setType("Fruit-selling");
        sd.setName("JADE-Fruit-trading");
        dfd.addServices(sd);
        try {
            DFService.register(this, dfd);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }

        //Add the behaviour serving queries from buyer agents
        addBehaviour(new OfferRequestsServer());

        //Add the behaviour serving purchase orders from buyer agents
        addBehaviour(new PurchaseOrdersServer());
    }

    //Put agent clean-up operations here
    protected void takeDown() {
        //Deregister from the yellow pages
        try {
            DFService.deregister(this);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }
        //Close the GUI
        myGui.dispose();
        //Printout a dismissal message
        System.out.println("Seller-agent " + getAID().getName() + " terminating.");
    }


    //This is invoked by the GUI when the user adds a new Fruit for sale
    public void updateCatalogue(final String name, final int price) {
        addBehaviour(new OneShotBehaviour() {
            public void action() {
                catalogue.put(name, new Integer(price));
                System.out.println(name + " inserted into catalogue. Price = " + price);
            }
        });
    }

    /**
     * Inner class OfferRequestsServer.
     * This is the behaviour used by Fruit-seller agents to serve incoming requests
     * for offer from buyer agents.
     * If the requested Fruit is in the local catalogue the seller agent replies
     * with a PROPOSE message specifying the price. Otherwise a REFUSE message is
     * sent back.
     */
    private class OfferRequestsServer extends CyclicBehaviour {
        public void action() {
            MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.CFP);
            ACLMessage msg = myAgent.receive(mt);
            if (msg != null) {
                //CFP Message received. Process it
                String name = msg.getContent();
                ACLMessage reply = msg.createReply();

                Integer price = (Integer) catalogue.get(name);
                if (price != null) {
                    //The requested Fruit is available for sale. Reply with the price
                    reply.setPerformative(ACLMessage.PROPOSE);
                    reply.setContent(String.valueOf(price.intValue()));
                } else {
                    //The requested Fruit is NOT available for sale.
                    reply.setPerformative(ACLMessage.REFUSE);
                    reply.setContent("not-available");
                }
                myAgent.send(reply);
            } else {
                block();
            }
        }
    }

    /**
     * Inner class PurchaseOrdersServer.
     * This is the behaviour used by Fruit-seller agents to serve incoming
     * offer acceptances (i.e. purchase orders) from buyer agents.
     * The seller agent removes the purchased Fruit from its catalogue
     * and replies with an INFORM message to notify the buyer that the
     * purchase has been successfully completed.
     */
    private class PurchaseOrdersServer extends CyclicBehaviour {
        public void action() {
            MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.ACCEPT_PROPOSAL);
            ACLMessage msg = myAgent.receive(mt);
            if (msg != null) {
                //ACCEPT_PROPOSAL Message received. Process it
                String name = msg.getContent();
                ACLMessage reply = msg.createReply();

                Integer price = (Integer) catalogue.remove(name);
                if (price != null) {
                    reply.setPerformative(ACLMessage.INFORM);
                    System.out.println(name + " sold to agent " + msg.getSender().getName());
                } else {
                    //The requested Fruit has been sold to another buyer in the meanwhile .
                    reply.setPerformative(ACLMessage.FAILURE);
                    reply.setContent("not-available");
                }
                myAgent.send(reply);
            } else {
                block();
            }
        }
    }
}
