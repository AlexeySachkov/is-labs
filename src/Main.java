import jade.Boot;

public class Main {
    public static void main(String[] args) {

        String[] services = {"-giu", "-agents", "agentSellerFromOnline:SellerFromOnline"};
        Boot.main(services);
        String[] services2 = {"-giu", "-agents", "agentSellerFromShop:SellerFromShop"};
        Boot.main(services2);
        String[] services3 = {"-giu", "-agents", "agentBuyer:Buyer"};
        Boot.main(services3);
    }
}
