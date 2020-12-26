/*
Определить отношение обращение(Список, ОбращенныйСписок), которое
обращает списки. Например, обращение([a,b,c,d],[d,c,b,a]).
*/

DOMAINS
список=symbol*

PREDICATES
nondeterm conc(список,список,список)
nondeterm reverse(список,список)

CLAUSES 
conc([],L,L). %факт1
conc([X|L1], L2, [X|L3]):-conc(L1,L2,L3). %правило1

reverse ([X],[X]).%факт2
reverse ([X|T],Z):-reverse(T,W),conc(W,[X],Z).%правило2

GOAL
reverse([a,b,c],F). %запрос1

/*
Редактирование запросов
1 reverse([a,b,c],F). F=["c","b","a"]
*/
