package behaviours;

import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;

public class TickerBehaviourTest extends TickerBehaviour {

    String nameTour;
    private AID[] sellerAgents;

    public TickerBehaviourTest(Agent a, long period, String nameTour) {
        super(a, period);
        this.nameTour = nameTour;
    }

    @Override
    protected void onTick() {
        System.out.println("Check to buy " + nameTour);

        DFAgentDescription template = new DFAgentDescription();
        ServiceDescription sd = new ServiceDescription();
        sd.setType("book-selling");
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

        myAgent.addBehaviour(new RequestPerformer(sellerAgents, nameTour));
    }
}
