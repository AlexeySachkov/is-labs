% Проверка возможности хода пешкой.
% Исходные данные
%   •	коды и координаты всех фигур для которой анализируется возможность хода.
%   •	код ходящей фигуры;
% Выходные данные
% Ответ есть или нет возможность хода


%    _______________________
%  8 __|__|__|__|__|__|__|__|
%  7 b7|__|__|  |__|  |__|__|
%  6 __|__|  |__|  |b6|__|__|
%  5 __|  |b4|__|b5|  |__|__|
%  4 __|__|__|w3|__|__|  |__|
%  3 __|__|__|__|  |__|__|__|
%  2 __|__|__|__|__|w2|__|__|
%  1 __|__|w1|__|__|__|__|__|
%    a   b  c  d  e  f  g  h

PREDICATES 
nondeterm figura(integer, symbol, symbol, integer)
nondeterm perevod(integer, symbol, symbol, integer)
nondeterm figura_per(integer, symbol, integer, integer)
nondeterm hod_figury(integer, symbol, symbol, integer)
nondeterm figura_o(integer, symbol, integer, integer)
nondeterm koordinata(symbol,  integer)

PREDICATES 
nondeterm figura(integer, symbol, symbol, integer)
nondeterm perevod(integer, symbol, symbol, integer)
nondeterm figura_per(integer, symbol, integer, integer)
nondeterm hod_figury(integer)
nondeterm figura_o(integer, symbol, integer, integer)
nondeterm koordinata(symbol,  integer)

CLAUSES
figura(1,white,c,1).%f1
figura(2,white,f,2).%f2
figura(3,white,d,4).%f3
figura(4,black,c,5).%f4
figura(5,black,e,5).%f5
figura(6,black,f,6).%f6
figura(7,black,a,7).%f7

koordinata(Sym, NewInt) :- Sym="a",NewInt=1;Sym="b",NewInt=2;Sym="c",NewInt=3;Sym="d",NewInt=4;Sym="e",NewInt=5;Sym="f",NewInt=6;Sym="g",NewInt=7;Sym="h",NewInt=8.
%Правило для замены символьной координаты на цифровую. 
 
hod_figury(Kod):-figura(Kod,Color,Sym,Int),perevod(Kod,Color,Sym,Int).
%Проверяем есть ли фигура на доске если есть запускаем перевод.

perevod(Kod,Color,Sym,Int) :- koordinata(Sym, NewInt),figura_per(Kod,Color,NewInt,Int).
%Переводим символьную координату в цифровую и запускаем расчет хода.

figura_per(Kod,white,Sym,Int):- Sym=1,Int<8,Sym1=Sym+1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1);Sym>1,Sym<8,Int<8,Sym1=Sym+1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1);Sym>1,Sym<8,Int<8,Sym1=Sym-1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1);Sym=8,Int<8,Sym1=Sym+1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1).
%Нахождение возможности хода для белых фигур с учетом условий.

figura_per(Kod,black,Sym,Int):- Sym=1,Int>1,Sym1=Sym+1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1);Sym>1,Sym<8,Int>1,Sym1=Sym+1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1);Sym>1,Sym<8,Int>1,Sym1=Sym-1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1);Sym=8,Int>1,Sym1=Sym+1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1).
%Нахождение возможности хода для черных фигур с учетом условий.

figura_o(Kod,Color,NewInt,Int):- koordinata(Sym, NewInt),not(figura(_,_,Sym,Int)).
%Проводим обратную заменую цифровой координаты на символьную и проверяем свободно ли поле на которое собираемся ходить. 

GOAL
hod_figury(1).
