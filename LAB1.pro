%Задача:
%1)Найти данные по имени 
%2)найти старшего брата или сестру
%Исходные данные:
%(Имя,пол,год рождения,месяц рождения,Родитель1,Родитель2).
%Результат:
PREDICATES
nondeterm people(symbol, symbol, integer, integer, symbol, symbol)
nondeterm search_old_sister(symbol, symbol)
nondeterm search_old_brother(symbol, symbol)
CLAUSES
people(danil,m, 1995, 3, sveta, vasya).%f1.
people(nastya,w, 1991, 10, sveta, vasya).%f2.
people(sasha,m, 1996, 8, marina, sergey).%f3.
people(sahsa,m, 1988, 2, sveta, vasya).%f4.
search_old_brother(X,Y):-people(X,_,Year1,Month1,Par1,Par2), people(Y,m,Year2,Month2,Par1,Par2),Year1>Year2.
search_old_brother(X,Y):-people(X,_,Year1,Month1,Par1,Par2), people(Y,m,Year2,Month2,Par1,Par2),Year1=Year2,Month1>Month2.
search_old_sister(X,Y):-people(X,_,Year1,Month1,Par1,Par2), people(Y,w,Year2,Month2,Par1,Par2),Year1>Year2.
search_old_sister(X,Y):-people(X,_,Year1,Month1,Par1,Par2), people(Y,m,Year2,Month2,Par1,Par2),Year1=Year2,Month1>Month2.

GOAL
%people(danil,Pol,Year,Month,Par1,Par2).
%Pol=m, Year=1995, Month=3, Par1=sveta, Par2=vasya
%1 Solution

%people(Name,Pol,Year,Month,sveta,Par2).
%Name=danil, Pol=m, Year=1995, Month=3, Par2=vasya
%Name=nastya, Pol=w, Year=1991, Month=10, Par2=vasya
%Name=sahsa, Pol=m, Year=1988, Month=2, Par2=vasya
%3 Solutions

%search_old_sister(danil,Y).
%Y=nastya
%1 Solution

search_old_brother(danil,Y).
%Y=sahsa
%1 Solution