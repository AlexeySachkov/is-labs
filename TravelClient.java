#Программа заточена под продажу билетов.
#Агент TravelClient - клиент, который покупает самый выгодный для себя билет.
#Агент TravelProvider - туристические компании, которые дают несколько вариантов поездок в различные города в определенный день недели за определенную цену.
#Лучший вариант определяется посредством выбора самого дешевого доступного в ближайший день билета.

#Examples of output:
#    Positive scenario:
#    Moscow departure Monday put into the catalog at a cost = 10000
#    Moscow departure Monday put into the catalog at a cost = 9000
#    Moscow departure Tuesday put into the catalog at a cost = 8000
#    Nizhny Novgorod departure Saturday put into the catalog at a cost = 7000
#    Nizhny Novgorod departure Monday put into the catalog at a cost = 6000
#    Hello! Buyer-agent Client@127.0.0.1:10020/JADE is ready.
#    Target travel is Moscow
#    Trying to order Moscow
#    Found the following seller agents:
#    Provider@127.0.0.1:10020/JADE
#    Moscow ordered from customers Client@127.0.0.1:10020/JADE
#    Moscow successful order from agent Provider@127.0.0.1:10020/JADE
#    Cost = 8000 Day Tuesday
#    Travel-agent Client@127.0.0.1:10020/JADE is stopped.
#    Hello! Buyer-agent Client2@127.0.0.1:10020/JADE is ready.
#    Target travel is Nizhny Novgorod
#    Trying to order Nizhny Novgorod
#    Found the following seller agents:
#    Provider5@127.0.0.1:10020/JADE
#    Nizhny Novgorod ordered from customers Client2@127.0.0.1:10020/JADE
#    Nizhny Novgorod successful order from agent Provider5@127.0.0.1:10020/JADE
#    Cost = 6000 Day Monday
#    Travel-agent Client2@127.0.0.1:10020/JADE is stopped.
    
#    Negative scenario:
#    Hello! Buyer-agent Client5@127.0.0.1:10020/JADE is ready.
#    There are no specifications for the intended travel
#    Travel-agent Client5@127.0.0.1:10020/JADE is stopped.
        

package travelagent;
import com.sun.org.apache.xalan.internal.lib.ExsltStrings;
import jade.core.Agent;
import jade.core.AID;
import jade.core.behaviours.*;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import java.text.SimpleDateFormat;
import java.util.Calendar;
public class TravelClient extends Agent {
    private static final long serialVersionUID = 1L;
    private String targetTravelName;
    // The list of known seller agents
    private AID[] sellerAgents;
    // Put agent initializations here
    protected void setup() {
        // Print a welcome message
        System.out.println("Hello! Buyer-agent " + getAID().getName() + " is ready.");
        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            targetTravelName = (String) args[0];
            System.out.println("Target travel is " + targetTravelName);
            // Add a TickerBehaviour that schedules a request for seller agents every minute
            addBehaviour(new TickerBehaviour(this, 15000) {
                private static final long serialVersionUID = 1L;
                protected void onTick() {
                    System.out.println("Trying to order  " + targetTravelName);
                    // Update the list of seller agents
                    DFAgentDescription template = new DFAgentDescription();
                    ServiceDescription sd = new ServiceDescription();
                    sd.setType("travel-order");
                    template.addServices(sd);
                    try {
                        DFAgentDescription[] result = DFService.search(myAgent, template);
                        System.out.println("Found the following seller agents:");
                        sellerAgents = new AID[result.length];
                        for (int i = 0; i < result.length; ++i) {
                            sellerAgents[i] = result[i].getName();
                            System.out.println(sellerAgents[i].getName());
                        }
                    } catch (FIPAException fe) {
                        fe.printStackTrace();
                    }
                    // Perform the request
                    myAgent.addBehaviour(new RequestPerformer());
                }
            });
        } else {
            // Make the agent terminate
            System.out.println("There are no specifications for the intended travel");
            doDelete();
        }
    }
    // Put agent clean-up operations here
    protected void takeDown() {
        // Printout a dismissal message
        System.out.println("Travel-agent " + getAID().getName() + " is stopped.");
    }
    private class RequestPerformer extends Behaviour {
        private static final long serialVersionUID = 1L;
        private AID bestSeller; // The agent who provides the best offer 
        private int bestPrice;  // The best offered price
        private int bestDate;
        private AID bestSeller2; // The agent who provides the best offer 
        private int bestPrice2;  // The best offered price
        private int bestDate2;
        private int paramDaysTo;
        private int repliesCnt = 0; // The counter of replies from seller agents
        private MessageTemplate mt; // The template to receive replies
        private int step = 0;
        public void action() {
            String[] day = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
            SimpleDateFormat takeDay = new SimpleDateFormat("EEEE");
            Calendar cal = Calendar.getInstance();
            String aH = takeDay.format(cal.getTime());
            for (int a = 0; a < day.length; a++) {
                if (aH.equals(day[a])) {
                    paramDaysTo = a;
                }
            }
            switch (step) {
                case 0:
                    // Send the cfp to all sellers
                    ACLMessage cfp = new ACLMessage(ACLMessage.CFP);
                    for (int i = 0; i < sellerAgents.length; ++i) {
                        cfp.addReceiver(sellerAgents[i]);
                    }
                    cfp.setContent(targetTravelName);
                    cfp.setConversationId("travel-trade");
                    cfp.setReplyWith("cfp" + System.currentTimeMillis()); // Unique value

                    myAgent.send(cfp);
                    // Prepare the template to get proposals
                    mt = MessageTemplate.and(MessageTemplate.MatchConversationId("travel-trade"),
                            MessageTemplate.MatchInReplyTo(cfp.getReplyWith()));
                    step = 1;
                    break;
                case 1:
                    // Receive all proposals/refusals from seller agents
                    ACLMessage reply = myAgent.receive(mt);
                    if (reply != null) {
                        // Reply received
                        if (reply.getPerformative() == ACLMessage.PROPOSE) {
                            // This is an offer 
//                            int price = Integer.parseInt(reply.getContent());
                            String a = reply.getContent();
                            String b[] = a.split("/");
                            int price = Integer.parseInt(b[0]);
                            int daysto = Integer.parseInt(b[1]);
                            if (bestSeller == null || daysto < bestDate2) {
                                bestPrice2 = price;
                                bestSeller2 = reply.getSender();
                                bestDate2 = daysto;
                                if (daysto < bestDate2 && price < bestPrice2) {
                                    // This is the best offer at present
                                    bestPrice2 = price;
                                    bestSeller2 = reply.getSender();
                                    bestDate2 = daysto;
                                }
                            }
                            if (bestSeller == null || (daysto > paramDaysTo && daysto < bestDate)) {
                                bestPrice = price;
                                bestSeller = reply.getSender();
                                bestDate = daysto;
                                if (daysto < bestDate && price < bestPrice) {
                                    // This is the best offer at present
                                    bestPrice2 = price;
                                    bestSeller2 = reply.getSender();
                                    bestDate2 = daysto;
                                }
                            }
                        }
                        repliesCnt++;
                        if (repliesCnt >= sellerAgents.length) {
                            if (bestSeller == null) {
                                bestPrice = bestPrice2;
                                bestSeller = bestSeller2;
                                bestDate = bestDate2;
                            }
                            // We received all replies
                            step = 2;
                        }
                    } else {
                        block();
                    }
                    break;
                case 2:
                    // Send the purchase order to the seller that provided the best offer
                    ACLMessage order = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                    order.addReceiver(bestSeller);
                    order.setContent(targetTravelName);
                    order.setConversationId("travel-trade");
                    order.setReplyWith("order" + System.currentTimeMillis());
                    myAgent.send(order);
                    // Prepare the template to get the purchase order reply
                    mt = MessageTemplate.and(
                            MessageTemplate.MatchConversationId("travel-trade"),
                            MessageTemplate.MatchInReplyTo(order.getReplyWith()));
                    step = 3;
                    break;
                case 3:
                    // Receive the purchase order reply
                    reply = myAgent.receive(mt);
                    if (reply != null) {
                        // Purchase order reply received
                        if (reply.getPerformative() == ACLMessage.INFORM) {
                            // Purchase successful. We can terminate                       
                            System.out.println(targetTravelName
                                    + " successful order from agent "
                                    + reply.getSender().getName());
                            System.out.println("Cost = " + bestPrice + " Day " + day[bestDate]);
                            myAgent.doDelete();
                        } else {
                            System.out.println("Order failed: the destination has been ordered.");
                        }

                        step = 4;
                    } else {
                        block();
                    }
                    break;
            }
        }
        public boolean done() {
            if (step == 2 && bestSeller == null) {
                System.out.println("Attempt failed: " + targetTravelName + " not available for sale");
            }
            return ((step == 2 && bestSeller == null) || step == 4);
        }
    }  // End of inner class RequestPerformer
}
