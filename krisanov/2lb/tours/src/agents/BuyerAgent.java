package agents;

import behaviours.CustomTicker;
import jade.core.Agent;

public class BuyerAgent extends Agent {

    protected void setup() {
        System.out.println("Buyer-agent "+getAID().getName()+" is ready.");

        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            String nameTour = (String) args[0];
            System.out.println("Target tour is "+ nameTour);

            addBehaviour(new CustomTicker(this, 15000, nameTour));
        } else {
            System.out.println("No target tour nameTour specified");
            doDelete();
        }
    }

    @Override
    protected void takeDown() {
        System.out.println("Buyer-agent "+getAID().getName()+" is terminating.");
    }

}