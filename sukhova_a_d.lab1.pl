%Приведены сведения о двух компаниях. Описаны отделы и сотрудники в них. О сотруднике известно: имя, должность, зарплата.

company('Google').
company('Microsoft').

department('Google', 'Pixel').
department('Google', 'Crunch').

employee('Bronte Hester', 'Developer').
employee('Jaxon Esquivel', 'Developer').
employee('Mandy Pritchard', 'Developer').
employee('Jevan Burrows', 'Developer').
employee('Sharmin Galindo', 'QA').
employee('Eleanor Howe', 'QA').
employee('Havin Hulme', 'Project manager').
employee('Niko Clarke', 'Project manager').
employee('Alexandra Sukhova', 'UX/UI designer').

salary('QA', 300).
salary('Developer', 2000).
salary('Project manager', 5000).
salary('UX/UI designer', 1500).

staff('Pixel', 'Bronte Hester').
staff('Pixel', 'Jaxon Esquivel').
staff('Pixel', 'Sharmin Galindo').
staff('Pixel', 'Havin Hulme').
staff('Crunch', 'Mandy Pritchard').
staff('Crunch', 'Jevan Burrows').
staff('Crunch', 'Eleanor Howe').
staff('Crunch', 'Alexandra Sukhova').
staff('Crunch', 'Niko Clarke').

%Предикат содержит сведения о сотрудниках в команде
team(Team) :- staff(Team, Employee),
    employee(Employee, Position),
    format('~w - ~s ~n', [Employee, Position]), fail.

%Предикат содержит информацию о всех сотрудниках в компании
employees(Company) :- department(Company, Team), team(Team).

%Предикат определяет всех людей на заданной должности 
positions(Company, Position) :- department(Company, Team), staff(Team, Employee), employee(Employee, Position), write(Employee), nl, fail.

%Предикат сравнивает зарплату сотрудника на заданной должности с минимумом
alive(Employee) :- salary(Employee, Salary), Salary >= 300, format('~w Still alive', [Employee]),nl.

%Предикат описывает сотрудника
employee_info(Employee) :- 
staff(Team, Employee),
department(Company, Team),
employee(Employee, Position),
salary(Position, Salary),
format('~w | ~w | ~w | ~w | ~w  ~n', [Employee, Position, Salary, Team, Company]), nl.

?-team('Pixel').
?-format('~n').
?-alive('QA').
?-format('~n').
?-positions('Google', 'Developer').
?-format('~n').
?-employee_info('Jevan Burrows').
