%Задача: узнать кто в какие игры играет.
PREDICATES 
%область предикатов
nondeterm играет(symbol,symbol)
CLAUSES 
%правила и факты
 играет(дарья,мморпг). 	 %факт1
 играет(вика,шутер). %факт2
 играет(илья,хоррор). %факт3
 играет(иван,платформер). %факт4
 играет(кира,файтинг). %факт5
 играет(лена,стратегии). %факт6
 играет(маша,симулятор). %факт7


  %играет(коля, ролевые):-играет(вика, шутер), играет(кира, файтинг), играет(маша, симулятор). %правило1
  % формулировка : коля играет в ролевые игры, при условии, что вика играет в шутеры и кира играет в файтинги и маша играет в симуляторы одновременно

  %играет(иван, платформер):-играет(илья, хоррор); играет(вика, мморпг); играет(маша, симулятор). %правило2
  %иван играет в платформер, если илья играет в хоррор и иван играет в платформер, если вика играет в мморпги
  %иван играет в платформер, если маша играет в симулятор

  играет(Кто, шутер):-играет(Кто, файтинг). %правило3
  %при условии что кто-то играет в шутер, то он играет и в файтинг

  играет(Кто,ролевые ):-играет(Кто, мморпг). %правило4
  %Если кто-то играет в ролевые игры, то он играет в мморпг

  играет(Кто,резидентивл) :- играет(Кто, шутер), играет(Кто, хоррор), играет(Кто, файтинг). %правило5
  %кто-то играет в Резидент ивл, при условии, что он играет в шутеры, хорроры и файтинги
  
   играет(илья,шутер):- играет(вика,шутер);играет(дарья,мморпг). %правило6
  %Илья играет в шутер при условии что вика играет в шутер или дарья играет в мморпг



GOAL 
%область запросов

 играет(дарья, мморпг).  %запрос1
  %Играет ли Дарья в мморпг?

  %играет(кто, хоррор). %запрос2
  %Кто играет в хорроры?

  %играет(кто, что). %запрос3
  %Кто и во что играет?

  %играет(вика, файтинг ). %запрос4
  %Играет ли вика в файтинги?

  %играет(иван, платформер). %запрос5
  %Играет ли иван в платфомеры?

  %играет(кто, симулятор). %запрос6
  %Кто играет в симуляторы?

  %играет(кто, резидентивл). %запрос7
  %Играет ли кто-то в резидентивл?

  %играет(кто, хоррор). %запрос8
  %кто играет в хоррор?


 /* Результаты 
 
 1. Цель: играет(дарья, мморпг).
          yes факт1
        
 2. Цель: играет(кто, шутер).
          кто=вика факт2
         
 3. Цель: играет(кто, что). 
          кто=дарья, что=мморпг
		кто=вика, что=шутер
		кто=илья, что=хоррор
		кто=ира, что=файтинг   факты 1-4
         
 4. Цель: играет(петя, ролевые).
          no правило1
         
 	 
 */
