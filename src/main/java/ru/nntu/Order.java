package ru.nntu;


// Информация о заказе.
public class Order {
    private int from;
    private int to;
    private int waitingTime;
    private String client;
    private String taxi;
    private int price;
    private int variables = 1;

    Order(int from, int to){
        setFrom(from);
        setTo(to);
    }

    Order(int from, int to, int waitingTime, String client, String taxi){
        setFrom(from);
        setTo(to);
        setWaitingTime(waitingTime);
        setClient(client);
        setTaxi(taxi);
    }

    public void setFrom(int from){
        this.from = from;
    }

    public void setTo(int to) {
        this.to = to;
    }

    public void setWaitingTime(int waitingTime){
        this.waitingTime = waitingTime;
    }

    public void setClient(String client) {
        this.client = client;
    }

    public void setTaxi(String taxi) {
        this.taxi = taxi;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public void setVariables(int inc){
        variables+=inc;
    }

    public int getFrom() {
        return from;
    }

    public int getTo() {
        return to;
    }

    public int getWaitingTime(){
        return waitingTime;
    }

    public String getClient(){
        return client;
    }

    public String getTaxi(){
        return taxi;
    }

    public int getPrice(){
        return price;
    }

    public int getVariables(){ return variables;}

}
