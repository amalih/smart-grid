// Agent subG in project IA.mas2j

/* Initial beliefs and rules */
off(subG).
unreachable(subG).
parent(subB, subG).
parent(subO, subG).
child(subN, subG).
child(subL, subG).
cost(subG, 20).
/* Initial goals */

/* Plans */


/* Connections */
+on(X) : parent(X,Y) & unreachable(Y) <- 
		    -unreachable(Y); 
			.broadcast(untell,unreachable(Y));
			+reachable(Y);
			.broadcast(tell,reachable(Y));
			.print(Y, " reachable");
			!on(Y).

/* Get On */
+!on(X): priority(X) & reachable(X) & off(X) & cost(X,Z) & Y>=Z <- 
			+on(X);
			-off(X);
			.broadcast(tell,on(X));
			.print(X, " connected");
			!on(X).
