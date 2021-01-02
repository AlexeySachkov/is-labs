%Страны мира
%База содержит знания о некоторых странах мира, такие как: название страны, ее площадь, население, официальный язык, валюта, континент расположения и горные массивы, которые находятся на территории страны
square(argentina, 2.7).
square(australia, 7.6).
square(brazil, 8.5).
square(canada, 10).
square(china, 9.6).
square(india, 3.3).
square(kazakhstan, 2.7).
square(russia, 17.1).
square(sudan, 2.5).
square(usa, 9.4).

population(argentina, 45.2).
population(australia, 25.2).
population(brazil, 207.3).
population(canada, 37.6).
population(china, 1404).
population(india, 2000).
population(kazakhstan, 18.8).
population(russia, 146.7).
population(sudan, 39.5).
population(usa, 328.2).

language(argentina, spanish).

language(australia, english).

language(brazil, portugal).

language(canada, english).
language(canada, french).

language(china, chinese).
language(china, mandarin).

language(india, hindi).
language(india, english).

language(kazakhstan, kazakh).
language(kazakhstan, russian).

language(russia, russian).

language(sudan, arabic).
language(sudan, english).

language(usa, english).

currency(argentina, ars).
currency(australia, aud).
currency(brazil, brl).
currency(canada, cad).
currency(china, cny).
currency(india, inr).
currency(kazakhstan, kzt).
currency(russia, rub).
currency(sudan, sdg).
currency(usa, usd).

geography(argentina, south_america, andes).
geography(australia, australia, great_dividing_range).
geography(brazil, south_america, brazilian_highlands).
geography(canada, north_america, appalachi).
geography(china, eurasia, tibetan_plateau).
geography(india, eurasia, himalayas).
geography(kazakhstan, eurasia, tien_shan).
geography(russia, eurasia, caucasus).
geography(sudan, africa, nuba).
geography(usa, north_america, appalachi).

%Запрос, который определяет, в какую страну можно поехать со знанием выбранного языка
what_language(Language) :- language(Country, Language), format('~w ~s country that you may go ~n', [Country, "is the"]), fail.

%Запрос, который определяет континент, в котором располагается введенная страна
continent(Country) :- geography(Country, Continent, Mountains), format('~w ~s continent where this country located ~n', [Continent, "is the"]), fail.

%Запрос, который выводит все страны, площадь которых больше 9 млн. км2
countries_with_square_9 :- square(Country, Square), Square>=9, format('~w ~s country with the square ', [Country, "is the"]), format('~w ~n',[Square]), fail, nl.

%Запрос, который выводит все страны, которые находятся в Евразии
eurasia :- geography(Country, Continent, Mountains), Continent='eurasia', write(Country), write('   '), fail, nl.

%Запрос, выводящий на экран все сведения о выбранной стране
information(Country) :- square(Country, Square), population(Country, Population), language(Country, Language), currency(Country, Currency), geography(Country, Continent, Mountains), format('~w ~s square ', [Country, "has"]), format('~w ~s which has population ', [Square, "mln km2, "]), format('~w ~s who speaks on ', [Population, "mln "]), format('~w ~s also have currency ', [Language, ". Country"]), format('~w ~s located in ', [Currency, ". Country"]), format('~w ~s you can see ', [Continent, " and"]), format('~w', [Mountains]).

%Запрос, который показывает населенность каждой страны
what_population :- population(Country, Population), format('~w ~s a population ', [Country, "has"]), format('~w ~s people ~n',[Population, "mln"]), fail.

%Запрос, проверяющий правильность ввода валюты страны
check_currency(Currency, Country) :- currency(Country, Currency).

%Запрос, который выводит все страны, в которых располагается определенный горный массив
mountains(Mountains) :- geography(Country, _, Mountains), format('~w ~s located in ',[Mountains, "is"]), format('~w ~n',[Country]), fail, nl.

/*
Вывод:
1-й:
	what_language(english).
		australia is the country that you may go 
		canada is the country that you may go 
		india is the country that you may go 
		sudan is the country that you may go 
		usa is the country that you may go 
2-й:
	?- continent(brazil).
		south_america is the continent where this country located 
3-й:
	?- countries_with_square_9.
		canada is the country with the square 10 
		china is the country with the square 9.5999999999999996 
		russia is the country with the square 17.100000000000001 
		usa is the country with the square 9.4000000000000004 
4-й:
	?- eurasia.
		china   india   kazakhstan   russia   
5-й:
	?- information(russia).
		russia has square 17.100000000000001 mln km2,  which has population 146.69999999999999 mln  who speaks on russian . Country also have currency rub . Country located in eurasia  and you can see caucasus
6-й:
?- what_population.
		argentina has a population 45.200000000000003 mln people 
		australia has a population 25.199999999999999 mln people 
		brazil has a population 207.30000000000001 mln people 
		canada has a population 37.600000000000001 mln people 
		china has a population 1404 mln people 
		india has a population 2000 mln people 
		kazakhstan has a population 18.800000000000001 mln people 
		russia has a population 146.69999999999999 mln people 
		sudan has a population 39.5 mln people 
		usa has a population 328.19999999999999 mln people
7-й:
	?- check_currency(usd, usa).
		yes
	?- check_currency(usd, sudan).
		no
8-й:
	?- mountains(appalachi).
		appalachi is located in canada 
		appalachi is located in usa
*/