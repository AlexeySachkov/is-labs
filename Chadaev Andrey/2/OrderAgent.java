package base;

import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.SimpleBehaviour;
import jade.lang.acl.ACLMessage;

public class OrderAgent extends Agent {
    protected void setup() {
        addBehaviour(new SimpleBehaviour(this) {
          private boolean finished = false;
          public String DestinationPoint = "Bor";

            AID[] resources = {
                    new AID("Resource1@192.168.1.52:1099/JADE", AID.ISGUID),
                    new AID("Resource2@192.168.1.52:1099/JADE", AID.ISGUID),
                    new AID("Resource3@192.168.1.52:1099/JADE", AID.ISGUID),
                    new AID("Resource4@192.168.1.52:1099/JADE", AID.ISGUID)};

            @Override
            public void action() {
                System.out.println(getLocalName() + " is active");
                ACLMessage message = new ACLMessage(ACLMessage.INFORM);
                message.setOntology("TestOntology");
                message.setContent(DestinationPoint);

                for (AID resource : resources) {
                    message.addReceiver(resource);
                }
                send(message);
                finished = true;
            }

            @Override
            public boolean done()
            {
                return finished;
            }
        });
    }
}

