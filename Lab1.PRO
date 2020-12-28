DOMAINS
list = integer*

PREDICATES
nondeterm new(list,list,list)

CLAUSES
new([],[],[]). %fact 1
new([],X,X). %fact 2
new(X,[],X).%fact 2
new([X1|Tail1], [X2|Tail2],[X|Tail]):- X=X1+X2,new(Tail1,Tail2,Tail) .% rule 1

GOAL
new ([1,2], [1,2,3],List). %request1
%List=[2,4,3]
%1 Solution

new([1,2,3,4,5],[1,2,3],List).%request2
%List=[2,4,6,4,5]
%1 Sulution

