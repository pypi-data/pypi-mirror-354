# CausalPFN: Amortized Causal Effect Estimation via In-Context Learning

An easy-to-use library for causal effect estimation using transformer-based in-context learners.

## Setup
Run the following command to add the package:

```bash
pip install -e .
```
If you are using some of the extended features such as benchmarking, you may need to install it using the `dev` flag:

```bash
pip install -e .[dev]
```

## Downloading and Setting up the Pre-trained Checkpoints

To download our checkpoints, setup using the following command (Assuming your checkpoint dir is `output/checkpoints`):

```bash
mkdir -p output/checkpoints/causalpfn
cd output/checkpoints/causalpfn && gdown https://drive.google.com/uc?id=1O-nV-2CT-nFVPCs99GXDfkG0McbWnop0 && cd -
```

Now make sure to store the *absolute path* to checkpoint directories in `dotenv` so that the library can access them -- this will make it easier to load the model path using dotenv. You can do this by running the following commands:

```bash
dotenv set CHECKPOINT_PATH <absolute_path_to_your_checkpoint_pt_file>
```

## Example Usage

Here is a simple example of how to use CausalPFN for causal effect estimation on a synthetic dataset where the ground truth causal effect is known. This example uses the `CATEEstimator` and `ATEEstimator` classes to estimate the Conditional Average Treatment Effect (CATE) and Average Treatment Effect (ATE) respectively.

```python
import numpy as np
from dotenv import load_dotenv
import os
import torch
import time
from causalpfn import CATEEstimator, ATEEstimator

load_dotenv(override=True)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# 1. Simulate synthetic data
np.random.seed(42)
n = 20000
d = 5
X = np.random.normal(1, 1, size=(n, d)).astype(np.float32)  # feature matrix
def true_cate(x):  # true CATE is nonlinear in x
    return np.sin(x[:, 0]) + 0.5 * x[:, 1]
def true_ate():
    return np.mean(true_cate(X))
tau = true_cate(X).astype(np.float32)
T = np.random.binomial(1, p=0.5, size=n).astype(np.float32)  # random treatment assignment
Y0 = X[:, 0] - X[:, 1] + np.random.normal(0, 0.1, size=n).astype(np.float32)  # control outcome
Y1 = Y0 + tau  # treated outcome
Y = Y0 * (1 - T) + Y1 * T  # observed outcome

# 2. Split into train/test
train_idx = np.random.choice(n, size=int(0.7 * n), replace=False)
test_idx = np.setdiff1d(np.arange(n), train_idx)
X_train, X_test = X[train_idx], X[test_idx]
T_train = T[train_idx]
Y_train = Y[train_idx]
tau_test = tau[test_idx]
# 3. Estimate CATE using CausalPFN
start_time = time.time()
causalpfn_cate = CATEEstimator(
    model_path=os.environ["CHECKPOINT_PATH"],
    device=device,
    verbose=True,
)
causalpfn_cate.fit(X_train, T_train, Y_train)
cate_hat = causalpfn_cate.estimate_cate(X_test)
cate_time = time.time() - start_time

# 4. Estimate ATE using CausalPFN
causalpfn_ate = ATEEstimator(
    model_path=os.environ["CHECKPOINT_PATH"],
    device=device,
    verbose=True,
)
causalpfn_ate.fit(X, T, Y)
ate_hat = causalpfn_ate.estimate_ate()

# 5. Evaluate
pehe = np.sqrt(np.mean((cate_hat - tau_test) ** 2))  # PEHE: squared error of CATE estimates
ate_rel_error = np.abs((ate_hat - true_ate()) / true_ate())  # relative error of ATE estimate
print(f"ATE Relative Error: {ate_rel_error:.4f}")
print(f"PEHE: {pehe:.4f}")
print(f"CATE estimation time spent per 1000 samples: {cate_time / (len(X) / 1000):.4f} seconds")
```

For more examples, refer to the notebooks; all of them can be found in the [`notebooks`](notebooks) directory:

1. [`notebooks/causal_effect`](notebooks/causal_effect.ipynb): Comparing CausalPFN with the other baselines for heterogeneous treatment effect estimation & ATE estimation.
2. [`notebooks/hillstrom_marketing`](notebooks/hillstrom_marketing.ipynb): A use-case of CausalPFN for uplift modelling on Hillstrom.
3. [`notebooks/calibration`](notebooks/calibration.ipynb): Demonstrating CausalPFN's uncertainty quantification and calibration features on synthetic datasets.

## Full Paper Reproducibility

To fully reproduce the results of the paper, follow [this](./REPRODUCE.md) more extended document.
