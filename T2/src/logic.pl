:- dynamic valid/2.
:- dynamic current/2.
:- dynamic adjacent/4.
:- dynamic visited/2.
:- dynamic energy/1.
:- dynamic ammo/1.


/* sensor para ouro (na mesma posicao) */
:- dynamic sensor_gold/2.

/* sensor para ameaca (em posicao adjacente) */
:- dynamic sensor/3.

/* regioes onde existe alguma ameaca */
:- dynamic dont_go/2.


/* posicao valida (range valido) */
/* (tambem é usado como ponto de partida para valores de X e Y) */
valid(X,Y) :- between(0,11,X), between(0,11,Y).

/* posicao na fronteira do mapa */
border(X,Y) :- valid(X,Y), (X=0;X=11;Y=0;Y=11).

/* distancia */
dist(D,X1,Y1,X2,Y2) :- D is abs(X1-X2) + abs(Y1-Y2).

/* vizinhos */
adjacent(X1, Y1, X2, Y2) :- valid(X2, Y2), X2 is X1+1, Y1 = Y2.
adjacent(X1, Y1, X2, Y2) :- valid(X2, Y2), X2 is X1-1, Y1 = Y2.
adjacent(X1, Y1, X2, Y2) :- valid(X2, Y2), X1 = X2, Y2 is Y1+1.
adjacent(X1, Y1, X2, Y2) :- valid(X2, Y2), X1 = X2, Y2 is Y1-1.

/* diagonal */
diagonal(X1, Y1, X2, Y2) :- valid(X2, Y2), X2 is X1+1, Y2 is Y1+1.
diagonal(X1, Y1, X2, Y2) :- valid(X2, Y2), X2 is X1-1, Y2 is Y1+1.
diagonal(X1, Y1, X2, Y2) :- valid(X2, Y2), X2 is X1+1, Y2 is Y1-1.
diagonal(X1, Y1, X2, Y2) :- valid(X2, Y2), X2 is X1-1, Y2 is Y1-1.


/* local seguro */
safe(X, Y) :- valid(X, Y), visited(X, Y), not(dont_go(X,Y)).

safe(X, Y) :- valid(X, Y), adjacent(X, Y, X2, Y2), visited(X2, Y2), 
              not(sensor(_,X2, Y2)), not(dont_go(X,Y)).

distance(X1, Y1, X2, Y2, D) :- D is abs(X1-X2)+abs(Y1-Y2).



/* Se acabou a energia, morre */
best_action(die, none1, none2) :- energy(E), E < 1.

/* Se sensor de ouro, pega o outro */
best_action(pickGold, X, Y) :- valid(X, Y), current(X, Y), sensor_gold(X, Y).


/* Passo simples para locais seguros e ainda nao visitados */
best_action(walk, X, Y) :- valid(X, Y), safe(X, Y), not(current(X, Y)), not(visited(X, Y)), current(XX, YY), adjacent(X, Y, XX, YY), not(dont_go(X,Y)).


/*** Anda em regioes proximas a ameacas, tomando o devido cuidado ***/
/* A regra abaixo determina a posicao X,Y pra onde deseja-se ir, */
/*		atraves da determinacao da posicao XT,YT de uma ameaca do tipo T,  */
/* 		e evitando tambem que se caia em outra ameaca T2 por engano. */
best_action(recklessWalk, X, Y) :- valid(X, Y), not(visited(X,Y)), valid(XT,YT), not(dont_go(X,Y)),
	valid(XS1,YS1), sensor(T,XS1,YS1), adjacent(XS1,YS1,XT,YT),
	valid(XS2,YS2), sensor(T,XS2,YS2), adjacent(XS2,YS2,XT,YT), [XS1,YS1] \= [XS2,YS2],
	not( (valid(XS3,YS3), sensor(T,XS3,YS3), adjacent(XS3,YS3,XT,YT), [XS3,YS3] \= [XS2,YS2], [XS1,YS1] \= [XS3,YS3]) ),
	not( (valid(XS4,YS4), sensor(T,XS4,YS4), adjacent(XS4,YS4,X,Y), [XS2,YS2] \= [XS4,YS4], [XS1,YS1] \= [XS4,YS4]) ),
	not( ( border(X,Y), aggregate_all(count, (sensor(_,XS5,YS5), adjacent(XS5,YS5,X,Y)), CountB), CountB>1 ) ),
	[X,Y] \= [XT,YT], adjacent(X,Y,XS1,YS1),
	not( (sensor(T2,XT2,YT2),adjacent(X,Y,XT2,YT2), T \= T2) ),
	aggregate_all(count,( (sensor(_,XT3,YT3)) ,diagonal(X,Y,XT3,YT3) ), Count), Count <3.

/* Atira em inimigos que possam liberar uma quantidade significativa de posiçoes nao visitadas */
best_action(shoot, X, Y) :- ammo(A), A > 0, valid(X,Y), valid(XA,YA), visited(XA,YA), adjacent(XA,YA,X,Y),
	valid(XS1,YS1), sensor(enemy,XS1,YS1), adjacent(XS1,YS1,X,Y),
	valid(XS2,YS2), sensor(enemy,XS2,YS2), adjacent(XS2,YS2,X,Y), [XS1,YS1] \= [XS2,YS2],
	valid(XS3,YS3), (sensor(enemy,XS3,YS3);not(visited(XS3,YS3))), adjacent(XS3,YS3,X,Y), [XS3,YS3] \= [XS2,YS2], [XS1,YS1] \= [XS3,YS3],
	aggregate_all(count, (valid(XN,YN), not(safe(XN,YN)), diagonal(X,Y,XN,YN)), Count), Count > 1.

/* Ultima possibilidade: sair */
best_action(escape, p1, p2) :- true.


