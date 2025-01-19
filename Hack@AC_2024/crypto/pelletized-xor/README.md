# Pelletized XOR

The challenge revolves around a pell equation $(x^2 - 3y^2 = 1)$ for positive integers $x$, $y$.<br>
A randomly generated $key$ (list of integers same length as flag) is provided.

User provides input (sequence of numbers, same length as flag).
Each number must a valid integer solution of $x$ for the pell equation.
The server computes $floor(\log_{m}(number))$ for number in input, to construct a sequence of integers, $s$.

The server then returns (s XOR key XOR flag)

Thus, the goal is for the user to get $s = key$ (where $key$ is known) by being able to find solutions to the pell equation between $m^k$ and $m^{k+1}$ for the list of integers $k$ in $key$.
