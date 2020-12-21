package agents;

import behaviours.OfferRequestsServer;
import behaviours.PurchaseOrdersServer;
import jade.core.Agent;
import jade.core.behaviours.*;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class SellerAgent extends Agent {

    private final Hashtable<String, Integer> tours = new Hashtable<>();

    protected void setup() {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        try {
            System.out.print("Print nameTour: ");
            String nameTour = reader.readLine();
            System.out.print("Print price: ");
            String str = reader.readLine();
            int price = Integer.parseInt(str);

            addTour(nameTour, price);
        } catch (IOException e) {
            e.printStackTrace();
        }

        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        ServiceDescription sd = new ServiceDescription();
        sd.setType("book-selling");
        sd.setName("JADE-book-trading");
        dfd.addServices(sd);
        try {
            DFService.register(this, dfd);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }

        addBehaviour(new OfferRequestsServer(tours));
        addBehaviour(new PurchaseOrdersServer(tours));
    }

    @Override
    protected void takeDown() {
        try {
            DFService.deregister(this);
        } catch (FIPAException fe) {
            fe.printStackTrace();
        }
        System.out.println("Seller-agent " + getAID().getName() + " is terminating.");
    }

    public void addTour(final String nameTour, final int price) {
        addBehaviour(new OneShotBehaviour() {
            public void action() {
                tours.put(nameTour, price);
                System.out.println(nameTour+" inserted into tours. Price = " + price);
            }
        });
    }

}