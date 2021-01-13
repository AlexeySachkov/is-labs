/*
Здесь описывается последовательность действия покупателя.
кейс 0:оповещаем продавца о названии товара, которое хочет купить покупатель
кейс 1: принимаем ответ. Если положительный, то идем дальше, если отрицательные - пакупатель уходит
кейс 2: информируем продавца о том, сколько изделий хотим купить
кейс 3: тут, в принципе, остался для доработки. Можно будет еще добавить рандомную генерацию кол-ва товара у продавца. Решил не удалять этот кейс
кейс 4: здесь уже кидаем запрос на скидку
кейс 5: как и в 1 кейсе, если PROPOSE - душевно благодарим за скидку, если REFUSE - огорчаемся, но покупаем и уходим.
*/
package behaviours;

import jade.core.AID;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
/**
 *
 * @author Евгений
 */
public class RequestPerformer extends Behaviour {
    private int step = 0;
    private final String nameOfAskingProduct;
    private final int countOfAskingProduct;
    String countOfAskingProductIsString; //Констыль для отправки кол-ва продукции в виде строки
    private AID[] sellerAgents;
    private MessageTemplate mt;
    private MessageTemplate mt2;
    private MessageTemplate mt3;
    int intermediatePrice; //чтоб узнать уйдет ли покупатель довольным, получив скидку, или расстроенным что не получил скидки
    int finishPrice;
    
    public RequestPerformer(AID[] sellerAgents, String nameOfAskingProduct, int countOfAskingProduct) {
        this.sellerAgents = sellerAgents;
        this.nameOfAskingProduct = nameOfAskingProduct;
        this.countOfAskingProduct = countOfAskingProduct;
    }
    
    @Override
    public void action() {
        switch (step) {
        case 0:
            ACLMessage cfp = new ACLMessage(ACLMessage.INFORM);//CFP
            //System.out.println("Лупа получил за Пупу, а ");
            cfp.addReceiver(sellerAgents[0]);//т.к. продавец у нас один, то отправляем именно ему
            cfp.setContent(nameOfAskingProduct); //кидаем продавцу что хочет купить покупатель
            cfp.setConversationId("product-trade");
            cfp.setReplyWith("cfp"+System.currentTimeMillis());
            myAgent.send(cfp);
            mt = MessageTemplate.and(MessageTemplate.MatchConversationId("product-trade"),
                    MessageTemplate.MatchInReplyTo(cfp.getReplyWith())); 
            System.out.println("К: Я хочу купить " + nameOfAskingProduct + ".");
       
        step++;
        break;
        
        case 1:
            ACLMessage reply = myAgent.receive(mt);
            if (reply != null){
                if(reply.getPerformative() == ACLMessage.PROPOSE){
                    step++;
                }
                if(reply.getPerformative() == ACLMessage.REFUSE){
                    System.out.println("К: Ладно, спасибо. До свидания!");
                    myAgent.doDelete();
                }
            } else {
                block();
            }
        break;
        
        case 2:
            ACLMessage orderCount = new ACLMessage(ACLMessage.CFP);//ACCEPT_PROPOSAL
                    orderCount.addReceiver(sellerAgents[0]);//Получатель все тот же один единственный продавец
                    countOfAskingProductIsString = String.valueOf(countOfAskingProduct);
                    orderCount.setContent(countOfAskingProductIsString);
                    orderCount.setConversationId("product-trade");
                    orderCount.setReplyWith("order"+System.currentTimeMillis());
                    myAgent.send(orderCount);
                    mt2 = MessageTemplate.and(MessageTemplate.MatchConversationId("product-trade"),
                            MessageTemplate.MatchInReplyTo(orderCount.getReplyWith()));
                    System.out.println("К: Мне нужно " + countOfAskingProductIsString + " ед.");
        step++;
        break;
        
        case 3:
            
            ACLMessage replyorderCount = myAgent.receive(mt2);
            if (replyorderCount != null){
                if(replyorderCount.getPerformative() == ACLMessage.PROPOSE){
                    intermediatePrice = (int) Integer.parseInt(replyorderCount.getContent());
                    //System.out.println("--- Покупатель получил промежуточную цену: " + intermediatePrice);
                    step++;
                }
            } else {
                block();
            }
            
        break;
        
        case 4:
            ACLMessage askForSale = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);//CFP
                    askForSale.addReceiver(sellerAgents[0]);//Получатель все тот же один единственный продавец
                    askForSale.setContent("А можно скидку?");
                    System.out.println("К: А можно скидку?");
                    askForSale.setConversationId("product-trade");
                    askForSale.setReplyWith("order"+System.currentTimeMillis());
                    myAgent.send(askForSale);
                    mt3 = MessageTemplate.and(MessageTemplate.MatchConversationId("product-trade"),
                            MessageTemplate.MatchInReplyTo(askForSale.getReplyWith()));
        step++;
        break;
        
        case 5:
            ACLMessage replyAskForSale = myAgent.receive(mt3);
            if (replyAskForSale != null){
                if(replyAskForSale.getPerformative() == ACLMessage.PROPOSE){
                    System.out.println("К: Больше спасибо!! Заберите мои деньгм и я пошел. Всего доброго!!");
                    step++;
                }
                if(replyAskForSale.getPerformative() == ACLMessage.REFUSE){
                    System.out.println("К: Ну и ладно, вот деньги. Спасибо, до свидания!");
                    step++;
                }
            } else {
                block();
            }
        break;
        }
        
        if (step == 6){
            myAgent.doDelete();
        }
        
    }
    
    @Override
    public boolean done() {
        return (step == 6);
    }
}
