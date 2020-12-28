DOMAINS
list = integer*

PREDICATES
nondeterm new(list,list,list)

CLAUSES
new([],[],[]). %факт 1
new([],X,X). %факт 2
new(X,[],X).%факт 2
new([X1|Tail1], [X2|Tail2],[X|Tail]):- X=X1+X2,new(Tail1,Tail2,Tail) .% правило 1

GOAL
new ([1,2], [1,2,3],List). %запрос1
%List=[2,4,3]
%1 Solution

new([1,2,3,4,5],[1,2,3],List).%запрос2
%List=[2,4,6,4,5]
%1 Sulution

