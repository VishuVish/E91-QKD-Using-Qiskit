#E91 QKD Protocol

import random
import numpy as np
import math as math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

with open("bits_for_E91.txt", "r") as f:
    bits = f.read().strip()

def run_E91(N, bits):
    
    circuit = []

    for i in range(N):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0,1)

        alice_angles = [0, math.pi/4, math.pi/2]
        bob_angles = [math.pi/8, 3*math.pi/8, 5*math.pi/8]

        alice_index = int(bits[4*i:4*i+2], 2) % 3
        bob_index = int(bits[4*i+2:4*i+4], 2) % 3

        alice_choices = alice_angles[alice_index]
        bob_choices = bob_angles[bob_index] 
    
        qc.ry(-2 * alice_choices, 0)
        qc.ry(-2 * bob_choices, 1)
    
        qc.measure(0, 0)
        qc.measure(1, 1)
    
        circuit.append(qc)
    
    sim = AerSimulator()
    tc = transpile(circuit, sim)

    job  = sim.run(tc, shots=10)
    results = job.result()

# Processing results to calculate correlations
    def bit_to_pm1(bit):
        return 1 if bit == '0' else -1

    correlation = []
    for i in range(N):
        counts = results.get_counts(i)
        total = sum(counts.values())
        ab_sum = 0
        for outcome, count in counts.items():
            a_bit = bit_to_pm1(outcome[0])
            b_bit = bit_to_pm1(outcome[1])
            ab_sum += a_bit * b_bit * count       
        correlation.append(ab_sum/ total)

# Extracting key bits and calculating CHSH S value
    key_bits = []
    test_bits = []
    raw_key = []

    for i in range(N):
        alice_index = int(bits[4*i:4*i+2], 2) % 3
        bob_index   = int(bits[4*i+2:4*i+4], 2) % 3
    
        if alice_index == bob_index:
            counts = results.get_counts(i)
            most_com = max(counts.items(), key= lambda x: x[1])[0]
            raw_key.append(most_com[1]) 
    
        test_bits.append((correlation[i], alice_index, bob_index))
    
        if alice_index == bob_index:
            key_bits.append(correlation[i])
              
    print(f"Key bits: {len(key_bits)}, total bits: {len(test_bits)}")
    
    def E(ax, by): 
        pairs = [corr for corr, ai, bi in test_bits if ai == ax and bi == by]
        return sum(pairs) / len(pairs) if pairs else 0

    E00 = E(0, 0)
    E01 = E(0, 1)
    E10 = E(1, 0)
    E11 = E(1, 1)

    S = E00 - E01 + E10 + E11
    return S, results

# Plotting the CHSH S values for different numbers of qubits
num_qubits = [5, 10, 100, 250, 500, 1000, 5000, 10000]
s_val = []

for N in num_qubits:
    bits = ''.join(random.choice('01') for _ in range(4 * N))
    S, results = run_E91(N, bits)
    s_val.append(S)
    
plt.plot(num_qubits, s_val, marker='o')
plt.xlabel('Number of Bits')
plt.ylabel('CHSH S Values')
plt.title('CHSH Test S Values Calculated vs. Number of Bits in E91 Protocol')
plt.axhline(y=2, color='r', linestyle='--', label='Classical limit')
plt.axhline(y=2*np.sqrt(2), color='g', linestyle='--', label='Quantum Limit (2√2)')
plt.grid(True)
plt.legend()
plt.show()

#QBER Estimation (this entire part could be nested inside the run_E91 function)

N = 10000 #This could be adjusted
alice_bits = []
bob_bits = []
alice_bases = []
bob_bases = []
for i in range (N):
    counts = results.get_counts(i)
    most_common = max(counts.items(), key=lambda x: x[1])[0]
    alice_bits.append(int(most_common[0]))  # qubit 1
    bob_bits.append(int(most_common[1]))    # qubit 0

    alice_index = int(bits[4*i:4*i+2], 2) % 3
    bob_index   = int(bits[4*i+2:4*i+4], 2) % 3
    alice_bases.append(alice_index)
    bob_bases.append(bob_index)

matching_indices = [i for i in range(N) if alice_bases[i] == bob_bases[i]]
mismatches = sum(alice_bits[i] != bob_bits[i] for i in matching_indices)
qber = mismatches / len(matching_indices) if matching_indices else 0
print(f"Estimated QBER for {N} bits: {qber:.4f}")