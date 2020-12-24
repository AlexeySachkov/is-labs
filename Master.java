import jade.core.Agent;
import jade.core.behaviours.*;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.*;
import java.util.Random;

public class Master extends Agent {
    protected String[][] list = {
            {
                    "Привет players !"
            },
            {
                    "В первом стаканчике !",
                    "Во втором стаканчике !",
                    "В третьем стаканчике !"
            },
            {
                    "В кaком стаканчике шарик ?",
                    "В каком стaканчике шарик ?",
                    "В каком стакaнчике шарик ?",
                    "В каком стаканчике шарик ?"
            },
            {
                    "Пока players !"
            }
    };
    DFAgentDescription[] result;
    public String secret = "";
    public int scrt = 0;
    public boolean flag = true;
    protected void setup() {
        final DFAgentDescription dfd = new DFAgentDescription();
//dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
//sd.setType("kr");
//sd.setName("master");
        dfd.addServices(sd);
        try {
            result = DFService.search(this, dfd);
            System.out.println(result.length + " в ожиданиие игры" );
        } catch (Exception e) {
            System.out.println(e);
        }
        final Agent agent = this;
        ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
        for(int i = 0; i<result.length; i++) {
            msg.addReceiver(result[i].getName());
            msg.setLanguage("English");
//Random r = new Random();
            msg.setContent(list[0][0]);
            send(msg);
            System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +msg.getContent() + "'' ");
        }
        addBehaviour(new TickerBehaviour(this, 5000) { // 5000 = 5 секундам
            protected void onTick() {
                try {
                    result = DFService.search(agent, dfd);
                    if (result.length>0) {
                    } else {
                        System.out.println(" ** " + getLocalName() + " ожидает новых игроков... ");
                    }
                } catch (Exception e) {
                    System.out.println(e);
                }
                ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
                for(int i = 0; i<result.length; i++) {
                    if (result.length != 0) {
                        msg.addReceiver(result[i].getName());
                        msg.setLanguage("English");
                        Random r = new Random();
                        if (flag == true) {
                            scrt = r.nextInt(4);
//System.out.println(scrt);
                        }
                        if (flag == false) {
                            scrt = r.nextInt(3);
                        }
                        if (scrt == 3) {
                            secret = (list[1][r.nextInt(3)]);
                            msg.setContent(list[2][scrt]);
                        } else {
                            secret = (list[1][scrt]);
                            msg.setContent(list[2][scrt]);
                        }
                        send(msg);
                        System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +msg.getContent() + "'' ");
                    } else {
                        System.out.println("Нет игроков, ожидаю...");
                    }
                }
            }
        });
        addBehaviour(new CyclicBehaviour(this) {
            public void action() {
                ACLMessage msg = receive();
                if (msg!=null) {
                    System.out.println(" -> " + getLocalName() + " принял сообщение" + " ''" +msg.getContent() + "'' ");
                    if (msg.getContent().equals(list[1][0])) {
                        if (msg.getContent().equals(secret)) {
                            ACLMessage reply = msg.createReply();
                            reply.setPerformative( ACLMessage.INFORM );
                            reply.setContent("Верно !");
                            send(reply);
                            System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +reply.getContent() + "'' ");
                            System.out.println(" ** " + getLocalName() + " отдает деньги выигравшему игроку ");
                        } else {
                            ACLMessage reply = msg.createReply();
                            reply.setPerformative( ACLMessage.INFORM );
                            reply.setContent("Не верно !");
                            send(reply);
                            System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +reply.getContent() + "'' ");
                            System.out.println(" ** " + getLocalName() + " забирает деньги проигравшего игрока ");
                        }
                    }
                    if (msg.getContent().equals(list[1][1])) {
                        if (msg.getContent().equals(secret)) {
                            ACLMessage reply = msg.createReply();
                            reply.setPerformative( ACLMessage.INFORM );
                            reply.setContent("Верно !");
                            send(reply);
                            System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +reply.getContent() + "'' ");
                            System.out.println(" ** " + getLocalName() + " отдает деньги выигравшему игроку ");
                        } else {
                            ACLMessage reply = msg.createReply();
                            reply.setPerformative( ACLMessage.INFORM );
                            reply.setContent("Не верно !");
                            send(reply);
                            System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +reply.getContent() + "'' ");
                            System.out.println(" ** " + getLocalName() + " забирает деньги проигравшего игрока ");
                        }
                    }
                    if (msg.getContent().equals(list[1][2])) {
                        if (msg.getContent().equals(secret)) {
                            ACLMessage reply = msg.createReply();
                            reply.setPerformative( ACLMessage.INFORM );
                            reply.setContent("Верно !");
                            send(reply);
                            System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +reply.getContent() + "'' ");
                            System.out.println(" ** " + getLocalName() + " отдает деньги выигравшему игроку ");
                        } else {
                            ACLMessage reply = msg.createReply();
                            reply.setPerformative( ACLMessage.INFORM );
                            reply.setContent("Не верно !");
                            send(reply);
                            System.out.println(" <- " + getLocalName() + " отправил сообщение " + " ''" +reply.getContent() + "'' ");
                            System.out.println(" ** " + getLocalName() + " забирает деньги проигравшего игрока ");
                        }
                    }
                }
            }
        });
    }
}
