# <img src="https://raw.githubusercontent.com/Lotfollahi-lab/CellDISECT/main/media/CellDISECT_Logo_whitebg.png" width="1000" alt="celldisect-logo">

<div align="center">

[![PyPI version](https://badge.fury.io/py/celldisect.svg)](https://badge.fury.io/py/celldisect)
[![Documentation Status](https://readthedocs.org/projects/celldisect/badge/?version=latest)](https://celldisect.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://github.com/Lotfollahi-lab/celldisect/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/Lotfollahi-lab/celldisect?logo=GitHub&color=yellow)](https://github.com/Lotfollahi-lab/celldisect/stargazers)
[![Downloads](https://static.pepy.tech/badge/celldisect)](https://pepy.tech/project/celldisect)
[![bioRxiv](https://img.shields.io/badge/bioRxiv-2025.06.03.657578-red.svg)](https://www.biorxiv.org/content/10.1101/2025.06.03.657578v1)

</div>

> **ℹ️ Beta Version Available**: A beta version with compatibility for Google Colab and newer versions of torch and scvi-tools is available on the [`beta-colab`](https://github.com/Lotfollahi-Lab/CellDISECT/tree/beta-colab) branch. Install it with `pip install celldisect==0.2.0b1`.

## 🧬 Overview

CellDISECT (Cell DISentangled Experts for Covariate counTerfactuals) is a powerful causal generative model that enhances single-cell analysis by:

- 🔍 **Disentangling Variations**: Separates covariate variations at test time
- 🧪 **Counterfactual Predictions**: Learns to make accurate counterfactual predictions
- 🎯 **Flexible Fairness**: Achieves flexible fairness through expert models for each latent space
- 🔬 **Enhanced Discovery**: Captures both covariate-specific information and novel biological insights

<p align="center">
  <img src="https://raw.githubusercontent.com/Lotfollahi-lab/CellDISECT/main/media/celldisect_illustration.png" width="750">
</p>

## 📚 Documentation

Visit our [comprehensive documentation](https://celldisect.readthedocs.io/) for:
- Detailed API reference
- Step-by-step tutorials
- Best practices and examples
- Advanced usage guides

## 🚀 Quick Start

### Prerequisites

We recommend using [Anaconda](https://www.anaconda.com/)/[Miniconda](https://docs.conda.io/projects/miniconda/en/latest/). Create and activate a new environment:

```bash
conda create -n CellDISECT python=3.9
conda activate CellDISECT
```

### Installation

1. **Install PyTorch** (tested with pytorch 2.1.2 and cuda 12):
```bash
conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=12.1 -c pytorch -c nvidia
```

2. **Install CellDISECT**:
```bash
# Via pip (stable version)
pip install celldisect

# Or via GitHub (latest development version)
pip install git+https://github.com/Lotfollahi-lab/CellDISECT
```

### Optional Dependencies

<details>
<summary>Click to expand optional installations</summary>

**RAPIDS/rapids-singlecell**:
```bash
pip install \
    --extra-index-url=https://pypi.nvidia.com \
    cudf-cu12==24.4.* dask-cudf-cu12==24.4.* cuml-cu12==24.4.* \
    cugraph-cu12==24.4.* cuspatial-cu12==24.4.* cuproj-cu12==24.4.* \
    cuxfilter-cu12==24.4.* cucim-cu12==24.4.* pylibraft-cu12==24.4.* \
    raft-dask-cu12==24.4.* cuvs-cu12==24.4.*

pip install rapids-singlecell
```

**CUDA-enabled JAX**:
```bash
pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```
</details>

## 📖 Tutorials & Examples

### Basic Tutorials

| Tutorial | Description | Links |
|----------|-------------|-------|
| **Basic Training** | Learn how to train CellDISECT and make counterfactual predictions using the Kang dataset | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Lotfollahi-Lab/CellDISECT/blob/main/docs/source/tutorials/CellDISECT_Counterfactual.ipynb) [![Documentation](https://img.shields.io/badge/docs-blue)](https://celldisect.readthedocs.io/en/latest/tutorials/CellDISECT_Counterfactual.html) |

### Advanced Applications

| Tutorial | Description | Links |
|----------|-------------|-------|
| **Latent Space Analysis** | Explore combinations of CellDISECT latent spaces for erythroid subset inference | [![Documentation](https://img.shields.io/badge/docs-blue)](https://celldisect.readthedocs.io/en/latest/tutorials/Erythroid_subset_inference.html) |
| **Double Counterfactual** | Advanced tutorial recreating Scenario 2 counterfactual on the Eraslan dataset | [![Documentation](https://img.shields.io/badge/docs-blue)](https://celldisect.readthedocs.io/en/latest/tutorials/Eraslan_CF_Tutorial.html) |

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](https://celldisect.readthedocs.io/en/latest/contributing.html) for details on how to:
- Report issues
- Submit bug fixes
- Propose new features
- Submit pull requests

## 📜 License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## 📫 Contact

For questions and support:
- Open an [issue](https://github.com/Lotfollahi-lab/celldisect/issues)
- Visit our [documentation](https://celldisect.readthedocs.io/)

## 📝 Citation

If you use CellDISECT in your research, please cite our paper:

**Megas, S., Amani, A., Rose, A., Dufva, O., Shamsaie, K., Asadollahzadeh, H., Polanski, K., Haniffa, M., Teichmann, S. A., & Lotfollahi, M.** (2025). Integrating multi-covariate disentanglement with counterfactual analysis on synthetic data enables cell type discovery and counterfactual predictions. *bioRxiv*. https://doi.org/10.1101/2025.06.03.657578

```bibtex
@article{Megas2025CellDISECT,
    title={Integrating multi-covariate disentanglement with counterfactual analysis on synthetic data enables cell type discovery and counterfactual predictions},
    author={Megas, Stathis and Amani, Arian and Rose, Antony and Dufva, Olli and Shamsaie, Kian and Asadollahzadeh, Hesam and Polanski, Krzysztof and Haniffa, Muzlifah and Teichmann, Sarah Amalia and Lotfollahi, Mohammad},
    journal={bioRxiv},
    year={2025},
    doi={10.1101/2025.06.03.657578},
    elocation-id={2025.06.03.657578},
    publisher={Cold Spring Harbor Laboratory},
    URL={https://www.biorxiv.org/content/10.1101/2025.06.03.657578v1}
}
```
