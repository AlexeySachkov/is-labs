% Программа для поиска родственных связей между людьми.
% Дана база людей, информация о том, кто и кому приходится родителем, кто с кем находится в брачных узал (или уже нет).

% Пример вывода программы
% ?- niece(X, june).
% false.
% ?- niece(X, kelly).
%X = megan 
% у june нет ни одной племянницы, а у kelly - megan.

% ?- grandchild(rylan, X).
% X = john 
% У rylan есть внук john

% ?- sister_in_law(kelly, Y).
% Y = louise 
% После свадьбы у kelly появилась сестра louise.

% Facts
male(mark).
male(thomas).
male(harold).
male(gordon).
male(chuck).
male(david).
male(pierre).
male(john).
male(barry).
male(shane).
male(marc).
male(jeff).
male(corey).
male(tj).
male(ed).
male(rylan).
female(megan).
female(louise).
female(marielaure).
female(kelly).
female(cathy).
female(june).
female(esthel).
female(mado).
female(sally).
female(laura).
female(grace).
parents(rylan, shane, laura).
parents(thomas, mark, louise).
parents(marielaure, mark, louise).
parents(mark, harold, june).
parents(louise, gordon, esthel).
parents(kelly, harold, june).
parents(cathy, harold, june).
parents(mado, gordon, esthel).
parents(chuck, gordon, esthel).
parents(sally, gordon, esthel).
parents(david, pierre, mado).
parents(shane, john, kelly).
parents(marc, john, kelly).
parents(jeff, john, kelly).
parents(corey, barry, cathy).
parents(tj, barry, cathy).
parents(megan, barry, cathy).
married(mado, pierre).
married(cathy, barry).
married(louise, mark).
married(esthel, gordon).
married(shane, laura).
married(marc, grace).
ex_spouse(kelly, john).
ex_spouse(harold, june).
ex_spouse(june, ed).

% Rules
spouse(S1,S2) :- married(S1,S2) ; married(S2,S1) ; ex_spouse(S1,S2) ; ex_spouse(S2,S1).
child(C,P) :- parents(C,P,_) ; parents(C,_,P).
daughter(D,P) :- female(D) , child(D,P).
son(S,P) :- male(S) , child(S,P).
father(Fa,C) :- male(Fa), child(C,Fa).
mother(Mo,C) :- female(Mo), child(C,Mo).
grandparents(X,G1,G2) :- parents(X,P1,P2),
 ( (parents(P1,G1,G2) ; parents(P2,G1,G2)) 
 ; (parents(P1,G2,G1) ; parents(P2,G2,G1)) ).
grandchild(X,G) :- grandparents(X,G,_) ; grandparents(X,_,G).
sister(Ss,X) :- female(Ss), parents(Ss,P1,P2),
 ( parents(X,P1,P2) ; 
 parents(X,P2,P1) ), Ss\=X.
brother(Br,Y) :- male(Br), parents(Br,P1,P2),
 ( parents(Y,P1,P2) ;
  parents(Y,P2,P1) ), Br\=Y.
sibling(W,Z) :- brother(W,Z) ; sister(W,Z).
aunt(A,Nn) :- female(A), parents(Nn,P1,P2),
             ( sibling(A,P1) ; sibling(A,P2) ;
              (sibling(Q,P1) , spouse(A,Q)) ;
               (sibling(R,P2) , spouse(A,R)) ).
uncle(U,Nn) :- male(U), parents(Nn,P1,P2),
             ( sibling(U,P1) ; sibling(U,P2) ; (sibling(Q,P1) , spouse(U,Q)) ; (sibling(R,P2) , spouse(U,R)) ).
nephew(Np,X) :- male(Np), (uncle(X,Np) ; aunt(X,Np)).
niece(Nc,Y) :- female(Nc), (uncle(Y,Nc) ; aunt(Y,Nc)).
cousin(K,L) :- grandparents(K,GF,GM), grandparents(L,GF,GM), not(sibling(K,L)), K\=L.
brother_in_law(B,P) :- (brother(B,X),spouse(X,P)); (sister(Y,P),spouse(Y,B)).
sister_in_law(S,P) :- (sister(S,X),spouse(X,P)); (brother(Y,P),spouse(Y,S)).
