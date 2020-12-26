%Компьютерные игры

%База состоит из разнообразных фактов о 8 компьютерных играх: название, оценка, жанр, издатель, разработчик, год выпуска.

game(lineage2, 7).
game(dbd, 7.1).
game(friday13, 6.5).
game(kopateli, 5).
game(minecraft, 9).
game(dota2, 8.2).
game(cs, 8).
game(league, 7.5).

genre(lineage2, rpg).
genre(lineage2, fantasy).

genre(dbd, horror).
genre(dbd, survival).

genre(friday13, horror).
genre(friday13, survival).

genre(kopateli, sandbox).
genre(kopateli, indie).

genre(minecraft, sandbox).
genre(minecraft, indie).

genre(dota2, moba).
genre(dota2, strategy).
genre(dota2, cybersport).

genre(cs, shooter).
genre(cs, action).
genre(cs, cybersport).

genre(league, moba).
genre(league, strategy).
genre(league, cybersport).

distributor(lineage2, fourgame).
distributor(dbd, steam).
distributor(friday13, steam).
distributor(kopateli, vk).
distributor(minecraft, mojang).
distributor(dota2, steam).
distributor(cs, steam).
distributor(league, riot).

info(lineage2, ncsoft, 2003).
info(dbd, behaviour, 2016).
info(friday13, gunmedia, 2017).
info(kopateli, diggerworld, 2015).
info(minecraft, mojang, 2011).
info(dota2, valve, 2013).
info(cs, valve, 2012).
info(league, riot, 2009).

%Данный запрос определяет игры, подходящие под определенный жанр
what_genre_do_i_want(Genre) :- genre(Game, Genre), format('~w ~s game you wanted ~n', [Game, "is the"]), fail.

%Данный запрос выводит на экран все игры, у которых оценка выше 8
games_with_score_8_and_more :- game(Game, Score), Score>=8, format('~w ~s game with the score ', [Game, "is the"]), format('~w ~n',[Score]), fail, nl.

%Данный запрос определяет распространителя выбранной игры
what_distributor(Game) :- distributor(Game, Distributor), format('~w ~s distributor of this game ~n', [Distributor, "is the"]).

%Данный запрос выводит на экран все игры, которые есть в киберспортивных соревнованиях
cybersport_games :- genre(Game, Genre), Genre='cybersport', write(Game), write('   '), fail, nl.

%Данный запрос выводит все игры с их оценками
games :- game(Game, Score), format('~w ~s game with the score ', [Game, "is the"]), format('~w ~n',[Score]), fail, nl.

%Данный запрос проверяет правильность введенного жанра у игры
correct_genre(Genre, Game) :- genre(Game, Genre).

%Данный запрос выводит на экран игры, вышедшие в определенном году
year(Year) :- info(Game, Developer, Year), format('~w ~s released in ',[Game, "was"]), format('~w ~n',[Year]).

%Данный запрос показывает всю информацию по определенной игре
full_info(Game) :- game(Game, Score), genre(Game, Genre), distributor(Game, Distributor), info(Game, Developer, Year), format('~w ~s genre ', [Game, "has"]), format('~w ~s it was developed by ', [Genre, ", and"]), format('~w ~s gave this to ', [Developer, "who"]), format('~w ~s it was released in ', [Distributor, ". After"]), format('~w ~s score ', [Year, "and take"]), format('~w', [Score]).
-----------------------------------------------------------------------------------------------------------------------------------
/*Вывод:
1-й запрос
	?- what_genre_do_i_want(strategy).
		dota2 is the game you wanted 
		league is the game you wanted
2-й запрос
	?- games_with_score_8_and_more.
		minecraft is the game with the score 9 
		dota2 is the game with the score 8.1999999999999993 
		cs is the game with the score 8 
3-й запрос
	?- what_distributor(dbd).
		steam is the distributor of this game 
4-й запрос
	?- cybersport_games.
		dota2   cs   league 
5-й запрос
	?- games.
		lineage2 is the game with the score 7 
		dbd is the game with the score 7.0999999999999996 
		friday13 is the game with the score 6.5 
		kopateli is the game with the score 5 
		minecraft is the game with the score 9 
		dota2 is the game with the score 8.1999999999999993 
		cs is the game with the score 8 
		league is the game with the score 7.5
6-й запрос
	?- correct_genre(shooter, dota2).
		no
	?- correct_genre(shooter, cs).
		true
7-й запрос
	?- year(2015).
		kopateli was released in 2015 
8-й запрос
	?- full_info(league).
		league has genre moba , and it was developed by riot who gave this to riot . After it was released in 2009 and take score 7.5
*/
