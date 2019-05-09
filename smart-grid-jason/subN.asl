// Agent subN in project IA.mas2j

/* Initial beliefs and rules */
off(subN).
unreachable(subN).
parent(subG, subN).
prev(subM, subN).
cost(subN, 13).

/* Initial goals */

/* Plans */

/* Connections */
+on(X) : parent(X,Y) & unreachable(Y) <- 
		    -unreachable(Y); 
			.broadcast(untell,unreachable(Y));
			+reachable(Y);
			.broadcast(tell,reachable(Y));
			.print(Y, " reachable").

/* Get On */
+energy(Y): priority(X) & reachable(X) & off(X) & cost(X,Z) & Y>=Z <- 
			+on(X);
			-off(X);
			.broadcast(tell,on(X));
			.print(X, " connected").
