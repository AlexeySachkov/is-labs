package laba2_ceramicproductstore;

import jade.core.Agent;
import behaviours.PurchaseOrdersServer;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import java.time.LocalDateTime;

/**
 *
 * @author Евгений
 */

public class CeramicSellerAgent extends Agent{
    //Массив объектов = изделия, которыми вообще торгует продавец
    item[] productionManufactured = new item [5];
    
    //Для интриги, продавец продает все все изделия, который изготавливает.
    //Массив ниже хранит изделия, которые продаются сегодня (при запуске агента-продавца)
    item[] productionSaleToday = new item [4];
    
    //Ниже определяется индекс изделия, которое сегодня продаваться не ьбудет
    int minRandomItem = productionManufactured.length-productionManufactured.length; 
    int maxRandomItem = productionManufactured.length; 
    int randomMissingItem = (int) ((Math.random() * (maxRandomItem - minRandomItem)) + minRandomItem);
    
    int test = 123;
    
    
    protected void setup() {
        //Определяем, какими изделиями вообще торгует продавец
        productionManufactured[0] = new item("turk", 200);
        productionManufactured[1] = new item("standart", 250);
        productionManufactured[2] = new item("econom", 150);
        productionManufactured[3] = new item("evil", 350);
        productionManufactured[4] = new item("cloud", 550);

        System.out.println(LocalDateTime.now() + " — Приветствую в моей лавке! Сегодня продаются следующие изделия:");
        int ss = 0;
        for (int i=0; i<productionManufactured.length; i++){
            if(i!=randomMissingItem){
                productionSaleToday[ss] = productionManufactured[i];
                System.out.println("Изделие " + productionSaleToday[ss].name + " по цене " + productionSaleToday[ss].price + " p.");
                ss++;
            }
        }
        
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
        sd.setType("product-selling");
        sd.setName("JADE-tour-trading");
        dfd.addServices(sd);
        try {
            DFService.register(this, dfd);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }
        addBehaviour(new PurchaseOrdersServer(productionSaleToday));
     }
    
    //Прикрываем агента-продавца
    @Override
    protected void takeDown() {
         System.out.println("Продавец закрывает лавку.");
    }

}
