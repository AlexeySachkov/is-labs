%Задание :Дан список [1,6,3,8,5,4]. Расположить элементы на четных местах в порядке возрастания.
Domains 
number= integer 
list= number*
Predicates
nondeterm  split ( List,List,List). %Разделяет первоначальный список на два списка. List- исходный список.
%List- список с элементами на четных местах. List - список с элементами на нечестных местах. 
insert_sort(list,list) %  внутренняя функция сортировки списка в порядке возрастания. 
%Она сортирует список с элементами на четных местах и получает на выходе отсортированный список в порядке возрастания.
insert(number,list,list)
asc_order(number,number)
nondeterm  unite ( List,List,List). % объединяет список с элементами на нечетных местах и отсортированный во возрастанию список.
nondeterm program (List,List).% выводит конечный результат программы.
clauses
split ([],[],[]).%f1
split ([X],[X],[]).%f2
split ([X,Y|Tail1],[Y|Tail2],[X|Tail3]):-split(Tail1,Tail2,Tail3).%f1
insert_sort([],[]).%f3
insert_sort([X|Tail],Sorted_list) :- insert_sort(Tail,Sorted_Tail), write ("X = ", X, " Tail = ", Tail, " Sorted_Tail = ", Sorted_Tail), nl,  insert(X,Sorted_Tail,Sorted_list), write ("X = ", X, " Tail = ", Tail, " Sorted_list = ", Sorted_list), nl. %Rule3
% Устранение элементов списка начинается с головы и осуществлять рекурсивно. Мы пошагово  заносим каждый элемент первого списка( список с элементами на четных местах)  в стек .
%В результате первый список  становится нулевым . Также происходит обновление второго списка
insert(X,[Y|Sorted_list],[Y|Sorted_list1]) :- asc_order(X,Y), !, insert(X,Sorted_list,Sorted_list1).%Rule4
% Переменной X  присваивается первое взятое из стека значение 8 ,а правило insert( 8,[],[8]). Затем происходит возврат на 1 круг  рекурсии insert_sort  и из стека извелекается.
% А значит и правило упорядочивания asc_order(X,Y) :- X>Y.
% Переменная X=4 ,Y=8 ,  правило :asc_orde(4,8):- 4>8 ( неуспешно)
% При помощи insert(X,Sorted_list,Sorted_list1)  вставляем 4  в выходной список слева от 8: insert(4,[8],[4,8]).
insert(X,Sorted_list,[X|Sorted_list]).%Rule5
%Происходит возрат insert_sort,  теперь : insert_sort([4,8],[4,8]). На следущем круге рекурсии происходит вставка элемента из стека 6.
%В начале работы на этом круге правило insert  имеет вид (6,[4,8],_]. 
%Сравниваются 6 и 4 asc_order(6,4):-6>4( успешно) , но 4 убирается в стек, insert вызывается рекурсивно еще раз ,но с хвостом списка [8] insert (6,[8],-) , 
% asc_order(6,8):- 6>8 (неуспешно) , то испытывается ( второй вариант ) insert (успешно).
%мы возвращаемся на предыдущие круги рекурсии сначала insert,  а потом insert_sort 6 в выходной список между 4,8. Insert (6,[4,8],[4,6,8], insert_sort([6,8,4],[4,6,8]).
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
% OUTPUT:
%X = 6 Tail = [] Sorted_Tail = []
%X = 6 Tail = [] Sorted_list = [6]
% X = 8 Tail = [6] Sorted_Tail = [6]
% X = 8 Tail = [6] Sorted_list = [6,8]
% X = 4 Tail = [8,6] Sorted_Tail = [6,8]
% X = 4 Tail = [8,6] Sorted_listl = [4,6,8]
% List = [1,4,3,6,5,8]
% 1 Solution
