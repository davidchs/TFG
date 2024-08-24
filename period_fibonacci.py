import quantum_arithmetic as qa

from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram

import numpy as np
import random
import matplotlib.pyplot as plt

from math import gcd
from fractions import Fraction
from collections import defaultdict

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, AncillaRegister, transpile



def superposition(circuit, num_qubits):
    """
    this function applies Hadamard gates to each qubit in the circuit and returns the circuit updated
    
    circuit: quantum circuit
    num_qbits: number of qubits used for the circuit 
    """
    for i in range(num_qubits):
        circuit.h(i)

    return circuit

def c_U(circuit, num_qubits, mod_bin, n):
    """
    this function applies the controlled gate in the circuit
    
    circuit: quantum circuit
    num_qbits: number of qubits used for the circuit
    mod_bin: module of the function in binary
    n: number of qubits needed to represent the module in binary
    """
    for qubit in range(num_qubits):
        controlled = qa.c_fibmodN(n, mod_bin, 2**qubit) 
        circuit.append(controlled, [qubit] + [l+num_qubits for l in range(4*n+2)])

    return circuit

def psi(circuit, num_qubits, mod_bin, n):
    """
    this function creates the state psi, which is the eigenvector of the controlled gate

    circuit: quantum circuit
    num_qubits: number of qubits used for the circuit
    mod_bin: module of the function in binary
    n: number of qubits needed to represent the module in binary
    """
    # Create F(n-1) = 0...01, F(n-2) = 0...00 and N
    circuit.x(num_qubits)
    # Create N
    """for i, qubit in enumerate(mod_bin):
        if int(qubit) == 1:
            circuit.x(num_qubits+2*n+1+i)"""
    circuit.barrier()
    circuit = c_U(circuit, num_qubits, mod_bin, n)

    return circuit

def qpe(circuit, num_qubits, mod_bin, n):
    """
    all the previous function are orderly applied creating the Quantum Phase Estimation algorithm

    circuit: quantum circuit
    num_qubits: number of qubits used for the data register
    bin: module of the function in binary
    n: number of qubits needed to represent the module in binary
    """
    circuit = superposition(circuit, num_qubits)
    circuit = psi(circuit, num_qubits, mod_bin, n)
    circuit.barrier()
    circuit.append(QFT(num_qubits, inverse=True).to_gate(label="QFT†"), range(num_qubits))
    circuit.barrier()
    circuit.measure(range(num_qubits), range(num_qubits))

    return circuit

def power_2(n):
    """
    function to check if n is a power of 2

    n: number to check
    """
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

# Value of the module 'N' for this case
N = 6 # big values spent much time
mod_bin = bin(N)[2:]

# Number of qubits 't' selected  with the relation: t >= 2 * log N
if power_2(N):
    n = int(np.ceil(np.log2(N))) + 1
else:
    n = int(np.ceil(np.log2(N)))
num_qubits = 2 * n

# Creation of registers and circuit
data = QuantumRegister(num_qubits, name="data")
target = QuantumRegister(4*n+2, name="target")
classical = ClassicalRegister(num_qubits, name="classical")
circuit = QuantumCircuit(data, target, classical)
circuit = qpe(circuit, num_qubits, mod_bin, n)
# circuit.draw(output='mpl', fold=-1)

sim = AerSimulator()
Shots = 250
transpiled_circuit = transpile(circuit, backend = sim)
sim_run = sim.run(transpiled_circuit, shots = Shots, memory = True)
sim_result=sim_run.result()
counts_result = sim_result.get_counts()
  
phases = defaultdict(list)
print('''Printing the various results followed by how many times they happened (out of the {} cases):\n'''.format(Shots), flush = True)
for i in range(len(counts_result)):

    print('-> Result \"{0}\" happened {1} times out of {2}'.format(
            list(sim_result.get_counts().keys())[i],
            list(sim_result.get_counts().values())[i],Shots), 
            flush = True)
    phases[list(sim_result.get_counts().keys())[i]].append(
            list(sim_result.get_counts().values())[i])
    
fig, ax = plt.subplots()

# Create the histogram of phase values
plot_histogram(phases, ax=ax) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha="center")
plt.show()

periods = defaultdict(list)
for i in range(len(counts_result)):

    all_registers_output = list(sim_result.get_counts().keys())[i]  
    output_desired = all_registers_output
            
    phase = int(output_desired, 2)/(2**num_qubits)

    if phase != 0:           
        print(' ', flush = True)
        print("--> Analysing result {0}. ".format(output_desired), flush = True)

        """ Print the final phase to user """
        print('---> In decimal, phase value for this result is: {0}'.format(phase), flush = True)

        """ Print the period to user """
        frac = Fraction(phase).limit_denominator(2**(num_qubits-1))
        r = frac.denominator
        print('---> The period found for this result is: {0}'.format(r),  flush = True)     
    else:
        print(' ', flush = True)
        print("--> Analysing result {0}. ".format(output_desired), flush = True)

        """ Print the final phase to user """
        print('---> In decimal, phase value for this result is: {0}'.format(phase), flush = True)

        """ Print the period to user """
        # If the phase is equal to 0.0 this means the function has periodicity of 1
        r = 1 
        print('---> The period found for this result is: {0}'.format(r),  flush = True)

    periods[r].append(list(sim_result.get_counts().values())[i])

fig, ax = plt.subplots()

# Gathering total counts of each period, histogram shown
all_periods = {key: sum(values) for key, values in periods.items()} 
plot_histogram(all_periods, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha="center")
plt.show()