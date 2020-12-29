euro_pair(spain, italy).
euro_pair(spain, france).
euro_pair(spain, germany).
euro_pair(spain, portugal).
euro_pair(germany, france).
euro_pair(germany, italy).
euro_pair(germany, portugal).
euro_pair(france, italy).
euro_pair(france, portugal).
euro_pair(italy, portugal).

capital(france, paris).
capital(germany, berlin).
capital(italy, roma).
capital(spain, madrid).
capital(portugal, lisboa).

border(spain, france).
border(germany, france).
border(france, italy).
border(spain, portugal).

color(spain,red,yellow,red).
color(germany,black,red,gold).
color(france,blue,white,red).
color(italy,green,white,red).
color(portugal,green,red,yellow).

nat_money(spain, esp).
nat_money(italy, itl).
nat_money(france, frf).
nat_money(germany, dem).
nat_money(portugal, pte).

water_border(spain, atlantic_ocean).
water_border(italy, mediterranean_sea).
water_border(france, atlantic_ocean).
water_border(germany, north_sea).
water_border(portugal, atlantic_ocean).

population(spain,47).
population(italy,60).
population(france,67).
population(germany,83).
population(portugal,10).

area(spain,505.990).
area(italy,301.338).
area(france,643.801).
area(germany,357.386).
area(portugal,92.212).

find_non_border_pair :- euro_pair(X,Y), \+ (border(X,Y)), format('~w ~s The ', [X, " no border with"]), format('~w ~n', [Y]), fail,nl.
find_border_pair :- border(X,Y), format('~w ~s The ', [X, " border with"]), format('~w ~n', [Y]), fail,nl.
find_capital :- capital(X,Y), format('~w ~s capital of ', [Y, "is the"]), format('~w ~n', [X]), fail, nl.
find_bord_cap :- border(X,Y), capital(X,Z), capital(X,Z), format('~w ~s the capital of ', [Z, " is"]), format('~w ~s of ', [X , " and"]),format('~w ~s capital is ', [Y, "the"]), format('~w ~n', [Z]), fail, nl.
find_water :- water_border(X,Y), format('~w ~s the ', [X, " border with"]), format('~w ~n', [Y]), fail, nl.
find_pop :- population(X,Y), format('~w ~s a population ', [X, "has"]), format('~w ~s ~n',[Y, " million"]), fail, nl.
find_area :- area(X,Y), format('~w ~s country with the area ', [X, "is the"]), format('~w ~s ~n',[Y, " thousand"]), fail, nl.
find_money :- nat_money(X,Y), format('~w ~s the ', [X, " have"]), format('~w ~n', [Y]), fail, nl.
find_color(X) :- color(X,B,N,M), format('~w ~s the color on flag ', [X, " has"]), format('~w ~s', [B , ", "]),format('~w ~s', [N, " and "]), format('~w ~s ~n', [M]).
find_info(X) :- area(X,Y), population(X,Z), water_border(X,R), nat_money(X,E), color(X,B,N,M), capital(X,T), format('~w ~s area ', [X, "has"]), format('~w ~s which has population ', [Y, " km2, "]), format('~w ~s has border with ', [Z, "mln "]), format('~w ~s also have national money ', [R, ". Country"]), format('~w ~s has color on flag ', [E, ". Country"]), format('~w ~s', [B,", "]), format('~w ~s', [N, " and "]), format('~w ~s', [M, ". "]), format('~w ~s capital of ', [T, "is the"]), format('~w ~n', [X]), fail, nl.

/*
Вывод:
1-й:
	find_non_border_pair.
		spain  no border with The italy 
		spain  no border with The germany 
		germany  no border with The italy 
		germany  no border with The portugal 
		france  no border with The portugal 
		italy  no border with The portugal 
2-й:
	find_border_pair.
		spain  border with The france 
		germany  border with The france 
		france  border with The italy 
		spain  border with The portugal 
3-й:
	find_capital.
		paris is the capital of france 
		berlin is the capital of germany 
		roma is the capital of italy 
		madrid is the capital of spain 
		lisboa is the capital of portugal 

4-й:
	find_bord_cap.
		madrid  is the capital of spain  and of france the capital is madrid 
		berlin  is the capital of germany  and of france the capital is berlin 
		paris  is the capital of france  and of italy the capital is paris 
		madrid  is the capital of spain  and of portugal the capital is madrid 
5-й:
	find_water.
		spain  border with the atlantic_ocean 
		italy  border with the mediterranean_sea 
		france  border with the atlantic_ocean 
		germany  border with the north_sea 
		portugal  border with the atlantic_ocean 
6-й:
	find_pop.
		spain has a population 47  million 
		italy has a population 60  million 
		france has a population 67  million 
		germany has a population 83  million 
		portugal has a population 10  million 

7-й:
	find_area.
		spain is the country with the area 505.99000000000001  thousand 
		italy is the country with the area 301.33800000000002  thousand 
		france is the country with the area 643.80100000000004  thousand 
		germany is the country with the area 357.38600000000002  thousand 
		portugal is the country with the area 92.212000000000003  thousand 
8-й:
	find_money.
		spain  have the esp 
		italy  have the itl 
		france  have the frf 
		germany  have the dem 
		portugal  have the pte 
9-й:
	find_color(italy).
		italy  has the color on flag green , white  and red 
10-й:
	find_info(italy).
		italy has area 301.33800000000002  km2,  which has population 60 mln  has border with mediterranean_sea . Country also have national money itl . Country has color on flag green , white  and red . roma is the capital of italy 
*/
