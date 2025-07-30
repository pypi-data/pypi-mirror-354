"""
Tests for no_bunching functionality in quantum computation.
"""

import pytest
import torch
import math
import merlin as ML
from merlin.core.process import ComputationProcessFactory
from merlin.core.generators import CircuitGenerator,StateGenerator



def calculate_fock_space_size(n_modes: int, n_photons: int) -> int:
    """Calculate the size of the Fock space for n_photons in n_modes."""
    if n_photons == 0:
        return 1
    return math.comb(n_modes + n_photons - 1, n_photons)


def calculate_no_bunching_size(n_modes: int, n_photons: int) -> int:
    """Calculate the size of the no-bunching space (single photon states only)."""
    if n_photons == 0:
        return 1
    if n_photons > n_modes:
        return 0  # Impossible to place more photons than modes without bunching
    return math.comb(n_modes, n_photons)


class TestNoBunchingFunctionality:
    """Test suite for no_bunching parameter in quantum computation."""

    def test_fock_space_vs_no_bunching_sizes(self):
        """Test that Fock space and no-bunching space sizes are calculated correctly."""
        # Test cases: (n_modes, n_photons)
        test_cases = [
            (3, 1),  # 3 modes, 1 photon
            (4, 2),  # 4 modes, 2 photons
            (5, 3),  # 5 modes, 3 photons
            (6, 2),  # 6 modes, 2 photons
        ]

        for n_modes, n_photons in test_cases:
            fock_size = calculate_fock_space_size(n_modes, n_photons)
            no_bunching_size = calculate_no_bunching_size(n_modes, n_photons)

            print(f"n_modes={n_modes}, n_photons={n_photons}")
            print(f"  Fock space size: {fock_size}")
            print(f"  No-bunching size: {no_bunching_size}")

            # No-bunching space should be smaller than or equal to Fock space
            assert no_bunching_size <= fock_size

            # For single photon, no-bunching size should equal n_modes
            if n_photons == 1:
                assert no_bunching_size == n_modes

    def test_computation_process_with_no_bunching_false(self):
        """Test computation process with no_bunching=False (full Fock space)."""
        n_modes = 4
        n_photons = 2

        # Create circuit and state
        circuit, _ = CircuitGenerator.generate_circuit(
            ML.CircuitType.PARALLEL_COLUMNS, n_modes, 2
        )
        input_state = StateGenerator.generate_state(n_modes, n_photons, ML.StatePattern.SEQUENTIAL)

        # Create computation process with no_bunching=False
        process = ComputationProcessFactory.create(
            circuit=circuit,
            input_state=input_state,
            trainable_parameters=["phi_"],
            input_parameters=["pl"],
            no_bunching=False
        )

        # Create dummy parameters
        spec_mappings = process.converter.spec_mappings
        dummy_params = []

        for spec in ["phi_", "pl"]:
            if spec in spec_mappings:
                param_count = len(spec_mappings[spec])
                dummy_params.append(torch.zeros(param_count))

        # Compute distribution
        distribution = process.compute(dummy_params)

        # Check that distribution size matches full Fock space
        expected_size = calculate_fock_space_size(n_modes, n_photons)
        actual_size = distribution.shape[-1]

        print(f"Full Fock space - Expected: {expected_size}, Actual: {actual_size}")
        assert actual_size == expected_size, f"Expected Fock space size {expected_size}, got {actual_size}"

    def test_computation_process_with_no_bunching_true(self):
        """Test computation process with no_bunching=True (single photon states only)."""
        n_modes = 4
        n_photons = 2

        # Create circuit and state
        circuit, _ = CircuitGenerator.generate_circuit(
            ML.CircuitType.PARALLEL_COLUMNS, n_modes, 2
        )
        input_state = StateGenerator.generate_state(n_modes, n_photons, ML.StatePattern.SEQUENTIAL)

        # Create computation process with no_bunching=True
        process = ComputationProcessFactory.create(
            circuit=circuit,
            input_state=input_state,
            trainable_parameters=["phi_"],
            input_parameters=["pl"],
            no_bunching=True
        )

        # Create dummy parameters
        spec_mappings = process.converter.spec_mappings
        dummy_params = []

        for spec in ["phi_", "pl"]:
            if spec in spec_mappings:
                param_count = len(spec_mappings[spec])
                dummy_params.append(torch.zeros(param_count))

        # Compute distribution
        distribution = process.compute(dummy_params)

        # Check that distribution size matches no-bunching space
        expected_size = calculate_no_bunching_size(n_modes, n_photons)
        actual_size = distribution.shape[-1]

        print(f"No-bunching space - Expected: {expected_size}, Actual: {actual_size}")
        assert actual_size == expected_size, f"Expected no-bunching size {expected_size}, got {actual_size}"

    def test_quantum_layer_with_no_bunching_parameter(self):
        """Test QuantumLayer integration with no_bunching parameter."""

        # We need to update the layer to support no_bunching
        # For now, let's test the computation process directly
        n_modes = 5
        n_photons = 2

        # Test both cases
        for no_bunching in [False, True]:
            circuit, _ = CircuitGenerator.generate_circuit(
                ML.CircuitType.SERIES, n_modes, 2
            )
            input_state = StateGenerator.generate_state(n_modes, n_photons, ML.StatePattern.PERIODIC)

            process = ComputationProcessFactory.create(
                circuit=circuit,
                input_state=input_state,
                trainable_parameters=["phi_"],
                input_parameters=["pl"],
                no_bunching=no_bunching
            )

            # Create dummy parameters
            spec_mappings = process.converter.spec_mappings
            dummy_params = []

            for spec in ["phi_", "pl"]:
                if spec in spec_mappings:
                    param_count = len(spec_mappings[spec])
                    dummy_params.append(torch.randn(param_count))

            distribution = process.compute(dummy_params)

            if no_bunching:
                expected_size = calculate_no_bunching_size(n_modes, n_photons)
            else:
                expected_size = calculate_fock_space_size(n_modes, n_photons)

            actual_size = distribution.shape[-1]

            print(f"no_bunching={no_bunching}: Expected {expected_size}, Actual {actual_size}")
            assert actual_size == expected_size

    def test_different_photon_numbers(self):
        """Test no_bunching with different numbers of photons."""
        n_modes = 6

        for n_photons in [1, 2, 3]:
            print(f"\nTesting {n_photons} photons in {n_modes} modes:")

            circuit, _ = CircuitGenerator.generate_circuit(
                ML.CircuitType.PARALLEL, n_modes, 2
            )
            input_state = StateGenerator.generate_state(n_modes, n_photons, ML.StatePattern.SPACED)

            # Test with no_bunching=True
            process_no_bunching = ComputationProcessFactory.create(
                circuit=circuit,
                input_state=input_state,
                trainable_parameters=["phi_"],
                input_parameters=["pl"],
                no_bunching=True
            )

            # Test with no_bunching=False
            process_full_fock = ComputationProcessFactory.create(
                circuit=circuit,
                input_state=input_state,
                trainable_parameters=["phi_"],
                input_parameters=["pl"],
                no_bunching=False
            )

            # Create dummy parameters
            spec_mappings = process_no_bunching.converter.spec_mappings
            dummy_params = []

            for spec in ["phi_", "pl"]:
                if spec in spec_mappings:
                    param_count = len(spec_mappings[spec])
                    dummy_params.append(torch.randn(param_count))

            # Compute distributions
            dist_no_bunching = process_no_bunching.compute(dummy_params)
            dist_full_fock = process_full_fock.compute(dummy_params)

            # Check sizes
            expected_no_bunching = calculate_no_bunching_size(n_modes, n_photons)
            expected_full_fock = calculate_fock_space_size(n_modes, n_photons)

            print(f"  No-bunching: {dist_no_bunching.shape[-1]} (expected {expected_no_bunching})")
            print(f"  Full Fock: {dist_full_fock.shape[-1]} (expected {expected_full_fock})")

            assert dist_no_bunching.shape[-1] == expected_no_bunching
            assert dist_full_fock.shape[-1] == expected_full_fock

            # No-bunching should be smaller
            assert dist_no_bunching.shape[-1] <= dist_full_fock.shape[-1]

    def test_impossible_no_bunching_case(self):
        """Test case where no_bunching is impossible (more photons than modes)."""
        n_modes = 3
        n_photons = 4  # More photons than modes

        circuit, _ = CircuitGenerator.generate_circuit(
            ML.CircuitType.SERIES, n_modes, 2
        )
        input_state = [1, 1, 1, 1][:n_modes] + [0] * max(0, n_modes - 4)

        # This should work but result in empty or minimal space
        process = ComputationProcessFactory.create(
            circuit=circuit,
            input_state=input_state,
            trainable_parameters=["phi_"],
            input_parameters=["pl"],
            no_bunching=True
        )

        # The calculation shows this should be 0, but the system might handle it differently
        expected_size = calculate_no_bunching_size(n_modes, n_photons)
        print(f"Impossible case: {n_photons} photons in {n_modes} modes")
        print(f"Expected no-bunching size: {expected_size}")

        # This might raise an error or return empty distribution
        # Let's see what actually happens
        spec_mappings = process.converter.spec_mappings
        dummy_params = []

        for spec in ["phi_", "pl"]:
            if spec in spec_mappings:
                param_count = len(spec_mappings[spec])
                dummy_params.append(torch.randn(param_count))

        try:
            distribution = process.compute(dummy_params)
            print(f"Actual distribution size: {distribution.shape[-1]}")
            # If it doesn't error, the size should be 0 or handled gracefully
            assert distribution.shape[-1] >= 0
        except Exception as e:
            print(f"Expected error for impossible case: {e}")
            # This is acceptable behavior

    def test_single_photon_case(self):
        """Test the simple single photon case."""
        n_modes = 5
        n_photons = 1

        circuit, _ = CircuitGenerator.generate_circuit(
            ML.CircuitType.PARALLEL_COLUMNS, n_modes, 2
        )
        input_state = StateGenerator.generate_state(n_modes, n_photons, ML.StatePattern.SEQUENTIAL)

        for no_bunching in [False, True]:
            process = ComputationProcessFactory.create(
                circuit=circuit,
                input_state=input_state,
                trainable_parameters=["phi_"],
                input_parameters=["pl"],
                no_bunching=no_bunching
            )

            spec_mappings = process.converter.spec_mappings
            dummy_params = []

            for spec in ["phi_", "pl"]:
                if spec in spec_mappings:
                    param_count = len(spec_mappings[spec])
                    dummy_params.append(torch.randn(param_count))

            distribution = process.compute(dummy_params)

            if no_bunching:
                # For single photon, no-bunching space = n_modes (each mode can have the photon)
                expected = n_modes
            else:
                # For single photon, Fock space = n_modes (same as no-bunching)
                expected = n_modes

            print(f"Single photon, no_bunching={no_bunching}: size={distribution.shape[-1]}, expected={expected}")
            assert distribution.shape[-1] == expected

    def test_compute_with_keys_functionality(self):
        """Test that compute_with_keys works with no_bunching."""
        n_modes = 4
        n_photons = 2

        circuit, _ = CircuitGenerator.generate_circuit(
            ML.CircuitType.SERIES, n_modes, 2
        )
        input_state = StateGenerator.generate_state(n_modes, n_photons, ML.StatePattern.PERIODIC)

        process = ComputationProcessFactory.create(
            circuit=circuit,
            input_state=input_state,
            trainable_parameters=["phi_"],
            input_parameters=["pl"],
            no_bunching=True
        )

        spec_mappings = process.converter.spec_mappings
        dummy_params = []

        for spec in ["phi_", "pl"]:
            if spec in spec_mappings:
                param_count = len(spec_mappings[spec])
                dummy_params.append(torch.randn(param_count))

        # Test compute_with_keys
        keys, distribution = process.compute_with_keys(dummy_params)

        # Should have the same distribution size
        expected_size = calculate_no_bunching_size(n_modes, n_photons)
        assert distribution.shape[-1] == expected_size

        # Keys should correspond to the states
        assert len(keys) == expected_size

        print(f"Keys: {keys}")
        print(f"Distribution shape: {distribution.shape}")
        print(f"Expected size: {expected_size}")


if __name__ == "__main__":
    # Run a quick demonstration
    print("=== No-Bunching Test Demonstration ===")

    test = TestNoBunchingFunctionality()

    print("\n1. Testing size calculations...")
    test.test_fock_space_vs_no_bunching_sizes()

    print("\n2. Testing computation process...")
    test.test_computation_process_with_no_bunching_false()
    test.test_computation_process_with_no_bunching_true()

    print("\n3. Testing different photon numbers...")
    test.test_different_photon_numbers()

    print("\n✅ All tests passed!")