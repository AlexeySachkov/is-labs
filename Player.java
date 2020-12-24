import jade.core.Agent;
import jade.core.behaviours.*;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.*;
import java.util.Random;

public class Player extends Agent {
    protected String[][] list = {
            {
                    "Привет master !"
            },
            {
                    "В первом стаканчике !",
                    "Во втором стаканчике !",
                    "В третьем стаканчике !"
            },
            {
                    "Ура я выйграл !",
                    "Жаль я проиграл !"
            },
            {
                    "Пока master !"
            }
    };
    public int cash = 3;
    protected void setup() {
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
        sd.setType("kr");
        sd.setName("player");
        dfd.addServices(sd);
        final Agent agent = this;
        try {
            DFService.register(this, dfd);
            System.out.println(getLocalName() + " Пришёл играть... ");
        } catch (Exception e) {
            System.out.println(e);
        }
        addBehaviour(new CyclicBehaviour(this) {
            public void action() {
                ACLMessage msg = receive();
                if (msg!=null) {
                    System.out.println(" -> " + myAgent.getLocalName() + " принял сообщение " + " ''" +msg.getContent() + "'' ");
                    ACLMessage reply = msg.createReply();
                    reply.setPerformative( ACLMessage.INFORM );
                    Random r = new Random();
                    switch (msg.getContent()) {
                        case "Привет players !":
                            reply.setContent(list[0][0]);
                            break;
                        case "В кaком стаканчике шарик ?":
                            reply.setContent(list[1][r.nextInt(2)]);
                            break;
                        case "В каком стaканчике шарик ?":
                            reply.setContent(list[1][r.nextInt(2)]);
                            break;
                        case "В каком стакaнчике шарик ?":
                            reply.setContent(list[1][r.nextInt(2)]);
                            break;
                        case "В каком стаканчике шарик ?":
                            reply.setContent(list[1][r.nextInt(2)]);
                            break;
                        case "Верно !":
                            reply.setContent(list[2][0]);
                            cash++;
                            System.out.println(" ** " + getLocalName() + " Имеет на руках сумму равную " + cash);
                            break;
                        case "Не верно !":
                            reply.setContent(list[2][1]);
                            cash--;
                            System.out.println(" ** " + getLocalName() + " Имеет на руках сумму равную " + cash);
                            break;
                    }
                    send(reply);
                    System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +reply.getContent() + "'' ");
                    if (cash == 6) {
                        try {
                            DFService.deregister(agent);
                        }
                        catch (Exception e) {
                            System.out.println(e);
                        }
                        System.out.println(" ** " + getLocalName() + " ''Спасибо за хорушую игру! Всем пока...'' ");
                        doDelete();
                    }
                    if (cash == 0) {
                        try {
                            DFService.deregister(agent);
                        }
                        catch (Exception e) {
                            System.out.println(e);
                        }
                        System.out.println(" ** " + getLocalName() + " ''Увы у меня кончились деньги, немогу играть. Всем пока...'' ");
                        doDelete();
                    }
                }
            }
        });
    }
}
