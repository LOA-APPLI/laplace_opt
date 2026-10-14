# libraries
import torch
from botorch.utils.sampling import draw_sobol_samples


def make_grid(bounds: torch.Tensor, 
              n_per_dim: int = 100) -> torch.Tensor:
    '''
    Args:
        bounds (torch.Tensor):
            the input boundaries in 2 x d tensor.

        n_per_dim (int):
            number of sample per dimension if d <= 2,
            else number of Solbol samples.

    Returns:
        torch.Tensor:
            tensor in physcial space.
    '''
    d = bounds.shape[1]

    if d <= 2:

        axes = [
            torch.linspace(bounds[0, i], bounds[1, i], n_per_dim)
            for i in range(d)
        ]

        mesh = torch.meshgrid(*axes, indexing="ij")

        X = torch.stack(
            [m.reshape(-1) for m in mesh],
            dim=-1,
        )
    
    else:

        X = draw_sobol_samples(
            bounds=bounds,
            n=n_per_dim,
            q=1,
        ).squeeze(1)


    return X