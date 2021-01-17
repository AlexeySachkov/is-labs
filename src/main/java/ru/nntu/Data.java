package ru.nntu;

// Среднее время перемещения между районами города.
public class Data {
    private static final int [][] time = {
            {6, 15, 30, 20, 25, 33, 35, 37, 54},
            {15, 6, 15, 25, 13, 18, 35, 35, 40},
            {30, 15, 6, 30, 15, 10, 45, 30, 35},
            {20, 25, 30, 6, 20, 30, 15, 20, 35},
            {25, 13, 15, 20, 6, 10, 30, 22, 29},
            {33, 18, 10, 30, 10, 6, 35, 25, 25},
            {35, 35, 45, 15, 30, 35, 6, 13, 30},
            {37, 35, 30, 20, 22, 25, 13, 6, 17},
            {54, 40, 35, 35, 29, 25, 30, 17, 6}};

    private static final double randParam = 0.25;


    public static int getTime(int from, int to){
        int minTime = time[from][to] - (int)(randParam * time[from][to]);
        int maxTime = time[from][to] + (int)(randParam * time[from][to]);
        return (int)(Math.round(Math.random() * (maxTime-minTime)) + minTime);
    }

    public static int getCountAreas(){
        return time.length;
    }

}
