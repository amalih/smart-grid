% 

resolution :-

    % INIT
    % define variables 
	Nodes = [A, C, G, L, O, P, F, B, M, N],
 	Costs = [5, 10, 20, 13, 40, 10, 50, 5, 13, 13],
  	Beta = 70,
	
    % define domain
	fd_domain_bool(Nodes),

    % RESTRICTIONS 
    % define source
    A #= 1,

	sum_below(Nodes,Costs,Beta),

    % need to have at least one (non-recursive) parent connected to be connected
    B #==> A, 
    C #==> A,
    O #==> ((G #/\ B) #\/ C),
    P #==> B,
    F #==> C,
    M #==> F,
    N #==> G,
    L #==> G,
    G #==> ((O #/\ C) #\/ B),

    % SOLVE
    fd_maximize((fd_labeling(Nodes), prioritize(Nodes,Pri)), Pri),

	write('Nodes        [A, C, G, L, O, P, F, B, M, N] = '), write([A, C, G, L, O, P, F, B, M, N]), nl,
    nl.


sum_below([A0, A1, A2, A3, A4, A5, A6, A7, A8, A9], [B0, B1, B2, B3, B4, B5, B6, B7, B8, B9], Limit) :-
    Sum = A0*B0 + A1*B1 + A2*B2 + A3*B3 + A4*B4 + A5*B5 + A6*B6 + A7*B7 + A8*B8 + A9*B9,
    Sum #=< Limit.

prioritize([A, C, G, L, O, P, F, B, M, N], Pri) :-
    Pri is A + 1000*C + 500*G + 250*L + 125*O + 60*P + 30*F + 15*B + 7*M + N.
        

:- initialization(resolution).
