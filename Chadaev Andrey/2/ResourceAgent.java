package base;

import jade.core.Agent;
import jade.core.behaviours.SimpleBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class ResourceAgent extends Agent {
    protected void setup() {
        addBehaviour(new SimpleBehaviour() {
            private boolean finished = false;
            public String DestinationPoint;

            @Override
            public void action() {
                System.out.println(getLocalName() + " is active");
                System.out.println(getLocalName() + " input destination point: ");
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
                try {
                    DestinationPoint = bufferedReader.readLine().toUpperCase();
                }
                catch (IOException e) {}

                MessageTemplate template1 = MessageTemplate.MatchPerformative(ACLMessage.INFORM);
                MessageTemplate template2 = MessageTemplate.MatchOntology("TestOntology");
                MessageTemplate template3 = MessageTemplate.and(template1, template2);

                ACLMessage message = blockingReceive(template3, 120000);

                if (message != null) {
                    System.out.println(getLocalName() + ": message from " + message.getSender().getLocalName() + " was received!");
                    if (DestinationPoint.equals(message.getContent().toUpperCase())) {
                        System.out.println(getLocalName() + ": order was accepted");
                    }
                    else {
                        System.out.println(getLocalName() + ": order was rejected");
                    }
                }
                else {
                    System.out.println(getLocalName() + ":empty message was received");
                }
                finished = true;
            }

            @Override
            public boolean done() {
                return finished;
            }
        });
    }
}
