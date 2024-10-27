# Analysis and Implementation of QPE for period finding

This repository contains the code and the results obtained during the development of the TFG/Bachelor's Thesis titled **"Detailed Analysis of Shor's Algorithm in Quantum Computing"**. 
The project focuses on the study of Shor's algorithm and its implementation using quantum computing. Specifically, it is explored the limits of the QPE used in Shor's algorithm for order finding, to apply for other type of functions for period finding. 

In this work, the Fibonacci sequence is implemented via quantum modular arithmetics and evaluated for moduli represented by 2 or 3 qubits (i.e., 2, 3, 4, 5, 6 and 7 in binary). All this is done with the **Qiskit** software.

## Project Description

The main objective of this project is to analyze and experiment with the **QPE** and its ability to obtain a phase and, subsequently, a period/order related to the function evaluated. 
Additionally, it explores its adaptation to identify periodicity in other functions, such as the **modulated Fibonacci sequence**. 
The results of this work demonstrate the applicability of the algorithm in different contexts and reveal its limitations. 
Also, further investigation and its expectations are addressed.

### Repository Contents

- **Source Code**: Implementations of QPE, periodicity identification in the Shor's algorithm's modular exponentiation and modulated Fibonacci sequence. There are two .py files for implementimg the quantum modular arithmetics and its integration for period finding in Fibonacci's case. Also, there is a .ipynb for the period finding of modular exponentiation giving further explanation as how this algorithm is structured.
- **Plots**: Results (in the form of plots) from the simulations conducted using Qiskit (v1.1.0) to verify the effectiveness of the algorithm.
- **Documentation**: Link to the TFG/Bachelor's Thesis: ...
