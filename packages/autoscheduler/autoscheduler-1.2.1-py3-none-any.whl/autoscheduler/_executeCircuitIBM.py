"""
Module containing IBM execution functions
"""
from qiskit import transpile, QuantumCircuit
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
from qiskit_aer import AerSimulator

def _runIBM(machine:str, circuit:QuantumCircuit, shots:int) -> dict:
    """
    Executes a circuit in the IBM cloud.

    Args:
        machine (str): The machine to execute the circuit.
        circuit (qiskit.QuantumCircuit): The circuit to execute.
        shots (int): The number of shots to execute the circuit.
    
    Returns:
        dict: The results of the circuit execution.
    """
    if machine == "local":
        backend = AerSimulator()
        x = int(shots)
        job = backend.run(circuit, shots=x)
        result = job.result()
        counts = result.get_counts()
        return counts
    else:
        # Load your IBM Quantum account
        service = QiskitRuntimeService()
        backend = service.backend(machine)
        sampler = Sampler(mode=backend)
        qc_basis = transpile(circuit, backend)
        x = int(shots)
        job = sampler.run([qc_basis], shots=x)
        result = job.result()
        counts = result[0].data.creg_c.get_counts()
        return counts

def _get_qubits_machine_ibm(machine:str) -> int:
    """
    Gets the number of qubits of an IBM machine.

    Args:
        machine (str): The machine to get the number of qubits from.
    
    Returns:
        int: The number of qubits of the machine.

    Raises:
        ValueError: If the machine is not available on the IBM account.
    """
    if machine == 'local':
        backend = AerSimulator()
    else:
        service = QiskitRuntimeService()
        available_backends = service.backends()
        available_backends_names = [backend.name for backend in available_backends]
        if machine not in available_backends_names:
            raise ValueError(f"Machine {machine} not available.")
        backend = service.backend(machine)
    return backend.configuration().n_qubits
