import jade.content.OntoAID;
import jade.core.Agent;
import jade.core.*;
import jade.core.behaviours.*;
import jade.lang.acl.*;
import jade.core.AID;
public class ClientAgent extends Agent
{
    protected void setup()
    {
        addBehaviour (new SimpleBehaviour(this)
        {
            private boolean finished = false;
            public String DestinationPoint = "Moscow";
            AID[] companies = {new AID("TC1@syusin:1099/JADE", true),
                    new AID("TC2@syusin:1099/JADE", true),
                    new AID("TC3@syusin:1099/JADE", true),
                    new AID("TC4@syusin:1099/JADE", true),
                    new AID("TC5@syusin:1099/JADE", true)};

            public void action()
            {
                System.out.println(getLocalName() + " is active");
                ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
                msg.setOntology("TestOntology");
                msg.setContent(DestinationPoint);
                for (int i=0; i < 4; i++)
                    msg.addReceiver(companies[i]);
                send(msg);
                finished = true;
            }
            public boolean done()
            {
                return finished;
            }
        });
    }
}





