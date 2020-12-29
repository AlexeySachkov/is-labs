package travelagent;
import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import java.util.Hashtable;
public class TravelProvider extends Agent {
    private static final long serialVersionUID = 1L;
    private Hashtable<String, String> catalogue;
    private TravelProviderGui myGui;
    // Put agent initializations here
    protected void setup() {
        // Create the catalogue
        catalogue = new Hashtable<String, String>();
        // Create and show the GUI 
        myGui = new TravelProviderGui(this);
        myGui.showGui();
        // Register the travel-order service in the yellow pages
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
        sd.setType("travel-order");
        sd.setName("JADE-book-trading");
        dfd.addServices(sd);
        try {
            DFService.register(this, dfd);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }
        // Add the behaviour serving queries from buyer agents
        addBehaviour(new OfferRequestsServer());
        // Add the behaviour serving purchase orders from buyer agents
        addBehaviour(new PurchaseOrdersServer());
    }
    // Put agent clean-up operations here
    @Override
    protected void takeDown() {
        // Deregister from the yellow pages
        try {
            DFService.deregister(this);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }
        // Close the GUI
        myGui.dispose();
        // Printout a dismissal message
        System.out.println("Provider  " + getAID().getName() + " is stopped.");
    }
    public void updateCatalogue(final String tittle, final String price, final int jb) {
        addBehaviour(new OneShotBehaviour() {
            /**
             *
             */
            private static final long serialVersionUID = 1L;
            @Override
            public void action() {
                final String gb=price+"/"+jb;
                catalogue.put(tittle, gb);
                 String[] day = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
                System.out.println(tittle + " departure "+day[jb]+" put into the catalog at a cost = " + price);
            }
        });
    }
    private class OfferRequestsServer extends CyclicBehaviour {
        private static final long serialVersionUID = 1L;
        @Override
        public void action() {
            MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.CFP);
            ACLMessage msg = myAgent.receive(mt);
            if (msg != null) {
                // CFP Message received. Process it
                String title = msg.getContent();
                ACLMessage reply = msg.createReply();

                String price = catalogue.get(title);
                if (price != null) {
                                   reply.setPerformative(ACLMessage.PROPOSE);
                    reply.setContent(price);
                } else {
                                  reply.setPerformative(ACLMessage.REFUSE);
                    reply.setContent("not-available");
                }
                myAgent.send(reply);
            } else {
                block();
            }
        }
    }  // End of inner class OfferRequestsServer
    private class PurchaseOrdersServer extends CyclicBehaviour {
        private static final long serialVersionUID = 1L;
        @Override
        public void action() {
            MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.ACCEPT_PROPOSAL);
            ACLMessage msg = myAgent.receive(mt);
            if (msg != null) {
                // ACCEPT_PROPOSAL Message received. Process it
                String title = msg.getContent();
                ACLMessage reply = msg.createReply();

                String price = catalogue.remove(title);
                if (price != null) {
                    reply.setPerformative(ACLMessage.INFORM);
                    System.out.println(title + " ordered from customers " + msg.getSender().getName());
                } else {
                                   reply.setPerformative(ACLMessage.FAILURE);
                    reply.setContent("not-available");
                }
                myAgent.send(reply);
            } else {
                block();
            }
        }
    }  // End of inner class OfferRequestsServer
}
