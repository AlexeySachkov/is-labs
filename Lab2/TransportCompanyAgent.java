import jade.core.Agent;
import jade.core.behaviours.*;
import jade.lang.acl.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
public class TransportCompanyAgent extends Agent
{
    protected void setup()
    {
        addBehaviour(new SimpleBehaviour(this)
        {
            private boolean finished = false;
            public String DestinationPoint;
            public void action()
            {
                System.out.println(getLocalName() + " is active");
                System.out.println(getLocalName() + " input destination point:");
                BufferedReader buff = new BufferedReader(new InputStreamReader(System.in));
                try
                {
                    DestinationPoint = buff.readLine().toUpperCase();
                }
                catch (IOException E) {}
                MessageTemplate m1 = MessageTemplate.MatchPerformative(ACLMessage.INFORM);
                MessageTemplate m2 = MessageTemplate.MatchOntology("TestOntology");
                MessageTemplate m3 = MessageTemplate.and(m1, m2);
                ACLMessage msg = blockingReceive(m3, 120000);
                if (msg != null)
                {
                    System.out.println(getLocalName() + ": message from " + msg.getSender().getLocalName() + " was received");
                    if (DestinationPoint.equals(msg.getContent().toUpperCase()))
                        System.out.println(getLocalName() + ": order was accepted");
                         if (msg.getPerformative() == ACLMessage.INFORM) {
                            System.out.println(DestinationPoint+" successfully");
                            System.out.println("Transport Company = "+getLocalName())};
                    else
                        System.out.println(getLocalName() + ": order was rejected");
                }
                if (msg == null)
                {
                    System.out.println(getLocalName() + ": empty message was received");
                }
                finished = true;
            }
            public boolean done()
            {
                return finished;
            }
        });
    }
}
