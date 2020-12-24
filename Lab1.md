# Поиск вакансий и сотрудников

% есть база со скилами,вакансиями и статусом(уровнем соискателя)

```
skill(python).
skill(sql).
skill(js).
skill(english).
skill(excel).

vacancy(ds).
vacancy(marketolog).
vacancy(tester).

status(student).
status(junior).
status(middle).
status(senior).
```
% требования к соискателю и возможные ограничения для конкретных вакансий:
```
req(ds,Y,Z):-skill(Y),status(Z),(Y=python;Y=sql),not(Z=student;Z=junior).
req(marketolog,Y,Z):-skill(Y),status(Z),(Y=excel;Y=english).
req(tester,Y,Z):-skill(Y),status(Z),(Y=python,Y=sql),(Z=student;Z=junior).
```
% "рабочая" вакансия или объявление включает в себя название должности, навыки и требуемый уровень
```
work(V,C,D):-vacancy(V),skill(C),status(D),req(V,C,D).
```
% у соискателей также есть ряд своих признаков:
```
person(peter,Y,Z):-skill(Y),status(Z),(Y=python;Y=sql),(Z=middle).
person(mary,Y,Z):-skill(Y),status(Z),(Y=excel;Y=sql;Y=english),(Z=student).
person(kira,Y,Z):-skill(Y),status(Z),(Y=python;Y=sql;Y=english),(Z=junior).
```
% и сопоставляем работу и человека:
```
workman(N,V,C,D):-work(V,C,D),person(N,C,D).
```

% полный код
```
vacancy(ds).
vacancy(marketolog).
vacancy(tester).
skill(python).
skill(sql).
skill(js).
skill(english).
skill(excel).
status(student).
status(junior).
status(middle).
status(senior).

req(ds,Y,Z):-skill(Y),status(Z),(Y=python;Y=sql),not(Z=student;Z=junior).
req(marketolog,Y,Z):-skill(Y),status(Z),(Y=excel;Y=english).
req(tester,Y,Z):-skill(Y),status(Z),(Y=python,Y=sql),(Z=student;Z=junior).

work(V,C,D):-vacancy(V),skill(C),status(D),req(V,C,D).

person(peter,Y,Z):-skill(Y),status(Z),(Y=python;Y=sql),(Z=middle).
person(mary,Y,Z):-skill(Y),status(Z),(Y=excel;Y=sql;Y=english),(Z=student).
person(kira,Y,Z):-skill(Y),status(Z),(Y=python;Y=sql;Y=english),(Z=junior).

workman(N,V,C,D):-work(V,C,D),person(N,C,D).
```
% запросы:
```
?- workman(N,V,Y,Z). %и его вариации, можно искать подходящую вакансию по имени, статусу или скиллу
%следующие запросы выводят имена подходящих для конкретных профессий людей, их скиллы и статус
?-workman(N,ds,Y,Z).
/*вывод:
N = peter,
Y = python,
Z = middle ;
N = peter,
Y = sql,
Z = middle ;
false.*/
?-workman(N,marketolog,Y,Z).
?-workman(N,tester,Y,Z).
%следующие запросы выводят подходящие вакансии для конкретных людей
?-workman(peter,V,Y,Z).
/*вывод:
V = ds,
Y = python,
Z = middle ;
V = ds,
Y = sql,
Z = middle ;
false.*/
?-workman(mary,V,Y,Z).
?-workman(kira,V,Y,Z).
%следующие запросы выводят вакансии и людей по скиллу
?-workman(N,V,sql,Z).
/*вывод:
N = peter,
V = ds,
Z = middle ;
false.*/
%следующие запросы выводят вакансии и людей по скиллу и статусу
?-workman(N,V,sql,junior).
/*...*/
?- person(peter,Y,Z). %данные по человеку
/*вывод:
Y = python,
Z = middle ;
Y = sql,
Z = middle ;
false.*/
?-person(N,python,Z). %узнаем кто знает питон и на каком уровне
/*вывод:
N = peter,
Z = middle ;
N = kira,
Z = junior ;
false.*/
?-person(N,Y,middle). %узнаем у кого такой уровень и какие навыки он имеет
?-person(N,sql,middle).%ищем человека с таким скилом и уровнем, если его нет, выведет false
/*вывод:
N = peter ;
false.*/
?- work(V,C,D). %вакансии и их требования по скилам и статусу
?- work(ds,C,D). %требования по скилам и статусу для вакансии ds
?- work(V,sql,D). %для каких вакансий требуется этот навык и какой уровень знания должен быть
/*вывод:
V = ds,
D = middle ;
V = ds,
D = senior ;
false.*/
?- work(V,C,junior). %на какие позиции берут juniors и какие скилы там нужны
/*можно комбинировать, уточнять две переменные и искать по третьей*/
?-work(V,sql,junior).%есть ли позиции для junior с навыком sql
/*вывод:
false.*/
?-req(V,Y,Z). %выведет все рекомендации для всех вакансий
?-req(ds,Y,Z). %можем узнать требования конкретной вакансии
?-req(V,sql,Z). %можем узнать для какой вакансии нужен sql
?-req(V,Y,student). %какие навыки нужны и вакансии подходят студентам
/*вывод:
V = marketolog,
Y = english ;
V = marketolog,
Y = excel ;
false.*/
/*также можно комбинировать, уточнять две переменные и искать по третьей*/
/*...*/
%еще можем просто обращаться к базе и узнавать какие в ней сейчас есть вакансии, скилы, статусы - увидим список данных
?-vacancy(X).
/*вывод:
X = ds ;
X = marketolog ;
X = tester.*/
?-skill(X).
?-status(X).
```
