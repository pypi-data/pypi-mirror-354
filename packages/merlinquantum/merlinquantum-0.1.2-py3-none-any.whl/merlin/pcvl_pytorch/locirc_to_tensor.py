# MIT License
#
# Copyright (c) 2025 Quandela
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from collections import defaultdict

import torch
import random

from multipledispatch import dispatch
from perceval.components import Circuit, AComponent, PS, BS, PERM, Unitary, Barrier, BSConvention

SUPPORTED_COMPONENTS = (PS, BS, PERM, Unitary, Barrier)


class CircuitConverter:
    """
    Convert a parameterized Perceval circuit into a differentiable PyTorch unitary matrix.
    Supports batch processing if "input_params" is a 2D tensor.

    """

    def __init__(self, circuit: Circuit, input_specs: list[str] = None, dtype: torch.dtype = torch.complex64, device: torch.device = torch.device('cpu')):
        """
        Initializes the CircuitConverter with a Perceval circuit.

        :param circuit: a parametrized Perceval Circuit object
        :param input_specs: List of parameter specs (names/prefixes), if ommited, we will expect a single tensor
        :param dtype: The data type to use for the tensors - one can specify either a float or complex dtype.
        """

        # device is the device where the tensors will be allocated, default is set with torch.device('xxx')
        # in pytorch module, there is no discovery of the device from parameters, so it is the user's responsibility to
        # set the device, with .to() before calling the generation function
        self.device = device
        self.input_params = None
        self.batch_size = 1

        self.set_dtype(dtype)

        assert isinstance(circuit, Circuit), f"Expected a Perceval LO circuit, but got {type(circuit).__name__}"
        self.circuit = circuit

        # Create parameter mapping - it will map parameter names to their index in the input tensors
        self.param_mapping = {}
        self.spec_mappings = {} # Track the mapping of input specs to parameter names

        self.nb_input_tensor = input_specs and len(input_specs) or 0
        param_names = [p.name for p in circuit.get_parameters()]

        if input_specs is None:
            self.param_mapping = {p.name: (0, idx) for idx, p in enumerate(self.circuit.get_parameters())}
        else:
            # Now create the mappings for parameters
            for i, spec in enumerate(input_specs):
                matching_params = [p for p in param_names if p.startswith(spec)]
                self.spec_mappings[spec] = matching_params

                if not matching_params:
                    raise ValueError(f"No parameters found matching the input spec '{spec}'.")
                for j, param in enumerate(matching_params):
                    self.param_mapping[param] = (i, j)

            # Check if all parameters are covered
            for param in param_names:
                if param not in self.param_mapping:
                    raise ValueError(f"Parameter '{param}' not covered by any input spec")

        self.list_rct = self._compile_circuit()

    def set_dtype(self, dtype: torch.dtype):
        if dtype == torch.float32 or dtype == torch.complex64:
            self.tensor_fdtype = torch.float32
            self.tensor_cdtype = torch.complex64
        elif dtype == torch.float64 or dtype == torch.complex128:
            self.tensor_fdtype = torch.float64
            self.tensor_cdtype = torch.complex128
        else:
            raise TypeError(f"Unsupported dtype {dtype}. Supported dtypes are torch.float32, torch.float64, "
                            f"torch.complex64, and torch.complex128.")

    def to(self, dtype: torch.dtype, device: str | torch.device):
        """
        Moves the converter to a specific device.

        :param dtype: The data type to use for the tensors - one can specify either a float or complex dtype.
                      Supported dtypes are torch.float32 or torch.complex64, torch.float64 or torch.complex128.
        :param device: The device to move the converter to.
        """
        if isinstance(device, str):
            self.device = torch.device(device)
        elif isinstance(device, torch.device):
            self.device = device
        else:
            raise TypeError(f"Expected a string or torch.device, but got {type(device).__name__}")
        if dtype not in (torch.float32, torch.float64, torch.complex64, torch.complex128):
            raise TypeError(f"Unsupported dtype {dtype}. Supported dtypes are torch.float32, torch.float64, "
                            f"torch.complex64, and torch.complex128.")

        self.set_dtype(dtype)

        for idx, (r, c) in enumerate(self.list_rct):
            if isinstance(c, torch.Tensor):
                self.list_rct[idx] = (r, c.to(dtype=self.tensor_cdtype, device=self.device))

        return self

    def _compile_circuit(self):
        """
        Precompile the circuit to remove barriers and merge blocks without parameters
        """

        # we are building a list of components or precompiled tensors or dimension (1, m, m)
        list_rct = []
        for r, c in self.circuit:
            if not isinstance(c, SUPPORTED_COMPONENTS):
                raise TypeError(f"{c} type not supported for conversion to PyTorch tensor.")
            if isinstance(c, Barrier):
                continue
            if not c.get_parameters(all_params=False):
                # we can already compute the tensor for this component
                curr_comp_tensor = self._compute_tensor(c)
                list_rct.append((r, curr_comp_tensor))
            else:
                list_rct.append((r, c))

        # in second pass, we will be fusing the adjacent numeric components together
        for idx, (r, ct) in enumerate(list_rct):
            if ct is None:
                # this component has been merged with a previous one, skip it
                continue
            if isinstance(ct, torch.Tensor):
                # let us check all the following components that could be merged with this one
                merge_group = [(r, ct)]
                min_group = r[0]
                max_group = r[-1]
                blocked_modes = set()
                for j in range(idx + 1, len(list_rct)):
                    r2, c2 = list_rct[j]
                    if c2 is None:
                        continue
                    if not isinstance(c2, torch.Tensor) or any(mode in blocked_modes for mode in r2):
                        for ir in r2:
                            blocked_modes.add(ir)
                        if len(blocked_modes) == self.circuit.m:
                            # all modes are blocked, we cannot merge anymore
                            break
                    else:
                        # we can merge this component with the previous one
                        merge_group.append((r2, c2))
                        if r2[0] < min_group:
                            min_group = r2[0]
                        if r2[-1] > max_group:
                            max_group = r2[-1]
                        # remove the component from the list
                        list_rct[j] = (r2, None)
                if len(merge_group) > 1:
                    # we have a group of components that can be merged
                    # we will compute the tensor for the whole group
                    merged_tensor = torch.eye(max_group-min_group+1, dtype=self.tensor_cdtype, device=self.device)
                    for r, c in merge_group:
                        c = c.to(self.device)
                        merged_tensor[r[0]-min_group:(r[-1]-min_group+1), :] = c @ merged_tensor[r[0]-min_group:(r[-1]-min_group+1), :]
                    list_rct[idx] = (range(min_group, max_group+1), merged_tensor)

        # Remove None entries from the list
        return [item for item in list_rct if item[1] is not None]

    def to_tensor(self, *input_params: torch.Tensor,
                  batch_size: int = None) -> torch.Tensor:
        """
        Converts a parameterized Perceval circuit to a PyTorch unitary tensor.

        :param *input_params: Pytorch list of tensors of shape (num_params,) or (batch_size, num_params),
                             representing parameters as defined by input_specs and indexed by param_mapping.
        :param batch_size: The batch size for the input parameters. If none, it is discovered from the input_params.
                           by default, it is set to 1.

        returns: The complex-valued converted Pytorch tensor of shape (circuit.m, circuit.m)
        or (batch_size, circuit.m, circuit.m).
        """
        if len(input_params) == 1 and isinstance(input_params[0], list):
            input_params = input_params[0]
        if len(input_params) != self.nb_input_tensor:
            raise ValueError(f"Expected {self.nb_input_tensor} input tensors, but got {len(input_params)}.")
        if not isinstance(input_params, list) and not isinstance(input_params, tuple):
            raise TypeError(f"Expected a list of input tensors, but got {type(input_params).__name__}.")

        self.torch_params = input_params

        if batch_size is None:
            if input_params and input_params[0].dim() > 1:
                has_batch = True
                batch_size = input_params[0].shape[0]
            else:
                has_batch = False
                batch_size = 1
        else:
            has_batch = True
        self.batch_size = batch_size

        converted_tensor = torch.eye(self.circuit.m,
                                     dtype=self.tensor_cdtype,
                                     device=self.device).unsqueeze(0).repeat(batch_size, 1, 1)
        # Build unitary tensor by composing component unitaries
        for r, c in self.list_rct:
            if isinstance(c, torch.Tensor):
                # If the component is already a tensor, use it directly, just move it to the correct device and dtype
                # and expand it to the batch size
                curr_comp_tensor = c.to(dtype=self.tensor_cdtype, device=self.device).expand(batch_size, -1, -1)
            else:
                curr_comp_tensor = self._compute_tensor(c)

            # Compose unitaries
            contribution = converted_tensor[..., r[0]:(r[-1] + 1), :].clone()
            converted_tensor[..., r[0]:(r[-1] + 1), :] = curr_comp_tensor @ contribution.to(curr_comp_tensor.device)

        if not has_batch:
            # If no batch dimension was provided, remove the batch dimension
            converted_tensor = converted_tensor.squeeze(0)

        return converted_tensor

    @dispatch((Unitary, PERM))
    def _compute_tensor(self, comp: AComponent) -> torch.Tensor:
        # Both PERM and a generic Unitary component has no parameters
        return torch.tensor(comp.compute_unitary(),
                            dtype=self.tensor_cdtype, device=self.device).unsqueeze(0).expand(self.batch_size, -1, -1)

    @dispatch(BS)
    def _compute_tensor(self, comp: AComponent) -> torch.Tensor:
        param_values = []

        for index, param in enumerate(comp.get_parameters(all_params=True)):
            if param.is_variable:
                (tensor_id, idx_in_tensor) = self.param_mapping[param.name]
                param_values.append(self.torch_params[tensor_id][..., idx_in_tensor])
            else:
                param_values.append(torch.tensor(float(param), dtype=self.tensor_fdtype, device=self.device))

        cos_theta = torch.cos(param_values[0] / 2)
        sin_theta = torch.sin(param_values[0] / 2)
        phi_tl_tr = param_values[1] + param_values[3]  # phi_tl_val + phi_tr_val
        u00_mul = torch.cos(phi_tl_tr) + 1j * torch.sin(phi_tl_tr)

        phi_tr_bl = param_values[3] + param_values[2]  # phi_tr_val + phi_bl_val
        u01_mul = torch.cos(phi_tr_bl) + 1j * torch.sin(phi_tr_bl)

        phi_tl_br = param_values[1] + param_values[4]  # phi_tl_val + phi_br_val
        u10_mul = torch.cos(phi_tl_br) + 1j * torch.sin(phi_tl_br)

        phi_bl_br = param_values[2] + param_values[4]  # phi_bl_val + phi_br_val
        u11_mul = torch.cos(phi_bl_br) + 1j * torch.sin(phi_bl_br)

        bs_convention = comp._convention
        if bs_convention == BSConvention.Rx:
            unitary_tensor = torch.tensor([[1, 1j], [1j, 1]], dtype=self.tensor_cdtype, device=self.device)
        elif bs_convention == BSConvention.Ry:
            unitary_tensor = torch.tensor([[1, -1], [1, 1]], dtype=self.tensor_cdtype, device=self.device)
        elif bs_convention == BSConvention.H:
            unitary_tensor = torch.tensor([[1, 1], [1, -1]], dtype=self.tensor_cdtype, device=self.device)
        else:
            raise NotImplementedError(f'BS convention : {comp._convention.name} not supported.')

        unitary_tensor = unitary_tensor.unsqueeze(0).repeat(self.batch_size, 1, 1).to(cos_theta.device)
        unitary_tensor[..., 0, 0] *= u00_mul.to(self.device) * cos_theta
        unitary_tensor[..., 0, 1] *= u01_mul.to(self.device) * sin_theta
        unitary_tensor[..., 1, 1] *= u11_mul.to(self.device) * cos_theta
        unitary_tensor[..., 1, 0] *= u10_mul.to(self.device) * sin_theta
        return unitary_tensor

    @dispatch(PS)
    def _compute_tensor(self, comp: AComponent) -> torch.Tensor:
        if comp.param("phi").is_variable:
            (tensor_id, idx_in_tensor) = self.param_mapping[comp.param("phi").name]
            phase = self.torch_params[tensor_id][..., idx_in_tensor]
        else:
            phase = torch.tensor(comp.param("phi")._value, dtype=self.tensor_fdtype, device=self.device)

        if comp._max_error:
            err = float(comp._max_error) * random.uniform(-1, 1)
            phase += err

        unitary_tensor = torch.exp(1j * phase).reshape(-1, 1) # reshape so that in any case, we have 2 dim
        return unitary_tensor.unsqueeze(-1)  # to change shape of tensor to (b, 1, 1)

