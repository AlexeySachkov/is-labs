package ru.nntu;


import java.util.HashMap;

// Информация о компаниях. Id, количество водителей.
public class Company {
    HashMap<Integer, Integer> countDrivers = new HashMap<>();

    Company(){
        countDrivers.put(1, 5);
        countDrivers.put(2, 5);
    }

    public int getCountCompany(){
        return countDrivers.keySet().size();
    }

    public int getCountDrivers(int companyId) {
        return countDrivers.get(companyId);
    }
}
