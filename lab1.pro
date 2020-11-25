Лабораторная 1. Елизаров Евгений М20-ист-1
Задание:
Для ненаправленного графа, описанного в задании 1, разработать программу, определяющую путь из заданного
начального узла в конечный за ограниченное количество переходов при запрете на повторное прохождение узлов.

Код:
DOMAINS
список=symbol*

PREDICATES
nondeterm путь(symbol,symbol,список,список,integer)
nondeterm путь1(symbol,список,список,список,integer)
nondeterm принадлежит(symbol,symbol,список)
nondeterm граф(список)
nondeterm смежные(symbol,symbol,список)

CLAUSES
граф([a,b,a,c,b,d,c,e,b,e,c,d]).
путь(A,Z,Граф,Путь,Номер) :- путь1(A,[Z],Граф,Путь,Номер).
путь1(A,[A|Путь1],_,Путь1,_).
путь1(A,[Z|Путь1],Граф,Путь,Номер) :- 	Номер > 0,смежные(Y,Z,Граф),
not (принадлежит(Y,_,Путь1)), not (принадлежит(_,Y,Путь1)),Номер1 = Номер - 1, путь1(A,[Y,Y,Z|Путь1],Граф,Путь,Номер1).
смежные(Y,Z,Граф) :- принадлежит(Y,Z,Граф); принадлежит(Z,Y,Граф).
принадлежит(Y,Z,[Y,Z|_]).
принадлежит(Y,Z,[_,_|Хвост]) :- принадлежит(Y,Z,Хвост).

GOAL
граф(Граф),путь(a,c,Граф,Путь,3).
/*
Граф=["a","b","a","c","b","d","c","e","b","e","c","d"], Путь=["a","c"]
Граф=["a","b","a","c","b","d","c","e","b","e","c","d"], Путь=["a","b","b","e","e","c"]
Граф=["a","b","a","c","b","d","c","e","b","e","c","d"], Путь=["a","b","b","d","d","c"]
3 Solutions
*/
