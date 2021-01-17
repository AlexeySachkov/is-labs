package ru.nntu;

import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentController;
import jade.wrapper.ContainerController;

class Controller {
    String host = "localhost";
    String port = "10099";
    private static final int numberOfClients = 4;
    void initAgents() {

        // Создаем агентов-диспетчеров и таксистов.
        Runtime rt = Runtime.instance();

        for (int i = 1; i <= new Company().getCountCompany(); i++) {
            Profile p = new ProfileImpl();
            p.setParameter(Profile.MAIN_HOST, host);
            p.setParameter(Profile.MAIN_PORT, port);
            p.setParameter(Profile.GUI, "false");
            p.setParameter(Profile.CONTAINER_NAME, "Taxi_" + i);
            ContainerController cc;
            if (i == 1)
                cc = rt.createMainContainer(p);
            else
                cc = rt.createAgentContainer(p);
            try {
                AgentController agent = cc.createNewAgent("Manager_" + i, "ru.nntu.CreateAgent", null);
                agent.start();
                for (int j = 1; j <= new Company().getCountDrivers(i); j++) {
                    agent = cc.createNewAgent("Driver_" + i + "_" + j, "ru.nntu.CreateAgent", null);
                    agent.start();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        // Создаем клиентов такси.
        Profile p = new ProfileImpl();
        p.setParameter(Profile.MAIN_HOST, host);
        p.setParameter(Profile.MAIN_PORT, port);
        p.setParameter(Profile.GUI, "false");
        p.setParameter(Profile.CONTAINER_NAME, "Client");
        ContainerController cc = rt.createAgentContainer(p);
        for (int i = 1; i <= numberOfClients; i++){
            try {
                AgentController agent = cc.createNewAgent("Client_" + i, "ru.nntu.CreateAgent", null);
                agent.start();
                Thread.sleep(1000);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
