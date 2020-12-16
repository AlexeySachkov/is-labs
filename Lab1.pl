%Постановка задачи. Дана информация об автогонщиках: имя, название команды, номер и результаты нескольких гонок. 
%Определить: 
%1. Являются ли два гонщика представителями одной команды.
%2. По названию команды, найти всех ее пилотов.
%3. Посчитать количество очков гонщиков после проведенных этапов.
%4. Посчитать количество очков команд после проведенных этапов.

%Пилот, команда, номер.
driver('Lewis_Hamilton', 'Mercedes', 1).
driver('Valtteri_Bottas', 'Mercedes', 2).
driver('Sebastian_Vettel', 'Ferrari', 3).
driver('Charles_Leclerc', 'Ferrari', 4).
driver('Max_Verstappen', 'Red_Bull', 5).
driver('Alexander_Albon', 'Red_Bull', 6).
driver('Lance_Stroll', 'Racing_Point', 7).
driver('Sergio_Perez', 'Racing_Point', 8).
driver('Lando_Norris', 'McLaren', 9).
driver('Carlos_Sainz', 'McLaren', 10).

%Результаты гонки. Название трассы, номера спортсменов на финише.
race_result('Monza', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).
race_result('Spa', [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]).
race_result('Hokkenheim', [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]).

%Вывод на экран результатов поиска пилотов для указанной команды.
print_drivers_in_team(Team):- drivers_in_team(Team, Drivers), write(Team), write(":"), write(Drivers).
%Поиск пилотов для указанной команды.
drivers_in_team(Team, Drivers):- bagof([Driver, Number], driver(Driver, Team, Number), Drivers).

%Поиск представителей одной команды.
print_teammate(Driver):- teammate(Driver,  Driver_2), write(Driver_2).
teammate(Driver_1, Driver_2):- driver(Driver_1, Team_Name, Num_1), driver(Driver_2, Team_Name, Num_2), Num_1 \= Num_2.

%Подсчет очков для пилотов.
print_driver_points(Driver):- driver_points(Driver, Points), write(Points).
driver_points(Driver, Points):- bagof(Point, points(Driver, Point), Result), sum_list(Result, Points).
points(Driver, Points):- race_result(Track, Result), driver(Driver, _, Number),  index(Number, Result, Position), points_per_position(Position, Points).
%Сумма элементов списка.
sum_list([],0).
sum_list([H|T],Sum):- sum_list(T,Sum1), Sum is H+Sum1.
%Перевод финишной позиции в количество очков.
points_per_position(Position, Point):- Position=1 -> Point=25;
Position=2 -> Point=18;
Position=3 -> Point=15;
Position=4 -> Point=12;
Position=5 -> Point=10;
Position=6 -> Point=8;
Position=7 -> Point=6;
Position=8 -> Point=4;
Position=9 -> Point=2;
Position=10 -> Point=1;
Point=0.
%Нахождение порядкового номера элемента в списке.
index(_,[],-1).
index(X,[X|_],1):-!.
index(X,[_|T],L):- index(X,T,L1), L1 > -1, L is L1+1. 
%Подсчет очков для команд.
print_team_points(Team):- team_points(Team, Points), write('Points:'), write(Points).
team_points(Team, Points):- drivers_in_team(Team, Drivers),  nth0(0, Drivers, Tmp_Driver_1), nth0(1, Drivers, Tmp_Driver_2), nth0(0, Tmp_Driver_1, Driver_1), nth0(0, Tmp_Driver_2, Driver_2), driver_points(Driver_1, Points_1), driver_points(Driver_2, Points_2), Points is Points_1+Points_2.
