female(sarah).
female(lora).
female(lilly).
female(kate).
female(zara).
female(grace).
female(ann).
female(lexie).
female(bella).

male(alex).
male(roy).
male(jack).
male(jerry).
male(garry).
male(harald).
male(peter).
male(kyle).
male(sam).

sister(lilly,roy).
sister(lilly,jack).
sister(ann, mayalice).
sister(zara,jerry).
sister(lexie, bella).

brother(roy,lilly).
brother(roy,jack).
brother(jack,lilly).
brother(jack,roy).
brother(jerry,garry).
brother(jerry,zara).
brother(peter, harald).
brother(peter, kyle).
brother(kyle, sam).

parent_of(lora,sarah).
parent_of(sarah,alex).
parent_of(roy,alex).
parent_of(lilly,kate).
parent_of(harald,jerry).
parent_of(grace,jerry).

married(roy,sarah).
married(kyle, lexie).
married(sam, bella).

father(X,Y):- male(X),parent_of(X,Y).
mother(X,Y):- female(X),parent_of(X,Y).
son(X,Y) :- male(X),parent_of(Y,X).
daughter(X,Y) :- female(X),parent_of(Y,X).
child(X,Y) :- parent_of(Y,X).
grandfather(X,Y) :- male(X), parent_of(X,Z),parent_of(Z,Y).
sibling(X,Y) :- parent_of(Z,X),parent_of(Z,Y),not(X=Y).
sibling(X,Y) :- sister(X,Y).
sibling(X,Y) :- brother(X,Y).
aunt(X,Y) :- parent_of(Z,Y),sister(X,Z),female(X).
uncle(X,Y) :- male(X),brother(X,Z),parent_of(Z,Y).
cousin(X,Y) :- sibling(A,B),parent_of(A,X),parent_of(B,Y).
cousin(X,Y) :- brother(A,B),parent_of(A,X),parent_of(B,Y).
