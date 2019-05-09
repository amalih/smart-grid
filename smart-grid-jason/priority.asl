// Agent priority in project IA.mas2j

/* Initial beliefs and rules */

off(subA).
off(subB).
off(subC).
off(subF).
off(subG).
off(subL).
off(subM).
off(subN).
off(subO).
off(subP).

prev(subA, subC).
prev(subC, subG).
prev(subG, subL).
prev(subL, subO).
prev(subO, subP).
prev(subP, subF).
prev(subF, subB).
prev(subB, subM).
prev(subM, subN).

!init.

+!init <- .broadcast(tell, priority(subA)).


/* Prioridades */

+on(X) : prev(X,Y) & off(Y) & not priority(Y) <- .broadcast(untell,priority(X)); .broadcast(tell, priority(Y)); .print("Priority: ", Y). 

