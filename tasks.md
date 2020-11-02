# Tasks

## Lab 1: Prolog introduction

What do you need to do:
- find and configure any Prolog [implementation](https://en.wikipedia.org/wiki/Comparison_of_Prolog_implementations)
- develop a knowledge base:
  - populate it with some facts
  - add as many rules as possible for extracting additional knowleges out of raw facts
  
Example:

```
male(tom).
female(angela).
female(lisa).
parent(tom, angela).
parent(lisa, angela).

% define mother(X, Y), mother(X)
% define father(X, Y), father(X)
% define son, brother, sister, daughter and other relationship
```

Example 2:

```
hobby(drawing).
hobby(sketching).
related_hobbies(drawing,sketching).
person(john).
likes(john, drawing).

% define common_interest(Person1, Person2)
% define suggested_hobbies(Person)
% define unpopular_hobbies(Hobby)
% define the_most_popular_hobby(Hobby)
```

Example 3:

```
book("Title", 120). % 120 - number of pages
written_by(john, "Title").

% define small_book(Book), huge_book(Book)
% define the_biggest_book(Book)
% define author_of_small_books(Author)
```

## Lab 2: Multi-agent systems

The idea of this task is to try and implement a tiny-tiny simple multiy-agent system,
just to get an idea of it and encounter typical problems in that area.

What do you need to do:
- select some existing MAS framework, suggested ones are:
  - [JADE](https://jade.tilab.com/) for JAVA folks
  - [pade](https://github.com/grei-ufc/pade) for python folks
- get yourself familiar with the framework
- code some simple MAS:
  - you need at least 2 agents that communicate about something
  - it is not enough to just send a message from one to another, there should be
    series of replies
    
Example:

One agent tries to sell something, another one tries to buy that. Both agents have some
conditions, i.e. seller wants to get maximum profit and won't sell if price is below
some MIN_SELL_PRICE; buyer wants to buy at minimum possible price and won't buy if price
is above some MAX_BUY_PRICE. So, those agents communicate with each other trying to either
agree on the price or conclude that the deal can't be performed.

Example 2:

You have several agents that need to from a group. In order to do that agents have to select
a leader within a group. So, they communicate with each other to somehow select a leader.

Example 3:

You have several agents and bunch of tasks for them. Each task require particular skill from an
agent and each agent has a unique skill. So, agents need to re-distribute tasks across them so
all tasks can be completed.