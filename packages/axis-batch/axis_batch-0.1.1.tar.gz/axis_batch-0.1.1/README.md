# Axis Batch

<p align="center">
  <a href="https://github.com/34j/axis-batch/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/34j/axis-batch/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://axis-batch.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/axis-batch.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/34j/axis-batch">
    <img src="https://img.shields.io/codecov/c/github/34j/axis-batch.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/axis-batch/">
    <img src="https://img.shields.io/pypi/v/axis-batch.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/axis-batch.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/axis-batch.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://axis-batch.readthedocs.io" target="_blank">https://axis-batch.readthedocs.io </a>

**Source Code**: <a href="https://github.com/34j/axis-batch" target="_blank">https://github.com/34j/axis-batch </a>

---

Divide an array into batches along specific axes in NumPy / PyTorch / JAX

## Installation

Install this via pip (or your favourite package manager):

```shell
pip install axis-batch
```

## Usage

```python
import numpy as np

from axis_batch import AxisBatch

a = np.arange(12).reshape(3, 4)
b = AxisBatch(a, axis=0, size=2)
for i, x in enumerate(b):
    print(f"{i}: {x}")
    b.send(x + 1)
print(b.value)
```

```text
0: [[0 1 2 3]
 [4 5 6 7]]
1: [[ 8  9 10 11]]
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
