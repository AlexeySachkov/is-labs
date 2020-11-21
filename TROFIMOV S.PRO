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

CLAUSES
figura(1,white,c,1).%f1
figura(2,white,f,2).%f2
figura(3,white,d,4).%f3
figura(4,black,c,5).%f4
figura(5,black,e,5).%f5
figura(6,black,f,6).%f6
figura(7,black,a,7).%f7

koordinata(b,2).
koordinata(d,2).
koordinata(e,3).
koordinata(g,3).
koordinata(f,4).
koordinata(d,4).

hod_figury(Kod,Color,Sym,Int):-figura(Kod,Color,Sym,Int),perevod(Kod,Color,Sym,Int).%pr1
%Проверяем есть ли пешка для которой ищем возможность хода на доске если есть запускаем правило перевод.

perevod(Kod,Color,Sym,Int):-Sym="a",figura_per(Kod,Color,1,Int);Sym="b",figura_per(Kod,Color,2,Int);Sym="c",figura_per(Kod,Color,3,Int);Sym="d",figura_per(Kod,Color,4,Int);Sym="e",figura_per(Kod,Color,5,Int);Sym="f",figura_per(Kod,Color,6,Int);Sym="g",figura_per(Kod,Color,7,Int);Sym="h",figura_per(Kod,Color,8,Int).%pr2
%Переводим координаты фигуры от типа (symbol,integer) к типу (integer,integer)

figura_per(Kod,white,Sym,Int):- Sym=1,Int<8,Sym1=Sym+1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1);Sym>1,Sym<8,Int<8,Sym1=Sym+1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1);Sym>1,Sym<8,Int<8,Sym1=Sym-1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1);Sym=8,Int<8,Sym1=Sym+1,Int1=Int+1,figura_o(Kod,white,Sym1,Int1).%pr3
%Ищем возможность хода для белой фигуры,проверяем все варианты и условия 

figura_per(Kod,black,Sym,Int):- Sym=1,Int>1,Sym1=Sym+1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1);Sym>1,Sym<8,Int>1,Sym1=Sym+1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1);Sym>1,Sym<8,Int>1,Sym1=Sym-1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1);Sym=8,Int>1,Sym1=Sym+1,Int1=Int-1,figura_o(Kod,black,Sym1,Int1).%pr4
%Аналогично пред.правилу только для черной фигуры

figura_o(Kod,Color,Sym,Int):-Sym=1,koordinata(a,Int),not(figura(_,_,a,Int));Sym=2,koordinata(b,Int),not(figura(_,_,b,Int));Sym=3,koordinata(c,Int),not(figura(_,_,c,Int));Sym=4,koordinata(d,Int),not(figura(_,_,d,Int));Sym=5,koordinata(e,Int),not(figura(_,_,e,Int));Sym=6,koordinata(f,Int),not(figura(_,_,f,Int));Sym=7,koordinata(g,Int),not(figura(_,_,g,Int));Sym=8,koordinata(h,Int),not(figura(_,_,h,Int)).%pr5
%Возвращяем координаты к типу (symbol,integer) 

GOAL
hod_figury(1,white,c,1).
