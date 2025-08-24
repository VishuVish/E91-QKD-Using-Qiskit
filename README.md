# E91 Quantum Key Distribution  

This project is a **Demonstration of the Ekert91 (E91) QKD protocol** implemented in Qiskit.  

In this project as well, just like [BB84](https://github.com/VishuVish/A_BB84_sim_using_Qiskit), the random bitstream used here are **not** from built-in pseudorandom generators.  
It is sourced from my project, [Chaos2Crypto](https://github.com/VishuVish/Chaos2Crypto-FFT-Based-Random-Number-Generator),  
where I developed an FFT-based random number generator with bias correction and cryptographic extraction.  

---

## What this project demonstrates
- **Entangled Bell pairs** are generated and distributed between Alice and Bob.  
- **Alice and Bob** randomly choose one of three measurement bases.
-  The randomness comes from the cryptographically secure bits in `bits_for_E91.txt` generated using [Chaos2Cryto](https://github.com/VishuVish/Chaos2Crypto-FFT-Based-Random-Number-Generator) Code. 
- A subset of results is used to compute the **CHSH correlation parameter (S-value):**   
- When Alice and Bob’s **bases match**, the results are used to form the **raw secret key**.  
- The **Quantum Bit Error Rate (QBER)** is estimated to detect noise or eavesdropping.  

---

##  Simulator Limitations
- Implemented with Qiskit’s `AerSimulator`.  
- Each Bell pair is simulated in its own circuit.  
- Runtime grows with the number of entangled pairs.  
- For sufficiently large \(N\), the CHSH test converges toward the expected quantum bound.  

---

##  Example Results
- **CHSH S-value:** typically ~2.8 (well above the classical bound of 2).  
- **QBER:** a few percent in ideal simulation, depending on random choices.  

---

Feel free to clone, modify, and extend this project!  
*(Ideas: add explicit noise models, simulate an eavesdropper, or extend key distillation with error correction.)*  
