"""
Experiment configuration for quantum layer setups.
"""

from ..core.generators import CircuitType, StatePattern


class PhotonicBackend:
    """Configuration container for quantum layer experiments."""

    def __init__(self, circuit_type: CircuitType, n_modes: int, n_photons: int,
                 state_pattern: StatePattern = StatePattern.PERIODIC,
                 use_bandwidth_tuning: bool = False, reservoir_mode: bool = False):

        # Validate circuit_type
        if isinstance(circuit_type, str):
            try:
                circuit_type = CircuitType(circuit_type.lower())
            except ValueError:
                raise ValueError(f"Invalid circuit_type: {circuit_type}. "
                                 f"Valid options are: {[e.value for e in CircuitType]}")
        elif not isinstance(circuit_type, CircuitType):
            raise TypeError(f"circuit_type must be CircuitType enum or string, got {type(circuit_type)}")

        # Validate n_modes
        if not isinstance(n_modes, int) or n_modes <= 0:
            raise ValueError(f"n_modes must be a positive integer, got {n_modes}")

        # Validate n_photons
        if not isinstance(n_photons, int) or n_photons < 0:
            raise ValueError(f"n_photons must be a non-negative integer, got {n_photons}")

        if n_photons > n_modes:
            raise ValueError(f"Cannot place {n_photons} photons into {n_modes} modes")

        # Validate state_pattern
        if isinstance(state_pattern, str):
            try:
                state_pattern = StatePattern(state_pattern.lower())
            except ValueError:
                raise ValueError(f"Invalid state_pattern: {state_pattern}. "
                                 f"Valid options are: {[e.value for e in StatePattern]}")
        elif not isinstance(state_pattern, StatePattern):
            raise TypeError(f"state_pattern must be StatePattern enum or string, got {type(state_pattern)}")

        self.circuit_type = circuit_type
        self.n_modes = n_modes
        self.n_photons = n_photons
        self.state_pattern = state_pattern
        self.use_bandwidth_tuning = use_bandwidth_tuning
        self.reservoir_mode = reservoir_mode