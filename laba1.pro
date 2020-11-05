% Шахматы. Варианты взятия фигуры пешкой.
% Исходные данные: 
%   •	коды всех фигур, их цвет и координаты (поле 1-8 на a-h);
%   •	код ходящей пешки;
% Результат:
%   •	код ходящей пешки;
%   •	цвет ходящей пешки;
%   •	новые координаты ходящей пешки (поле 1-8 на a-h);
%   •	код взятой фигуры;


PREDICATES
nondeterm фигура(symbol, symbol, symbol, symbol,integer)
nondeterm взятие(symbol, symbol, symbol, symbol, integer, symbol, symbol, integer)
nondeterm перевод(symbol, integer)
nondeterm координата (symbol, symbol, integer, integer, symbol)
CLAUSES 
фигура (пешка, п1, белая, d,4). %ф1
фигура (пешка, п2, белая, e,6). %ф2
фигура (пешка, п3, черная, c,6). %ф3
фигура (пешка, п4, чёрная, f,5). %ф4
фигура (конь, к1, белая, b,5). %ф5
фигура (конь, к2, черная, e,3). %ф6
фигура (ладья, л1, белая, g,4). %ф7
фигура (ладья, л2, черная, d,7). %ф8
фигура (ладья, л3, черная, f,7). %ф9
перевод(Координата1, Новая_к1):- Координата="a", Новая_к1=1; Координата1="b", Новая_к1=2; Координата1="c", Новая_к1=3; Координата1="d", Новая_к1=4; Координата1="e", Новая_к1=5; Координата1="f", Новая_к1=6; Координата1="g", Новая_к1=7; Координата1="h", Новая_к1=8. %правило2
координата(К1_ходящей, К1_взятой, К2_ходящей, К2_взятой, Цвет_ходящей):- Цвет_ходящей="белая", перевод(K1_ходящей,Новая_к1_ходящей), перевод(K1_взятой,Новая_к1_взятой), Разность=Новая_к1_взятой-Новая_к1_ходящей, abs(Разность)=1, К2_взятой=K2_ходящей+1; Цвет_ходящей="черная", перевод(K1_ходящей,Новая_к1_ходящей), перевод(K1_взятой,Новая_к1_взятой), Разность=Новая_к1_ходящей-Новая_к1_взятой, abs(Разность)=1, К2_взятой=K2_ходящей-1. %правило3
%взятие(пешка, п2, белая, e, 6, л2, d, 7):- фигура (пешка, п2, белая, e,6), фигура (ладья, л2, черная, d,7). %правило1
взятие (Наименование, Код_ходящей_фигуры, Цвет_ходящей_фигуры, Kоордината1, Kоордината2, Код_взятой_фигуры, Kоордината1_новая, Координата2_новая):-  фигура(Ниаменование,Код_ходящей_фигуры,Цвет_ходящей_фигуры,Kоордината1,Kоордината2), Наименование="пешка", фигура(_,Код_взятой,_,Координата1_новая,Координата2_новая), координата(Координата1, Координата1_новая, Координата2, Координата2_новая, Цвет_ходящей_фигуры).%правило4
GOAL
фигура (конь, к1, белая, b,5). %з1
взятие(пешка, п2, белая, e, 6, л2, d, 7).%з2
взятие (Наименование, п2, Цвет_ходящей_фигуры, Kоордината1, Kоордината2, Код_взятой_фигуры, Kоордината1_новая, Координата2_новая). %з3
