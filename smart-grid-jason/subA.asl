// Agent SubA in project IA.mas2j

/* Initial beliefs and rules */
reachable(subA).
off(subA).
child(subB, subA).
child(subC, subA).
cost(subA, 5).
/* Initial goals */

/* Plans */
+energy(Y): priority(X) & reachable(X) & off(X) & cost(X,Z) & Y>=Z
			<- +on(X);
			-off(X);
			.broadcast(tell,on(X));
			.print(X, " connected").
