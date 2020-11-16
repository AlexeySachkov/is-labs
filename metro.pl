% Несколько веток метро (минимум 1)
% У веток есть цвета (либо нумерация)
% У каждой ветки есть станции (минимум 2)
% Каждая станция соединена с минимум одной другой станцией
% Минимум одна станция для двух веток является пересадочной

% Задачи:
% 1) Возможность вывести все цвета (номера) веток. Возможность вывести количество веток.
% 2) Возможность вывести все станции одной ветки. Возможность вывести количество станций одной ветки.
% 3) Возможность вывести все пересадки одной ветки. Возможность вывести количество пересадок одной ветки.
% 4) Возможность вывести маршрут от станции А до станции Б в пределах одной ветки.
% 5) Возможность вывести маршрут от станции А до станции Б в пределах ДВУХ(может все) веток. Не обязательно самый короткий путь

% Выполнено:
% 1) findAllLines(), countLine().
% 2) findAllStations(X), countAllStations(X).
% 4-5) findRoute(X,Y).


line(
  red, 
  [someStation, gorkovskaya, moskovskaya, chkalovskaya, leninskaya, zarechnaya, 
  dvigatelRevolyutsii, proletarskaya, avtozavodskaya, komsomolskaya, kirovskaya,
  parkKultury]
  ).

line(
  blue, 
  [strelka, moskovskaya, kanavinskaya, burnakovskaya, burevestnik]
  ).

line(
  green, 
  [a, b, kanavinskaya,c, d, e]
  ).

% 1
countLine():-
  aggregate_all(count, line(_,_), Count),
  print(Count).
findAllLines():-findAllLines([]).
findAllLines(Lines):-
  line(Line,_),
  \+ member(Line,Lines),
  print(Line).

% 2
findAllStations(X):-
  line(X,Stations),
  print(Stations).
countAllStations(X):-  
  line(X,Stations),
  length(Stations,Len),
  print(Len).

% 4-5
findRoute(X,Y):-findRoute(X,Y,[],[]).  
% 4 
findRoute(X,Y,Lines,Output):-
      line(Line,Stations),
      \+ member(Line,Lines),
      member(X,Stations),
      member(Y,Stations),
      append(Output,[[X,Line,Y]],NewOutput),
      printRoute(NewOutput).
% 5
findRoute(X,Y,Lines,Output):-
      line(Line,Stations),
      \+ member(Line,Lines),
      member(X,Stations),
      member(Intermediate,Stations),
      X\=Intermediate,Intermediate\=Y,
      append(Output,[[X,Line,Intermediate]],NewOutput),
      findRoute(Intermediate,Y,[Line|Lines],NewOutput).
printRoute([]).
printRoute([H|T]):-
  format('You have to from ~w take ~w line go to ~w\n', H),
  length(T,Len),
  Len >0 -> 
  writeln('And after:'),
  print(T).