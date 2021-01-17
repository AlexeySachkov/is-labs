package ru.nntu;

import jade.core.Agent;

// Определяем тип агента и задаем ему определенное поведение.
public class CreateAgent extends Agent{

    @Override
    protected void setup() {
        String id = getAID().getLocalName();
        System.out.println("Создан агент: " + id);
        if (id.matches("Manager(.*)")){
            addBehaviour(new ManagerBehaviour(Integer.parseInt(id.split("_")[1])));
        }
        else if (id.matches("Driver(.*)")){
            addBehaviour(new TaxiBehaviour());
        }
        else {
            addBehaviour(new ClientBehaviour());
        }
    }
}
