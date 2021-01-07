predicates   /* программа имеет базу потенциальных призывников, база состоит из студентов которые в среднем обучаются 1-6 лет */
nondeterm vozrast(string, real)
nondeterm podlegit_pr(string)
nondeterm nepodlegit_pr(string)
nondeterm to_study(string)
nondeterm not_study(string)
clauses /*описываем факты, фамилия и возраст призывника */
vozrast(sidorov,18).
vozrast(petrov,20).
vozrast(fedorov,22).
vozrast(vinokurov,22).
vozrast(kulalaev,20).
vozrast(metelkov,34).
vozrast(smirnov,24).
to_study(smirnov)./* учится на данный момент*/
to_study(sidorov).
to_study(petrov).
to_study(fedorov).
not_study(vinokurov). /*не учится */
not_study(kulalaev).
not_study(metelkov).

podlegit_pr(X):-not_study(X),vozrast(X,Y),Y>=18,Y<=27. /* подлежат призыву, те чей возраст от 18 до 27 и они не обучаются.*/
nepodlegit_pr(X):-to_study(X),vozrast(X,Y),Y>=18,Y<=24. /* не подлежат призыву, те чей возраст от 18 до 24 и они обучаются.*/

Goal
podlegit_pr(smirnov). /* узнаем подлежит ли призыву смирнов*/
podlegit_pr(X). /* узнаем всех, кто подлежит призыву*/
nepodlegit_pr(X)./* узнаем всех, кто не подлежит призыву*/
to_study(X)./* узнаем всех, кто пока что обучается*/
not_study(X). /* узнаем всех, кто не обучается*/
to_study(fedorov)./* узнаем всех, учиться ли федоров сейчас (да/нет)*/
