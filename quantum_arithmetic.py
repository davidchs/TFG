from qiskit import *

def carry(circuit, q0, q1, q2, q3, inverse: str):
    """
    this function performs the carry operation needed in the plain adder

    circuit: quantum circuit
    q0, q1, q2, q3: qubits involved in the carry operation positioned as shown in figure
    inverse: string evaluating whether the operation is performed in reverse or not
    """
    # Start performing the carry following the figure scheme
    if inverse:
        circuit.ccx(q0,q2,q3)
        circuit.cx(q1,q2)
        circuit.ccx(q1,q2,q3)
    else:
        circuit.ccx(q1,q2,q3)
        circuit.cx(q1,q2)
        circuit.ccx(q0,q2,q3)

    return circuit

def sum(circuit, q0, q1, q2, inverse: str):
    """
    this function performs the sum operation needed in the plain adder

    circuit: quantum circuit
    q0, q1, q2: qubits involved in the carry operation positioned as shown in figure
    inverse: string evaluating whether the operation is performed in reverse or not
    """
    # Start performing the sum following the figure scheme
    if inverse:
        circuit.cx(q0,q2)
        circuit.cx(q1,q2)
    else:
        circuit.cx(q1,q2)
        circuit.cx(q0,q2)

    return circuit

def adder(circuit, a, b, c, inverse: str):
    """
    this function performs the plain adder of a + b

    circuit: quantum circuit
    a: n-qubit register 
    b: n+1-qubit register
    c: n-qubit ancilla register
    inverse: string evaluating whether the operation is performed in reverse or not
    """
    # Calculate n 
    n = len(a)
    
    # Start performing the addition following the figure scheme
    if inverse:
        for i in range(n-1):
            circuit = sum (circuit, c[i], a[i], b[i], inverse = True)
            circuit = carry(circuit, c[i], a[i], b[i], c[i+1], inverse = False)
        circuit = sum(circuit, c[n-1], a[n-1], b[n-1], inverse = True)
        circuit.cx(a[n-1], b[n-1])
        circuit = carry(circuit, c[n-1], a[n-1], b[n-1], b[n], inverse = True)
        for i in reversed(range(n-1)):
            circuit = carry(circuit, c[i], a[i], b[i], c[i+1], inverse = True)
    else:
        for i in range(n-1): 
            # Carry value to c_{i+1} from checking c[i], a[i] and b[i]
            circuit = carry(circuit, c[i], a[i], b[i], c[i+1], inverse = False)
        # Carry most significant bit to b[n]
        circuit = carry(circuit, c[n-1], a[n-1], b[n-1], b[n], inverse = False)
        circuit.cx(a[n-1], b[n-1])
        circuit = sum(circuit, c[n-1], a[n-1], b[n-1], inverse = False)
        for i in reversed(range(n-1)):
            # Undo carry to restore ancilla 
            circuit = carry(circuit, c[i], a[i], b[i], c[i+1], inverse = True)
            circuit = sum (circuit, c[i], a[i], b[i], inverse = False)

    return circuit

def addmodN(circuit, a, b, N, mod_bin: str, c, t):
    """
    this function performs the modular addition a + b mod N

    circuit: quantum circuit
    a: n-qubit register 
    b: n+1-qubit register
    N: n-qubit register representing the module
    mod_bin: string depicting the module in binary
    c: n-qubit ancilla register
    t: ancilla qubit
    """
    # Start performing the gates following the figure scheme
    circuit = adder(circuit, a, b, c, inverse = False)
    circuit = adder(circuit, N, b, c, inverse = True)

    # Ancilla qubit usage (overflow)
    circuit.x(b[-1])
    circuit.cx(b[-1], t)
    circuit.x(b[-1])

    # Modular subtraction if overflowed
    for i, qubit in enumerate(mod_bin):
        if int(qubit) == 1:
            circuit.cx(t, N[i])
    circuit = adder(circuit, N, b, c, inverse = False)
    for i, qubit in enumerate(mod_bin):
        if int(qubit) == 1:
            circuit.cx(t, N[i])

    # Restoring of ancilla
    circuit = adder(circuit, a, b, c, inverse = True)
    circuit.cx(b[-1], t)
    circuit = adder(circuit, a, b, c, inverse = False)

    return circuit

def fibmodN(circuit, a, b, N, mod_bin: str, c, t):
    """
    this function performs the calculation of the next Fibonacci sequence's value mod N

    circuit: quantum circuit
    a: n-qubit register {F(n-1)}
    b: n+1-qubit register {F(n-2)}
    N: n-qubit register representing the module
    mod_bin: string depicting the module in binary
    c: n-qubit ancilla register
    t: ancilla qubit
    """
    # Perform modular addition
    circuit = addmodN(circuit, a, b, N, mod_bin, c, t)

    # Then swap the results
    for i in range(len(a)):
        circuit.swap(a[i], b[i])

    return circuit

def c_fibmodN(n, mod_bin, power):
    """Controlled Fibonacci sequence by mod N"""


    a = QuantumRegister(n,'a')
    b = QuantumRegister(n+1,'b')
    N = AncillaRegister(n,'N')
    c = AncillaRegister(n,'c')
    t = AncillaRegister(1,'t')
    circuit = QuantumCircuit(a, b, N, c, t)

    for i, qubit in enumerate(mod_bin):
        if int(qubit) == 1:
            circuit.x(N[i])

    for iteration in range(power):
        circuit = fibmodN(circuit, a, b, N, mod_bin, c, t)

    # Undo the ancilla register N
    for i, qubit in enumerate(mod_bin):
        if int(qubit) == 1:
            circuit.x(N[i])

    # Convert the circuit that includes only operations on registers a, b, N, c, t to a gate
    fibmodN_gate = circuit.to_gate(label='Fib mod N')
    
    c_fibmodN = fibmodN_gate.control()

    return c_fibmodN

