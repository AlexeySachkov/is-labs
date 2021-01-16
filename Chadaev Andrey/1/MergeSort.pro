DOMAINS
l = integer*

PREDICATES
nondeterm mergeSort(l,l)
nondeterm split(l,l,l)
nondeterm merge(l,l,l)

CLAUSES
mergeSort([],[]).
mergeSort([A],[A]).
mergeSort([A,B|R],S) :-
	split([A,B|R],L1,L2),
	mergeSort(L1,S1),
	mergeSort(L2,S2),
	merge(S1,S2,S).

split([],[],[]).
split([A],[A],[]).
split([A,B|R],[A|Ra],[B|Rb]) :-
	split(R,Ra,Rb).

merge(A,[],A).
merge([],B,B).
merge([A|Ra],[B|Rb],[A|M]) :-
	A =< B, merge(Ra,[B|Rb],M).
merge([A|Ra],[B|Rb],[B|M]) :-
	A > B, merge([A|Ra],Rb,M).

GOAL
mergeSort([6,4,1,11,8,12,0],R).