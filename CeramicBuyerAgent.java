package laba2_ceramicproductstore;

import behaviours.AskAboutProduct;
import jade.core.Agent;
import java.time.LocalDateTime;

/**
 *
 * @author Евгений
 */
public class CeramicBuyerAgent extends Agent {
    private String productNameToBuy;
    private int productCountToBuy;
    private String crutch;
    
    
    @Override
    protected void setup() {
        
        //Выводим сообщение при создании агента-покупателя
        System.out.println("\n" + LocalDateTime.now() + " — Покупатель с именем '" + getAID().getName() + "' приходит в магазин.");
        
        //Ниже получаем аргументы (они вводятся при добавлении агента), выводит сообщение и тригерим событие
        Object[] products = getArguments();
        if (products != null && products.length > 0) {
            productNameToBuy = (String) products[0];
            crutch = (String) products[1];
            productCountToBuy = Integer.parseInt(crutch);
            //АРГУМЕНТЫ ПЕРЕДАЮТСЯ ЧЕРЕЗ ЗАПЯТУЮ!!!
            //System.out.println("Я хочу купить " + productNameToBuy + ", мне нужно " + productCountToBuy + " ед.");

            addBehaviour(new AskAboutProduct(this, productNameToBuy, productCountToBuy));
        }
        
        else {
            // Make the agent terminate immediately
            System.out.println("Случилась что-то непредвиденное и покупатель выбежал из магазина :с");
            doDelete();
        }
        
        
    }
    
    @Override
    protected void takeDown(){
        System.out.println(LocalDateTime.now() + " — Покупатель с именем '" + getAID().getName() + "' приходит покидает магазин.");
    }
    
}
