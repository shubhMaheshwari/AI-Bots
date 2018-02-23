# IDA
	Compatively Slower than DFS 
	Espically on the middle moves because it is always returing 0 Hence always walking a dead end
	We need an Evaluator at depth == 0 to make it better
	Very slow before 60
		15 sec

# IDA vs DFS		
	Not effectve in this game

# Monte Carlo is only better for starting states not afterward	

	Make sure to have the right ratio of randomness and exploration. Number of times montecarlo ran and depth of the game
	Monte Carlo was a failure 
	Too much computation we dont even have the time

# DFS 
	Good only if depth >=100


# Good Heuristics 
##	Good database
	Solve the problem for some specific situiations 
##	Forward pruning
	Prune the obviously bad moves 
	Beam Search 
		N actions are each choosen at random, dending on IDA, but can lose the best state 
	Simulated annealing 

##	PROBCUT(Probablistic Cut algorithm)
		alpha beta with probablity when cheking their values  

	Prier games played earlier to calculate the values.  
	At Each depth how good is this value. 

	Acc = 64% with half of the time needed

	LARGE transposition table
	Table lookup 

	Espically opening and closing move
	Look up their can be useful 


## Probablity Theory


## Decision Theory 
	Uncerantity: Situiation needs a right decision. instead of a good or bad situiation