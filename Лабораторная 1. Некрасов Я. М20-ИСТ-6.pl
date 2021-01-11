%% Задача: Даны 3 сосуда ёмкостью 12 литров, 8 литров, 5 литров. Необходимо путём переливания жидкости из сосуда в сосуд получить 6 литров, при том, что 1-ый сосуд полностью наполнен, а остальные - пусты.
write_list([]).
	write_list([X|L]) :- writeln(X), write_list(L).

	solution :- solve_pr([sosud(1, 12, 12), sosud(2, 8, 0), sosud(3, 5, 0)], sosud(_, _, 6), [], Steps),
		    write_list(Steps).

	replace(S, [S|L], X, [X|L]).
	replace(S, [T|L], X, [T|Ls]) :- replace(S, L, X, Ls).


	solve_pr(State, Goal, _, [State]) :- member(Goal, State).
	solve_pr(State, Goal, History, [State|Steps]) :-
				member(Sosud, State), member(Sosud2, State), not(Sosud = Sosud2),
				mv(Sosud, Sosud2, ResSosud, ResSosud2),
	                        replace(Sosud, State, ResSosud, State2),
                                replace(Sosud2, State2, ResSosud2, StateX),

			        not(member(StateX, [State|History])),
	                        solve_pr(StateX, Goal, [State|History], Steps).


	mv(sosud(Id1, Max1, Current), sosud(Id2, Max2, Current2),
		sosud(Id1, Max1, 0), sosud(Id2, Max2, Current3)) :-
			Current > 0, Current3 is Current2 + Current, Current3 =< Max2.

	mv(sosud(Id1, Max1, Current), sosud(Id2, Max2, Current2),
		sosud(Id1, Max1, Current3), sosud(Id2, Max2, Max2)) :-
			Current > 0, Current3 is Current2 + Current - Max2, Current3 >= 0.

%% ?- solution.
%% [sosud(1,12,12),sosud(2,8,0),sosud(3,5,0)]
%% [sosud(1,12,4),sosud(2,8,8),sosud(3,5,0)]
%% [sosud(1,12,0),sosud(2,8,8),sosud(3,5,4)]
%% [sosud(1,12,8),sosud(2,8,0),sosud(3,5,4)]
%% [sosud(1,12,8),sosud(2,8,4),sosud(3,5,0)]
%% [sosud(1,12,3),sosud(2,8,4),sosud(3,5,5)]
%% [sosud(1,12,3),sosud(2,8,8),sosud(3,5,1)]
%% [sosud(1,12,11),sosud(2,8,0),sosud(3,5,1)]
%% [sosud(1,12,11),sosud(2,8,1),sosud(3,5,0)]
%% [sosud(1,12,6),sosud(2,8,1),sosud(3,5,5)]
%% true 