female(sarah).%
female(lora).%
female(lilly).%
female(kate).%
female(zara).%
female(grace).%
female(ann).%
female(lexie).%
female(bella).%
female(veronica).%
female(ellis).%
female(beatrice).%
female(julia).%
female(sophia).%
female(dorothy).%
female(sandra).%
female(avis).%
female(nora).%

male(alex).%
male(roy).%
male(jack).%
male(jerry).%
male(garry).%
male(harald).%
male(peter).%
male(kyle).%
male(sam).%
male(damon).%
male(cannon).%
male(elliott).%
male(john).%
male(ethan).%
male(asher).%
male(robert).%
male(gabriel).%
male(thomas).%

%1st generation
parent_of(alex,jack).
parent_of(alex,roy).
parent_of(sarah,jack).
parent_of(alex,roy).
parent_of(sarah,jack).
%2nd generation
parent_of(roy,jerry).
parent_of(roy,garry).
parent_of(lora,jerry).
parent_of(lora,garry).
%3rd generation
parent_of(jerry,harald).
parent_of(kate,harald).
parent_of(garry,grace).
parent_of(garry,ann).
parent_of(garry,lexie).
parent_of(zara,grace).
parent_of(zara,ann).
parent_of(zara,lexie).
%4th generation
parent_of(harald,bella).
parent_of(peter,bella).
parent_of(kyle,lilly).
parent_of(kyle,sam).
parent_of(lexie,lilly).
parent_of(lexie,sam).
%5th generation
parent_of(damon,veronica).
parent_of(damon,ellis).
parent_of(damon,cannon).
parent_of(bella,veronica).
parent_of(bella,ellis).
parent_of(bella,cannon).
parent_of(sam,robert).
parent_of(dorothy,robert).
%6th generation
parent_of(elliott,john).
parent_of(elliott,ethan).
parent_of(ellis,john).
parent_of(ellis,ethan).
parent_of(cannon,gabriel).
parent_of(beatrice,gabriel).
parent_of(robert,nora).
parent_of(robert,thomas).
parent_of(sandra,nora).
parent_of(sandra,thomas).
%7th generation
parent_of(john,sophia).
parent_of(julia,sophia).
parent_of(ethan,asher).
parent_of(avis,asher).

father_of(X,Y):- male(X), parent_of(X,Y).
mother_of(X,Y):- female(X), parent_of(X,Y).
grandfather_of(X,Y):- male(X), parent_of(X,Z), parent_of(Z,Y).
grandmother_of(X,Y):- female(X), parent_of(X,Z), parent_of(Z,Y).
sister_of(X,Y):- female(X), father_of(F, Y), father_of(F,X),X \= Y.
sister_of(X,Y):- female(X), mother_of(M, Y), mother_of(M,X),X \= Y.
aunt_of(X,Y):- female(X), parent_of(Z,Y), sister_of(Z,X),!.
brother_of(X,Y):- male(X), father_of(F, Y), father_of(F,X),X \= Y.
brother_of(X,Y):- male(X), mother_of(M, Y), mother_of(M,X),X \= Y.
uncle_of(X,Y):- parent_of(Z,Y), brother_of(Z,X).
ancestor_of(X,Y):- parent_of(X,Y). ancestor_of(X,Y):- parent_of(X,Z), ancestor_of(Z,Y).
