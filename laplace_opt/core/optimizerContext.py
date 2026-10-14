# libraries
from dataclasses import dataclass
from typing import Sequence

from laplace_log import log
import torch
from botorch.utils.transforms import normalize


@dataclass
class Observation:
    '''
    Represents a single evaluation result.

    Attributes:
        x (torch.Tensor): 
            Input vector for the evaluation.
        y (torch.Tensor):
            Corresponding objective values.
        shot_number (int):
            Corresponding shot.
    '''
    x: torch.Tensor    # shape [d]
    y: torch.Tensor    # shape [n_obj]
    shot_number: int


class OptimizationContext:
    '''
    Stores training data, bounds, and objectives for optimization.

    Provides methods to access baseline points and compute reference points
    for acquisition functions.
    '''
    def __init__(self, bounds, objectives: dict, inputs: dict):
        '''
        Initialize the optimization context with problem definition.

        Args:
            bounds (torch.Tensor):
                Bounds for each input variable.

            objectives (dict):
                Dictionary of objectives to optimize.
            
            inputs (dict):
                Dictionary of inputs to optimize
        '''
        self.bounds = bounds
        self.objectives = objectives
        self.inputs = inputs
        self.n_obj = len(self.objectives)
        self.n_inputs = len(self.inputs)
        self.n_init = -1
        self.step = 0
        
        self._observations: list[Observation] = []
        log.debug("Context created.")

    @property
    def Y_opt_space(self) -> torch.Tensor:
        '''Return the objectives in optimization space.'''
        return torch.stack([obs.y for obs in self._observations])

    @property
    def Y_physical(self) -> torch.Tensor:
        '''Return the objectives in physical space.'''
        Y = self.Y_opt_space
        Y_physical = self._to_physical(Y)
        return Y_physical

    @property
    def Y_opt(self) -> torch.Tensor:
        '''Return the objectives in the physical space made during the optimization phase.'''
        if self.n_init != -1:
            return self.Y_physical[self.n_init:]
        log.warning(f"The initialization is not set (n_init = {self.n_init}).\n" 
                    f"Returning objectives in physical space insteaded.")
        return self.Y_physical

    @property
    def Y_init(self) -> torch.Tensor:
        '''Return the objectives in the physical space made during the initialization phase.'''
        if self.n_init != -1:
            return self.Y_physical[:self.n_init]
        log.warning(f"The initialization is not set (n_init = {self.n_init}).\n" 
                    f"Returning objectives in physical space insteaded.")
        return self.Y_physical
    
    def _to_physical(self, Y_opt: torch.Tensor) -> torch.Tensor:
        '''Helper changing an objective tensor according to the min/max direction.'''
        Y_phys = Y_opt.clone()
        for i, obj in enumerate(self.objectives.values()):
            if obj.minimize:
                Y_phys[:, i] *= -1
        return Y_phys

    @property
    def shot_number_list(self) -> list[int]:
        '''Return the list of shot numbers.'''
        return [obs.shot_number for obs in self._observations]

    @property
    def X_physical(self) -> torch.Tensor:
        '''Return the inputs in physical space.'''
        X = torch.stack([obs.x for obs in self._observations])
        return X
    
    @property
    def X_normalized(self) -> torch.Tensor:
        '''Return the inputs in normalized space.'''
        return normalize(self.X_physical, self.bounds)
    
    @property
    def X_opt(self) -> torch.Tensor:
        '''Return the inputs in the physical space made during the optimization phase.'''
        if self.n_init != -1:
            return self.X_physical[self.n_init:]
        log.warning(f"The initialization is not set (n_init = {self.n_init}).\n" 
                    f"Returning inputs in physical space insteaded.")
        return self.X_physical
    
    @property
    def X_init(self) -> torch.Tensor:
        '''Return the inputs in the physical space made during the initialization phase.'''
        if self.n_init != -1:
            return self.X_physical[:self.n_init]
        log.warning(f"The initialization is not set (n_init = {self.n_init}).\n" 
                    f"Returning inputs in physical space insteaded.")
        return self.X_physical        

    def get_obj_state_dict(self) -> dict[str, dict[str, str | int | bool]]:
        '''Helper provinding the dictionary describing each objective.'''
        obj_state_dict = {}
        for key, obj in self.objectives.items():
            obj_state_dict[key] = obj.to_dict()
        return obj_state_dict
    
    def get_input_state_dict(self) -> dict[str, dict[str, str | int | Sequence[float]]]:
        '''Helper providing the dictionary describing each input.'''
        input_state_dict = {}
        for key, input in self.inputs.items():
            input_state_dict[key] = input.to_dict()
        return input_state_dict

    def add_observation(self, x: torch.Tensor, y: torch.Tensor, shot_number: int) -> None:
        '''
        Add a single observation to the context.

        Both the input x and output y must be given in physical space.
        
        This method will apply a transformation on y in order to save
        it in optimization space (taking the opposite if the objective
        must be minimized).

        Args:
            x (torch.Tensor): 
                Input vector of shape [d].
            y (torch.Tensor): 
                Corresponding objective values of shape [n_obj].
        '''
        y_corrected = y.clone()
        for i, obj in enumerate(self.objectives.values()):
            if obj.minimize:
                y_corrected[i] = -y_corrected[i]
        
        self._observations.append(
            Observation(
                x=x, 
                y=y_corrected, 
                shot_number=shot_number
                )
            )
        log.debug(f"Observation added: x={x.tolist()}," 
                  f"y={y_corrected.tolist()}," 
                  f"shot_number={shot_number}")


    def X_by_objective(self) -> list[torch.Tensor]:
        '''
        Get input tensors grouped by objective.

        Returns:
            list[torch.Tensor]: 
                List of tensors, one per objective, containing 
                the input vectors for valid observations.
        '''
        Xs = [[] for _ in range(self.n_obj)]

        for obs in self._observations:
            for i in range(self.n_obj):
                if not torch.isnan(obs.y[i]):
                    Xs[i].append(obs.x)

        return [
            torch.stack(x) if x else torch.empty(0, self.bounds.shape[1], dtype=torch.double)
            for x in Xs
        ]
    

    def Y_by_objective(self) -> list[torch.Tensor]:
        '''
        Get output tensors grouped by objective.
        (return the value in objective space)

        Returns:
            list[torch.Tensor]: 
                List of tensors, one per objective, containing 
                the corresponding objective values.        
        '''
        Ys = [[] for _ in range(self.n_obj)]

        for obs in self._observations:
            for i in range(self.n_obj):
                if not torch.isnan(obs.y[i]):
                    Ys[i].append(obs.y[i:i+1])

        return [
            torch.stack(y) if y else torch.empty(0, 1, dtype=torch.double)
            for y in Ys
        ]


    def get_X_baseline(self) -> torch.Tensor:
        '''
        Get all unique evaluated input points in physical space.

        Returns:
            torch.Tensor: 
                Concatenated and unique inputs across all observations.        
        '''
        return torch.unique(self.X_physical, dim=0)
    

    def get_X_baseline_normalized(self) -> torch.Tensor:
        '''
        Get all unique evaluated input points in normalized space.

        Returns:
            torch.Tensor: 
                Normalized unique input points.
        '''
        return normalize(self.get_X_baseline(), self.bounds)


    def get_ref_point(self) -> torch.Tensor:
        '''
        Compute a reference point for multi-objective optimization.

        The reference correspond to the **optimized space**.

        Returns:
            torch.Tensor: 
                Reference point vector of shape [n_obj].
        '''
        Y = self.Y_opt_space
        ref = Y.min(dim=0).values - 0.1 * Y.abs().max(dim=0).values
        return ref


    def get_ref_point_physical(self) -> torch.Tensor:
        '''
        Compute a reference point for multi-objective optimization.

        The reference correspond to the **physical space**.

        Returns:
            torch.Tensor: 
                Reference point vector of shape [n_obj].
        '''
        ref = self.get_ref_point()
        for i, obj in enumerate(self.objectives.values()):
            if obj.minimize:
                ref[i] *= -1
        return ref
    

    def compute_pareto_front(self, Y_opt: torch.Tensor) -> torch.Tensor:
        '''
        Compute the 2D Pareto front of the given Y tensor.

        Args:
            Y (torch.Tensor): 
                Tensor of shape [n_points, 2] in optimization space.

        Returns:
            torch.Tensor:
                Tensor of Pareto-optimal points, shape [n_pareto, 2]
        '''
        if Y_opt.numel() == 0:
            return Y_opt

        if Y_opt.shape[1] != 2:
            raise ValueError("compute_pareto_front currently supports exactly 2 objectives.")

        # Sort by objective 0 (descending = best first)
        order = torch.argsort(Y_opt[:, 0], descending=True)
        Y_sorted = Y_opt[order]

        pareto_mask = torch.zeros(Y_sorted.shape[0], dtype=torch.bool)

        best_y2 = -torch.inf
        for i in range(Y_sorted.shape[0]):
            y2 = Y_sorted[i, 1]
            if y2 > best_y2:
                pareto_mask[i] = True
                best_y2 = y2

        return Y_sorted[pareto_mask]


    def get_pareto_front(self) -> torch.Tensor:
        '''2D Pareto front in optimization space.'''
        Y = self.Y_opt_space
        if Y.numel() == 0:
            return Y
        return self.compute_pareto_front(Y)
    

    def get_pareto_front_physical(self) -> torch.Tensor:
        '''2D Pareto front expressed in physical objective space.'''
        Y_pareto_opt = self.get_pareto_front()
        if Y_pareto_opt.numel() == 0:
            return Y_pareto_opt
        return self._to_physical(Y_pareto_opt)


    def set_step(self, step: int):
        '''Set the optimization step.'''
        self.step = step