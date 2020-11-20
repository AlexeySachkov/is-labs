Domains 
number= integer
list= number*
Predicates
nondeterm  split ( List,List,List).
insert_sort(list,list)
insert(number,list,list)
asc_order(number,number)
nondeterm  unite ( List,List,List).
nondeterm program (List,List).
clauses
split ([],[],[]).%f1
split ([X],[X],[]).%f2
split ([X,Y|Tail1],[Y|Tail2],[X|Tail3]):-split(Tail1,Tail2,Tail3).%f1
insert_sort([],[]).%f3
insert_sort([X|Tail],Sorted_list) :- insert_sort(Tail,Sorted_Tail), write ("X = ", X, " Tail = ", Tail, " Sorted_Tail = ", Sorted_Tail), nl,  insert(X,Sorted_Tail,Sorted_list), write ("X = ", X, " Tail = ", Tail, " Sorted_list = ", Sorted_list), nl. %Rule3
insert(X,[Y|Sorted_list],[Y|Sorted_list1]) :- asc_order(X,Y), !, insert(X,Sorted_list,Sorted_list1).%Rule4
insert(X,Sorted_list,[X|Sorted_list]).%Rule5
asc_order(X,Y) :- X>Y.%Rule6
unite([],[],[]).%f4
unite ([X],[],[X]).%f5
unite([Y|Tail2],[X|Tail3],[X,Y|Tail4]):-unite(Tail2,Tail3,Tail4).%Rule7
program (List1,List5) :- split(List1,List2,List3),insert_sort(List2,List4), unite (List4,List3,List5).%Rule8
GOAL
%split ([1,6,3,8,5,4],List1,List2).%r1
%insert_sort([6,8,4],S).%r2
%unite ([4,6,8],[1,3,5],List).%r3
program ([1,4,3,8,5,6],List).%r4
