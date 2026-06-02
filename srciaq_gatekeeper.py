# MÓDULO 2: NÚCLEO IAQ - GATEKEEPER DE ALTA DISPONIBILIDAD
import json
import os
import sys
from qiskit import QuantumCircuit, execute, Aer

class QuantumFluidGatekeeper:
    def __init__(self):
        self.vector_file = "tmp/qse_fluid_tensor.json"
        self.fluidity_threshold = 0.88

    def execute_connection(self):
        if not os.path.exists(self.vector_file):
            print("[-] Error: Ejecute el Oráculo primero.")
            sys.exit(1)
            
        with open(self.vector_file, "r") as f:
            data = json.load(f)

        qc = QuantumCircuit(3, 3)
        qc.h([0, 1, 2])
        qc.u(data['theta'], data['phi'], data['lam'], 0)
        qc.measure([0, 1, 2], [0, 1, 2])
        
        simulator = Aer.get_backend('qasm_simulator')
        counts = execute(qc, simulator, shots=1000).result().get_counts()
        
        fluidity = (counts.get('000', 0) + counts.get('111', 0)) / 1000
        
        if fluidity >= self.fluidity_threshold:
            print(f"[+++] CONEXIÓN APROBADA: {fluidity*100:.1f}%.")
        else:
            print(f"[-] CONEXIÓN DENEGADA: {fluidity*100:.1f}%.")

if __name__ == "__main__":
    iaq = QuantumFluidGatekeeper()
    iaq.execute_connection()