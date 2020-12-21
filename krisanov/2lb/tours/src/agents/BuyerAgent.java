package agents;

import behaviours.TickerBehaviourTest;
import jade.core.Agent;

public class BuyerAgent extends Agent {

    protected void setup() {
        System.out.println("Buyer-agent "+getAID().getName()+" is ready.");

        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            String nameTour = (String) args[0];
            System.out.println("Target book is "+ nameTour);

            addBehaviour(new TickerBehaviourTest(this, 15000, nameTour));
        } else {
            System.out.println("No target book nameTour specified");
            doDelete();
        }
    }

    @Override
    protected void takeDown() {
        System.out.println("Buyer-agent "+getAID().getName()+" is terminating.");
    }

}