% SWI-Prolog 8.2.2

% Several metro lines (at least 1)
% The lines have colors (or numbering)
% Each line has stations (minimum 2)
% Each station is connected to at least one other station
% At least one station for two lines is an interchange

% Tasks:
% 1) Possibility to display all colors (numbers) of lines. Possibility to display the number of lines.
% 2) Possibility to display all stations of one line out. Possibility to display the number of stations on one line.
% 3) Possibility to display all interchange of one line. Possibility to display the number of interchange of one line.
% 4) Possibility to display the route from station A to station within one line.
% 5) Possibility to display the route from station A to station B within TWO (maybe all) lines. Not necessarily the shortest path

% Done:
% 1) findAllLines(), countLine().
% 2) findAllStations(X), countAllStations(X).
% 4-5) findRoute(X,Y).

% Not done and not the fact that I will do it 3.))


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
  [a, b, kanavinskaya, c, d, e]
  ).

% 1
countLine():-
  aggregate_all(count, line(_,_), Count),
  print(Count).
findAllLines():-findAllLines([]).
findAllLines(Lines):-
  line(Line,_),
  \+ member(Line,Lines),
  writeln(Line),fail.

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
      member(Interchange,Stations),
      X\=Interchange,Interchange\=Y,
      append(Output,[[X,Line,Interchange]],NewOutput),
      findRoute(Interchange,Y,[Line|Lines],NewOutput).
printRoute([]).
printRoute([H|T]):-
  format('You have to from ~w take ~w line go to ~w\n', H),
  length(T,Len),
  Len >0 -> 
  writeln('And after:'),
  print(T).