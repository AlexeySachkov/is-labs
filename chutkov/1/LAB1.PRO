DOMAINS

PREDICATES
nondeterm car(symbol, symbol, symbol)
nondeterm person(symbol, integer)
nondeterm owner(symbol, symbol)
nondeterm hasLicense(symbol)
nondeterm havePermisionOnCar(symbol, symbol)
nondeterm havePermitionToDrive(symbol)
nondeterm haveAccessToCar(symbol, symbol)
nondeterm canDrive(symbol, symbol)

CLAUSES
car(ytf220, bmw, red). %f1
car(gxt781, toyota, white). %f2
car(nya501, citroen, gray). %f3
car(jbc700, bmw, blue). %f4
car(gkt912, rangerover, black). %f5

person(michael, 25). %f6
person(ana, 19). %f7
person(jack, 43). %f8
person(diana, 31). %f9
person(tasha, 50). %f10

hasLicense(michael). %f11
hasLicense(jack). %f12
hasLicense(tasha). %f13

owner(michael, ytf220). %f14
owner(jack, gxt781). %f15
owner(tasha, jbc700). %f16
owner(diana, nya501). %f17
owner(ana, gkt912). %f18

havePermisionOnCar(jack, ytf220).
havePermisionOnCar(ana, gxt781).
havePermisionOnCar(tasha, gkt912).

havePermitionToDrive(Name) :- person(Name, Age), Age>17, hasLicense(Name). %r1
haveAccessToCar(Name, CarNumber) :- owner(Name, CarNumber); havePermisionOnCar(Name, CarNumber). %r2
canDrive(Name, CarNumber):- havePermitionToDrive(Name), haveAccessToCar(Name, CarNumber). %r3

GOAL
% car(_, bmw, Colour). %g1
/*
Colour=red
Colour=blue
2 Solutions
*/

% person(Name, Age). %g2
/*
Name=michael, Age=25
Name=ana, Age=19
Name=jack, Age=43
Name=diana, Age=31
Name=tasha, Age=50
5 Solutions
*/

% owner(Name, nya501). %g3
/*
Name=diana
1 Solution
*/

% owner(Name, jbc700). %g4
/*
Name=tasha
1 Solution
*/

% havePermitionToDrive(ana). %g5
/*
no
*/

% haveAccessToCar(Name, Car). %g6
/*
Name=michael, Car=ytf220
Name=jack, Car=gxt781
Name=tasha, Car=jbc700
Name=diana, Car=nya501
Name=ana, Car=gkt912
Name=jack, Car=ytf220
Name=ana, Car=gxt781
Name=tasha, Car=gkt912
8 Solutions
*/

% havePermitionToDrive(Name). %g7
/*
Name=michael
Name=jack
Name=tasha
3 Solutions
*/

% canDrive(ana, _). %g8
/*
no
*/

% canDrive(Name, Car). %g9
/*
Name=michael, Car=ytf220
Name=jack, Car=gxt781
Name=jack, Car=ytf220
Name=tasha, Car=jbc700
Name=tasha, Car=gkt912
5 Solutions
*/