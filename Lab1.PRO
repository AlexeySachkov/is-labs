DOMAINS
list = integer*

PREDICATES
nondeterm new(list,list,list)

CLAUSES
new([],[],[]). %Факт 1
new([],X,X). %Факт2
new(X,[],X).%Факт3
new([X1|Tail1], [X2|Tail2],[X|Tail]):- X=X1+X2,new(Tail1,Tail2,Tail) .%правило1

GOAL
new ([1,2],[1,2,3],List). %запрос1
%new([1,2,3,4,5],[1,2,3],List).%запрос2

