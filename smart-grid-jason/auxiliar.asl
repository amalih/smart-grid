// Agent auxiliar in project IA.mas2j

/* Initial beliefs and rules */
energy(70).
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
cost(subA, 5).
cost(subB, 5).
cost(subC, 10).
cost(subO, 40).
cost(subP, 10).
cost(subG, 20).
cost(subL, 13).
cost(subF, 50).
cost(subN, 13).
cost(subM, 13).


/* Initial goals */
!tellenergy.
/* Plans */

+!tellenergy : energy(X)
		<- .print("Starting...");
		.print("Energy: ", X);
		.broadcast(tell, energy(X)).

/* Turn on */

+on(Y) : energy(X) & cost(Y,Z) <- 
						 -+energy(X-Z);
						 -off(Y);
						 .print("Energy: ",(X-Z));
						 .broadcast(untell,energy(X));
						 .broadcast(tell,energy(X-Z)).
	






