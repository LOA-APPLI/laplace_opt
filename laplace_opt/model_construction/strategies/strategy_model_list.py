# libraries
import torch
from botorch.models import SingleTaskGP, ModelListGP
from botorch.models.transforms.outcome import Standardize
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch import fit_gpytorch_mll
from botorch.utils.transforms import normalize

# kernels
from gpytorch.kernels.rbf_kernel import RBFKernel
from gpytorch.kernels.matern_kernel import MaternKernel
from gpytorch.kernels.scale_kernel import ScaleKernel

# project
from laplace_opt.core.optimizerContext import OptimizationContext
from laplace_opt.model_construction import StrategyStructure


class ModelList(StrategyStructure):
    '''
    Independent-output Gaussian Process model.

    Each output dimension is modeled with an independent SingleTaskGP.
    The resulting models are combined into a ModelListGP for multi-output
    Bayesian optimization.
    '''
    display_name = "Independent GP (ModelList)"
    description = (
        "Independent Gaussian Process for each output dimension.\n"
        "Assumes outputs are conditionally independent given X.\n"
        "Works for Single- and Multi-objectives."
    )

    parameters: dict[str, dict] = {

        "standardize_outputs": {
            "type": bool,
            "default": True,
            "label": "Standardize outputs",
            "description": (
                "Apply per-output standardization before GP training.\n"
                "Improves numerical stability and conditioning."
            )
        },

        "covar_module": {
            "type": dict,
            "default": 0,
            "combo": {
                "RBF": RBFKernel,
                "Matern": MaternKernel
            },
            "label": "Kernel",
            "description" : (
                "Kernel used for each independent Gaussian Process.\n"
                "Defines smoothness and correlation structure of the surrogate model."
            )
        },

        "nu": {
            "type": float,
            "decimals": 3,
            "step": 0.1,
            "min": 1e-3,
            "max": 100,
            "default": 2.5,
            "label": "nu",
            "description": (
                "smoothness parameter\n"
                "Usual are 2.5; 1.5; 0.5 (smaller values are less smooth)\n"
                "Only used if kernel is 'Matern'"
            ),
        },

    }


    def build_model(self,
                    context: OptimizationContext,
                    **params) -> ModelListGP:
        '''
        Construct independent GPs for each output dimension 
        and combine them into a ModelListGP.

        Args:
            context (OptimizationContext): 
                Provides training data for each objective and normalization bounds.
            
            **params:
                Additional keyword arguments.

        Returns:
            ModelListGP:
                multi-output GP model with independent SingleTaskGPs per output.
        '''
        models = []
        
        train_X_list = context.X_by_objective()
        train_Y_list = context.Y_by_objective()
        bounds = context.bounds

        # parameters
        kernel_kwargs = {}
        covar_cls = params.get("covar_module", RBFKernel)
        standardize = params.get("standardize_outputs", False)
        nu = params.get("nu", 2.5)

        for X, Y in zip(train_X_list, train_Y_list):         # for each objective
            X_norm = normalize(X, bounds)                    # normalize inputs

            outcome_transform = (
                Standardize(m=1) if standardize else None    # standardize output
            )

            # make the input arguments of the covar module
            kernel_kwargs["ard_num_dims"] = X.shape[-1]
            if covar_cls is MaternKernel:
                kernel_kwargs["nu"] = nu

            base_kernel = covar_cls(**kernel_kwargs)         # construct the covar
            covar = ScaleKernel(base_kernel=base_kernel)     # scale it
            
            gp = SingleTaskGP(
                train_X=X_norm,
                train_Y=Y,
                outcome_transform=outcome_transform,
                covar_module=covar,
            )

            models.append(gp)

        return ModelListGP(*models)


    def fit_model(self, 
                  model: ModelListGP,
                  **params) -> ModelListGP:
        '''
        Fit the model provided.

        Args:
            model (ModelListGP): 
                The model to be fitted.
            
            **params:
                Additional keyword arguments.

        Returns:
            ModelListGP:
                fitted multi-output GP model with independent 
                SingleTaskGPs per output.
        '''
        for gp in model.models:
            mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
            fit_gpytorch_mll(mll)
        
        return model


    def posterior(self, 
                  model: ModelListGP, 
                  X_norm: torch.Tensor) -> tuple[list, list, list]:
        '''
        Compute the posterior of the given model over
        the X_norm imput tensor.

        Args:
            model (ModelListGP):
                the model from which we compute the posterior.
            
            X_norm (torch.Tensor):
                the input tensor over which sample the posterior.
        
        Returns:
            tuple[list, list, list]
            the posterior, the mean and the std computed.
        '''
        posteriors, means, stds = [], [], []

        with torch.no_grad():
            for gp in model.models:
                post = gp.posterior(X_norm)

                posteriors.append( post )
                means.append( post.mean.squeeze(-1) )
                stds.append( post.variance.sqrt().squeeze(-1) )

        return posteriors, means, stds