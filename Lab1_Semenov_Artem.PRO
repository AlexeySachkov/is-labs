PREDICATES
nondeterm herb(symbol,integer)
nondeterm where(symbol,symbol)
nondeterm when(symbol,symbol)
nondeterm for_what_purpose(symbol, symbol)
nondeterm what_herbs(symbol,symbol)
nondeterm if_i_am_here(symbol,symbol)
nondeterm rarest(symbol,integer)
nondeterm the_rarest(symbol,integer)
nondeterm frequent(symbol,integer)
nondeterm the_frequent(symbol,integer)
nondeterm if_season_is_now(symbol,symbol)
nondeterm possibility_to_collect(symbol,symbol,symbol)
nondeterm need_help_now(symbol,symbol,symbol,symbol)

CLAUSES
% число означет примерную частоту встречаемости данного растения (1-10)
herb(thyme, 8). 		%thyme - чабрец  
herb(tutsan, 6).		%tutsan - зверобой
herb(salvia, 4).		%salvia - шалфей
herb(eucalyptus,7).		%eucalyptus - эвкалипт
herb(sagebrush, 6).		%sagebrush - полынь
herb(immortelle, 6).	%immortelle - бессмертник
herb(linen, 7).			%linen - лен
herb(calendula, 5).		%calendula - календула
herb(chamomile, 9).		%chamomile - ромашка

when(thyme,may).
when(thyme,june).
when(thyme,july).
when(thyme,august).

when(tutsan,june).
when(tutsan,july).
when(tutsan,august).

when(salvia,july).
when(salvia,september).

when(eucalyptus,august).
when(eucalyptus,september).
when(eucalyptus,october).

when(sagebrush,july).
when(sagebrush,august).

when(immortelle,june).
when(immortelle,july).

when(linen,august).
when(linen,september).

when(calendula,july).
when(calendula,august).
when(calendula,september).

when(chamomile,june).
when(chamomile,july).
when(chamomile,august).


for_what_purpose(thyme,hypertension). 	
for_what_purpose(tutsan,hypertension).		
for_what_purpose(tutsan,liver_disease).
for_what_purpose(tutsan,stomach_diseases).
for_what_purpose(salvia,lung_disease).
for_what_purpose(salvia,hypertension). 
for_what_purpose(eucalyptus,lung_disease).	
for_what_purpose(eucalyptus,cold).
for_what_purpose(sagebrush,liver_disease).	
for_what_purpose(sagebrush,stomach_diseases).
for_what_purpose(immortelle,liver_disease).	
for_what_purpose(immortelle,kidney_disease).
for_what_purpose(linen,kidney_disease).
for_what_purpose(calendula,stomach_diseases).		
for_what_purpose(chamomile,cold).		
for_what_purpose(chamomile,hypertension).
for_what_purpose(chamomile,kidney_disease).


where(tutsan,woods).
where(tutsan,fields).
where(thyme,mountains).
where(thyme,woods).	
where(salvia,woods).
where(salvia,shores).
where(eucalyptus,woods).
where(eucalyptus,shores).
where(sagebrush,fields). 
where(immortelle,steppe).
where(immortelle,woods).
where(linen,steppe).
where(linen,woods).
where(calendula,fields).
where(chamomile,fields).
where(chamomile,steppe).

%Если у меня что-то болит, какие нужны мне расстения
what_herbs(Disease,Herbs):- for_what_purpose(Herbs,Disease).

%Если я нахожусь в какому-то месте, что я могу собрать
if_i_am_here(Place,Herbs):- where(Herbs,Place).

%Поиск самого маленького числа
rarest(Herb, Number):- herb(Herb,Count),Count < Number,!,fail.
rarest(_,_).

%Поиск самого редкого растения
the_rarest(Herb,Number):-herb(Herb,Number),rarest(_,Number),!.

%Поиск самого большого числа
frequent(Herb, Number):- herb(Herb,Count),Count > Number,!,fail.
frequent(_,_).

%Поиск самого частого растения
the_frequent(Herb,Number):-herb(Herb,Number),frequent(_,Number),!.

%Если сейчас какой-то месяц, что я могу собрать?
if_season_is_now(Season,Herbs):-when(Herbs,Season).
 
%Что я могу собрать в данном месте в данное время?
possibility_to_collect(Place,Season,Herbs):-when(Herbs,Season),where(Herbs,Place).

%Что я могу собрать сейчас в этом месте, чтоб помочь с определенной болью.
need_help_now(Disease,Place,Season,Herbs):- for_what_purpose(Herbs,Disease),when(Herbs,Season),where(Herbs,Place).

GOAL
%the_frequent(Herb, Number).
need_help_now(hypertension,woods,july,Herbs).


