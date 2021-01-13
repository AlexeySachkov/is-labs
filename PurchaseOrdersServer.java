package behaviours;

import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import laba2_ceramicproductstore.item;

/**
 *
 * @author Евгений
 */
public class PurchaseOrdersServer extends CyclicBehaviour{
    item[] productionSaleToday = new item [4];
    String targetProductName;//для поиска по массиву
    String targetProductCountIsStingForAccept;//Получать из сообщений можем только сторку. Эта переменная тчоб принять 2 сообщение
    int targetProductCount; //В эту переменную преобразуем значение из targetProductCountIsStingForAccept
    
    int finishPrice;//здесь сумма покупки
    int intermediatePrice; //промежуточная цена, до того, как покупатель попросит скидку
    
    int numberOfFoundedProduct = 100;//для костыльной работы
    
    
    public PurchaseOrdersServer(item[] productionSaleToday){
        this.productionSaleToday = productionSaleToday;
    }
    
    @Override
    public void action(){
        //MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.ACCEPT_PROPOSAL);
        MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.INFORM);//CFP
        ACLMessage msg = myAgent.receive(mt);

        if (msg != null){
            targetProductName = msg.getContent();
            System.out.println("---Продавец получил сообщение, ищем " + targetProductName);

            for(int i=0; i < productionSaleToday.length; i++ ){
               //System.out.println("---Попытка поиска №" + i);
                if (targetProductName.equals(productionSaleToday[i].name)){
                    //Название товара мы узнали. Нашли в массиве объектов который именно нужен и узнаем его цену,
                    //чтоб спросить покупателя сколько штук ему нужны для того, чтоб рассчитать итоговую сумму
                    targetProductCount = productionSaleToday[i].price;  
                    numberOfFoundedProduct = i;
                    //System.out.println("Нашел " + targetProductCount + ", сколько Вам нужно?");
                }
            }
            
            ACLMessage reply = msg.createReply();
            
            //Если запрашиваемое изделие продается (имеется в массиве продающихся сегодня изделий)
            //то заполняет ответ вопросом сколько штук хочет приобрести покупатель
            //Если запрашиваемое изделие не продается, то говорим покуптелю что он попутал
            
            //Здесь, вообще, индекс найденной продукции изначально равен 100. Если найден товар в магазине (отправленное название изделие
            //найденно в массиве проадваемых изделий), то продолжаем беседу и спрашгиваем сколько штук хочет купить покупатель
            //если запрашиваемое изделие не найдено, его индекс будет 100, тогда извиняемся что в магазине нет таких изделий
            if (numberOfFoundedProduct != 100){
                if (targetProductName.equals(productionSaleToday[numberOfFoundedProduct].name)){
                    reply.setPerformative(ACLMessage.PROPOSE);
                    //Отправляем покупателю в ответ цену изделия. Зачем?
                    System.out.println("П: Сколько единиц " + targetProductName + " вы хотите приобрести?");
                } 
            } 
            if (numberOfFoundedProduct == 100){
                reply.setPerformative(ACLMessage.REFUSE);
                System.out.println("П: Если я и изготавливаю такое изделие, то сегодня оно не продается. Приношу извинения");
            }
            myAgent.send(reply);
            

        }
        else{
            block();
        }
        
//Здесь ожидание второго сообщения от покупателя
        MessageTemplate mt2 = MessageTemplate.MatchPerformative(ACLMessage.CFP);
        ACLMessage msg2 = myAgent.receive(mt2);

        if (msg2 != null){
            targetProductCountIsStingForAccept = msg2.getContent();
            targetProductCount = Integer.parseInt(targetProductCountIsStingForAccept); //В эту переменную преобразуем значение из targetProductCountIsStingForAccept

            intermediatePrice = targetProductCount * productionSaleToday[numberOfFoundedProduct].price;
            System.out.println("---Продавец получил запрос на  " + targetProductCount + " ед. изделия " + targetProductName);
            System.out.println("П: Это есть. С вас " + targetProductCount + "*" + productionSaleToday[numberOfFoundedProduct].price + "=" + intermediatePrice + " р.");

            ACLMessage replyForCount = msg2.createReply();
            replyForCount.setPerformative(ACLMessage.PROPOSE);
            replyForCount.setContent(String.valueOf(intermediatePrice));
            myAgent.send(replyForCount); 
        }else{
            //System.out.println("Что-то и где-то пошло не по плану при отправке покупателю промежуточной цены :с");
            block();
        }        
//Конец обработки второго сообщения 

//Здесь ожидание третьего сообщения от покупателя
        MessageTemplate mt3 = MessageTemplate.MatchPerformative(ACLMessage.ACCEPT_PROPOSAL);
        ACLMessage msg3 = myAgent.receive(mt3);

        if (msg3 != null){
            System.out.println("---Продавец получил запрос на скидку.");
            ACLMessage replyForCount = msg3.createReply();
            //Ниже система скидок. В каждом из условий уже пуляется ответ на запрос скидки
            if (targetProductCount >= 100 ){
                finishPrice = (int) (intermediatePrice * 0.8);
                System.out.println("П: Хорошо, могу дать Вам скидку 20%. С вас " + finishPrice + " p.");
                replyForCount.setPerformative(ACLMessage.PROPOSE);
            } else if (targetProductCount >= 50 && targetProductCount < 100){
                finishPrice = (int) (intermediatePrice * 0.9);
                System.out.println("П: Хорошо, могу дать Вам скидку 10%. С вас " + finishPrice + " p.");
                replyForCount.setPerformative(ACLMessage.PROPOSE);
            } else if (targetProductCount >= 25 && targetProductCount < 50){
                finishPrice = (int) (intermediatePrice * 0.95);
                System.out.println("П: Хорошо, могу дать Вам скидку 5%. С вас " + finishPrice + " p.");
                replyForCount.setPerformative(ACLMessage.PROPOSE);
            }else if (targetProductCount < 25){
                finishPrice = intermediatePrice;
                System.out.println("П: К сожалению, не могу дать Вам скиндку." + finishPrice);
                replyForCount.setPerformative(ACLMessage.REFUSE);
            }
//Передадим конечную цену продавцу, так, пусть будет
            replyForCount.setContent(String.valueOf(finishPrice));
            myAgent.send(replyForCount); 
        }else{
            //System.out.println("Что-то и где-то пошло не по плану при отправке покупателю цены со скидкой :с");
            block();
        }        
//Конец обработки третьего сообщения 
    }
}
