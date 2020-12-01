PREDICATES

nondeterm human(symbol,symbol,symbol,symbol)
nondeterm gp_check(symbol,symbol,symbol)
nondeterm father(symbol,symbol)
nondeterm mother(symbol,symbol)

CLAUSES

human(h1,m,h2,h3).
human(h2,m,h4,h5).
human(h3,w,h6,h7).
human(h4,m,h8,h9).
human(h5,w,h10,h11).
human(h6,m,h12,h13).
human(h7,w,h14,h14).

father(Код_отца, Код_человека):- human(Код_человека, _ , Код_отца, _ ) , human(Код_отца, m, _, _ );
							 human(Код_человека, _, _,Код_отца), human(Код_отца, m, _, _ ).
							  
mother(Код_матери, Код_человека):- human(Код_человека, _ , Код_матери, _ ) , human(Код_матери, w, _, _ ); 
								human(Код_человека, _, _,Код_матери), human(Код_матери, w, _, _ ).
							   	  
gp_check(Код_человека, Код_дедушки, Код_бабушки):- father(Код_отца, Код_человека), mother(Код_матери, Код_человека), 
												    father(Код_дедушки, Код_отца), mother(Код_бабушки, Код_матери).
												      
GOAL
gp_check(h1, Дедушка, Бабушка).