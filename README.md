# TwoPhaseSimplexMethod

There are two standard methods for handling artificial variables within the simplex method:

The Big M method

The 2-Phase Method

Although they seem to be different, they are essentially identical. However, methodologically the 2-Phase method is much superior. We shall therefore focus on it.

The 2-Phase method is based on the following simple observation: Suppose that you have a linear programming problem in canonical form and you wish to generate a feasible solution (not necessarily optimal) such that a given variable, say x3, is equal to zero. Then, all you have to do is solve the linear programming problem obtained from the original problem by replacing the original objective function by x3 and setting opt=min.

If more than one variable is required to be equal to zero, then replace the original objective function by the sum of all the variables you want to set to zero.

Observe that because of the non-negativity constraint, the sum of any collection of variables cannot be negative. Hence the smallest possible feasible value of such a sum is zero. If the smallest feasible sum is strictly positive, then the implication is that it is impossible to set all the designated variables to zero.
