# laplace_opt

PyQt6-based GUI application for **Laplace optimization** workflows.

This package provides a desktop application with a structured logging system and server protocol integration. It is designed to launch an interactive optimization window (`OptWindow`) and handle data and logs cleanly, suitable for research and scientific workflows.

---

## Features

- PyQt6 graphical user interface
- Structured logging via `laplace_log`
- Using `laplace_server` protocol
- Entry point via `main.py`
- Modular design separating GUI, logging, and server logic

---

## Installation

Install dependencies:

```bash
pip install PyQt6 qdarkstyle torch botorch laplace-server laplace-log matplotlib
```

Install package:

```bash
pip install laplace-opt
```

---

## Run the code

To run the code use:

```bash
python -m laplace_opt.main
```

---

## Project Structure

```
laplace_opt/
├── laplace_opt/
│   ├── main.py                 # Entry point launching the GUI
│   ├── app_config.ini          # Default configuration
│   ├── interface/              # GUI window implementation
│   ├── core/                   # Optimization process
│   ├── model_construction/     # Optimization ressources
|   ├── post_analysis/          # Result interpreter
│   ├── utils/                  # Helpers
├── tests/                      # Test scripts
├── LICENSE                     # GPL-3.0 License
└── README.md                   # Project README
```

---

## To be done

- Option in order to follow an input or output without optimizing it.
- Improve PlotWidget and the posterior plot. (3D + bug corrections).
- PostAnalysis must be corrected / adapted (especially now that the model is saved).
- Changing the formalism for the suggestion in order to avoid [None, None, ..., None] list.
- In plot window, propose to plot the acquisition function?

---

## Licence

GPL-3.0

---

## Status

This project is actively used in the LAPLACE ecosystem for optimization experiments. It is designed for controlled research environments and scientific workflows.