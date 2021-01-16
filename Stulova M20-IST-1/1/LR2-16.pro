﻿
/*
Задание:
Дан список. Сформировать на его основе два списка.
Занести элементы из первой половины исходного списка в первый список,
а из второй половины – во второй. Убедиться, что центральные элементы
полученных списков равны.
*/

DOMAINS
	li = integer*
PREDICATES
	nondeterm sol(li,li,li)
	nondeterm prep(li,li,li)
	nondeterm div(li, li, li, li)
	nondeterm equal(li, li, li)
CLAUSES
	sol(L,L1,L2):- div(L,L1,L2,L), prep(L1,L2,L1). %пр1

	prep(L1,L2,[_|L3]):- equal(L1,L2,L3). %пр2

	div([H|T],[H|L1],L2,[_,_|L3]):- div(T,L1,L2,L3). %пр3

	div(T,[],T,[]):- !. %пр4

	equal([_|L1], [_|L2], [_,_|L3]):- equal(L1, L2, L3). %пр5

	equal([N|L1],[N|L2],[]):- !. %пр6
GOAL
sol([1,2,8,4,5,6,7,8,9,10],L1,L2). %з1
/*
Цель: Разделить список [1,2,8,4,5,6,7,8,9,10] на две части.
Решение: L1=[1,2,8,4,5], L2=[6,7,8,9,10]
*/