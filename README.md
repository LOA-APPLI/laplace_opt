# LAPLACE Optimizer (LAPLACE-LHC)

**LAPLACE Optimizer** is a Python desktop application for Bayesian optimization workflows, built with [PyQt6](https://pypi.org/project/PyQt6/) and [BoTorch](https://botorch.org/).

The application provides a graphical interface for configuring and running optimization experiments, monitoring inputs and objectives, and visualizing optimization results. It integrates with the `laplace_server` protocol and `laplace_log` logging system to support structured communication and logging throughout the optimization workflow.

## Features

- **Graphical interface:** Desktop application built with PyQt6.
- **Bayesian optimization:** Optimization workflows powered by BoTorch and PyTorch.
- **Configurable models:** Model construction resources for defining inputs, objectives, strategies, and acquisition functions.
- **Structured logging:** Integration with `laplace_log` for experiment logging.
- **Server protocol integration:** Communication based on the `laplace_server` protocol.
- **Result analysis:** Tools for interpreting optimization results and visualizing model predictions.
- **Modular architecture:** Separate components for the user interface, optimization logic, model construction, and post-analysis.

## Installation

### Prerequisites

Make sure Python and `pip` are installed in your environment. A virtual environment is recommended to isolate project dependencies.

### Install dependencies

Install the required dependencies:

```bash
pip install PyQt6 qdarkstyle torch gpytorch botorch laplace-server laplace-log matplotlib
```

### Install LAPLACE Optimizer

If the package is available on your configured Python package index, install it with:

```bash
pip install laplace-opt
```

If you are developing the project from its Git repository, see the source installation instructions below.

## Getting Started

### Option 1: Run the installed package

If you installed `laplace-opt` using `pip`:

1. Copy the provided `main.py` example into your working directory, if required by your installation.
2. Launch the application using this entry point.
3. In the **Model path** field, specify the path to a `model_construction/` directory containing the resources required for your optimization workflow.
4. Your configuration will be loaded on the next application start. 

The model construction directory defines the experiment-specific configuration, including inputs, objectives, optimization strategies, and acquisition functions.

**Note:** The exact contents of `model_construction/` depend on the model and configuration expected by the application. You can copy/paste the default one and modify it according to your needs.

### Option 2: Run from the Git repository

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/LOA-APPLI/laplace_opt
cd laplace_opt
```

Install the dependencies, then launch the application as a Python module:

```bash
python -m laplace_opt.main
```

## Project Structure

```text
laplace_opt/
├── laplace_opt/
│   ├── main.py                 # Application entry point
│   ├── app_config.ini          # Default configuration
│   ├── interface/              # GUI implementation
│   ├── core/                   # Optimization logic
│   ├── model_construction/     # Default model resources
│   ├── post_analysis/          # Result interpretation and analysis
│   └── utils/                  # Shared utilities
├── benchmark/                  # Benchmarking and algorithmic evaluation
├── examples/                   # Test-function data and usage examples
├── tests/                      # Developer-oriented tests
├── requirements.txt            # Package requirements
├── LICENSE                     # GPL-3.0 license
└── README.md                   # Project documentation
```

## Development Roadmap

The following improvements are planned:

- [ ] **Post-analysis:** Correct and adapt `PostAnalysis`, particularly to account for the updated model-saving workflow.
- [ ] **Input and output monitoring:** Add the ability to track selected inputs or outputs without including them in the optimization process.
- [ ] **Visualization improvements:** Improve `PlotWidget` and posterior plots, including 3D visualization and model-related bug fixes.
- [ ] **Suggestion representation:** Replace the current sparse-list representation (e.g., `[None, None, position, ..., None]`) with a clearer and more robust data structure.
- [ ] **Acquisition function visualization:** Consider adding acquisition function plots to `PlotWindow`.
- [ ] **Examples and post-analysis workflows:** Review and update the examples based on saved `.pt` data for test functions, including the associated procedures for loading, interpreting, and analyzing results. This work should be aligned with the planned changes to `PostAnalysis`.
- [ ] **Benchmarking:** Revisit the benchmark framework and assess the feasibility of completing and validating the intended algorithmic evaluation workflow. The current implementation is incomplete and is not yet a reliable basis for benchmarking results.

## Development and Testing

The `tests/` directory contains developer-oriented tests intended to support implementation, debugging, and regression checks during development. These tests are generally quicker to run than a full benchmarking workflow and are primarily intended for contributors rather than end users.

The tests and benchmark serve different purposes: tests help identify implementation issues, whereas benchmarking is intended to evaluate optimization performance under defined experimental conditions. Neither should be interpreted as comprehensive validation of the application in its current state.

The examples provide complementary reference material for working with saved test-function data and analyzing optimization results. Their compatibility with the current implementation still needs to be reviewed, particularly in light of the planned post-analysis changes.

## License

This project is distributed under the [GNU General Public License v3.0](LICENSE).

## Project Status

LAPLACE Optimizer is actively used within the LAPLACE ecosystem for optimization experiments. It is intended for controlled research environments and scientific workflows.

