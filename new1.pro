predicates
nondeterm grades(string, string, real)
nondeterm mathematician(string)
nondeterm physicist(string)
nondeterm programmer(string)
nondeterm linguist(string)
nondeterm historian(string)
nondeterm lagging_behind(string)
nondeterm has_3(string)
nondeterm has_4(string)
nondeterm has_5(string)
clauses /* описываем факты, студент по определенному предмету имеет оценку */
grades(sidorov,programming,5).
grades(petrova,physics,5).
grades(smirnov,physics,2).
grades(chistov,programming,5).
grades(zelenov,programming,3.4).
grades(orlova,mathematics,4.3).
grades(rodionov,mathematics,3).
grades(zadornov,mathematics,5).
grades(sidorov,history,5).
grades(ivanova,history,5).
grades(zaharov,history,3).
grades(kuleshova,english,4.4).
grades(zagudaeva,english,5).
grades(kondrakova,english,4).
grades(kulalaev,english,3).
mathematician(X):-grades(X,mathematics,5). /* правило математик, этот у кого по математика твердая 5  */
physicist(X):-grades(X,physicics,5).        /* правило физик, этот у кого по физике твердая 5  */
programmer(X):-grades(X,programming,5).       /* правило программист, этот у кого по программированию твердая 5  */
historian(X):-grades(X,history,5).             /* правило историк, этот у кого по истории твердая 5  */
linguist(X):-grades(X,english,5).                  /* правило лингвист, этот у кого по английскоу твердая 5  */
lagging_behind(X):-grades(X,_,Y),Y<3.               /* правило двоечник, то у кого оценка <3  */
has_3(X):-grades(X,_,Y),Y>=3,Y<3.5.                     /* правило троечник, то у кого оценка >=3 и <3.5  */
has_4(X):-grades(X,_,Y),Y>=4,Y<4.5.                            /* правило четверочник, то у кого оценка >=4 и <4.5  */
has_5(X):-grades(X,_,Y),Y>=4.5.                                  /* правило отличник то у кого оценка >=4.5  */
Goal
grades(X,english,Y).  /* узнаем тех, кто изучает английский язык и их оценки */
historian(X).            /* узнаем тех, кто отличник по истории */
grades(X,programming,Y).  /* узнаем тех, кто изучает программирование их оценки */
grades(X,physics,Y).           /* узнаем тех, кто изучает физику их оценки */
has_3(X).  /* узнаем кто по различным предметам учится на 3 */
has_5(X)./* узнаем кто отличник, выведет список студентов по различным дисциплинам */
lagging_behind(X). /* узнаем кто двоечник */
has_4(X). /* узнаем у кого 4 по различным предметам */
grades(X,english,5). /* узнаем отличников по английскоу*/
grades(sidorov,history,Y). /* узнаем оценку Сидорова по истории */
