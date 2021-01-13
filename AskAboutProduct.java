package behaviours;

import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;

/**
 *
 * @author Евгений
 */
public class AskAboutProduct extends OneShotBehaviour{
    String nameOfAskingProduct;
    int countOfAskingProduct;
    private AID[] sellerAgent;
    
    public AskAboutProduct(Agent a, String name, int count) {
        this.nameOfAskingProduct = name;
        this.countOfAskingProduct = count;
    }
    
    @Override
    public void action() {
        DFAgentDescription template = new DFAgentDescription();
        ServiceDescription sd = new ServiceDescription();
        sd.setType("product-selling");
        template.addServices(sd);
        
        try {
            DFAgentDescription[] result = DFService.search(myAgent, template);
            sellerAgent = new AID[result.length];
            
            for (int i = 0; i < result.length; ++i) {
                sellerAgent[i] = result[i].getName();
            }
        } catch (FIPAException fe) {
            System.out.println("Что-то и где-то пошло не по плану!");
            fe.printStackTrace();
        }
        
        myAgent.addBehaviour(new RequestPerformer(sellerAgent, nameOfAskingProduct, countOfAskingProduct));
    }
    
}
