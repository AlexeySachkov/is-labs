/*
Definition of grandfather and grandmother.
Initial data:
– Person's code, his gender, his parent's code1, his parent's code2
- Person code
Result:
Human code, grandfather code, grandmother code.
*/
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

father(Key_Father, Key_Person):- human(Key_Person, _ , Key_Father, _ ) , human(Key_Father, m, _, _ );
							 human(Key_Person, _, _,Key_Father), human(Key_Father, m, _, _ ).
							  
mother(Key_Mother, Key_Person):- human(Key_Person, _ , Key_Mother, _ ) , human(Key_Mother, w, _, _ ); 
								human(Key_Person, _, _,Key_Mother), human(Key_Mother, w, _, _ ).
							   	  
gp_check(Key_Person, Key_Grandpa, Key_Grandmother):- father(Key_Father, Key_Person), mother(Key_Mother, Key_Person), 
												    father(Key_Grandpa, Key_Father), mother(Key_Grandmother, Key_Mother).
												      
GOAL
gp_check(h1, Grandpa, Grandmother).