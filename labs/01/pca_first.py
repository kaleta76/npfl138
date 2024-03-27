#!/usr/bin/env python3
import argparse
import os

import numpy as np
import torch

from mnist import MNIST

DEBUG = False

def debug_print(msg):
    if DEBUG:
        print(msg)

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--examples", default=1024, type=int, help="MNIST examples to use.")
parser.add_argument("--iterations", default=64, type=int, help="Iterations of the power algorithm.")
parser.add_argument("--recodex", default=False, action="store_true", help="Evaluation in ReCodEx.")
parser.add_argument("--seed", default=42, type=int, help="Random seed.")
parser.add_argument("--threads", default=2, type=int, help="Maximum number of threads to use.")
# If you add more arguments, ReCodEx will keep them with your default values.


def main(args: argparse.Namespace) -> tuple[float, float]:
    # Set the random seed and the number of threads.
    np.random.seed(args.seed)
    if args.threads:
        torch.set_num_threads(args.threads)
        torch.set_num_interop_threads(args.threads)

    # Load data
    mnist = MNIST()

    data_indices = np.random.choice(mnist.train.size, size=args.examples, replace=False)
    data = torch.tensor(mnist.train.data["images"][data_indices] / 255, dtype=torch.float32)

    debug_print(f"{data.size()}")

    # TODO: Data has shape [args.examples, MNIST.H, MNIST.W, MNIST.C].
    # We want to reshape it to [args.examples, MNIST.H * MNIST.W * MNIST.C].
    # We can do so using `torch.reshape(data, new_shape)` with new shape
    # `[data.shape[0], data.shape[1] * data.shape[2] * data.shape[3]]`.

    # zmena tvaru dat pomocou torch
    data = data.reshape(args.examples, MNIST.H * MNIST.W * MNIST.C)
    debug_print(f"{data.size()=}")

    # TODO: Now compute mean of every feature. Use `torch.mean`, and set
    # `dim` (or `axis`) argument to zero -- therefore, the mean will be
    # computed across the first dimension, so across examples.
    #
    # Note that for compatibility with Numpy/TF/Keras, all `dim` arguments
    # in PyTorch can be also called `axis`.

    # vypocet priemernej hodnoty - mean pre kazdy prvok tensoru dim = 0
    mean = torch.mean(data, dim=0)

    debug_print(f"{mean=}")

    # TODO: Compute the covariance matrix. The covariance matrix is
    #   (data - mean)^T * (data - mean) / data.shape[0]
    # where transpose can be computed using `torch.transpose` or `torch.t` and
    # matrix multiplication using either Python operator @ or `torch.matmul`.
    # Odoberieme priemernú hodnotu od dát
    data_centered = data - mean

    debug_print(f"{data_centered=}")

    # Vypočítame transpozíciu centrovanej matice
    data_centered_T = torch.transpose(data_centered, 0, 1)

    debug_print(f"{data_centered_T=}")
    # Vypočítame maticu kovariancie
    cov = data_centered_T @ data_centered / data.shape[0]

    debug_print(f"{cov=}")

    # TODO: Compute the total variance, which is the sum of the diagonal
    # of the covariance matrix. To extract the diagonal use `torch.diagonal`,
    # and to sum a tensor use `torch.sum`.

    # Získame diagonálu matice kovariancie
    cov_diag = torch.diagonal(cov)

    # Vypočítame súčet diagonály, čo je celková variancia
    total_variance = torch.sum(cov_diag)

    debug_print(f"{total_variance=}")


    # TODO: Now run `args.iterations` of the power iteration algorithm.
    # Start with a vector of `cov.shape[0]` ones of type `torch.float32` using `torch.ones`.
    v = torch.ones(cov.shape[0], dtype=torch.float32)

    debug_print(f"{v=}")

    for i in range(args.iterations):
        # TODO: In the power iteration algorithm, we compute
        # 1. v = cov v
        #    The matrix-vector multiplication can be computed as regular matrix multiplication
        #    or using `torch.mv`.
        # 2. s = l2_norm(v)
        #    The l2_norm can be computed using for example `torch.linalg.vector_norm`.
        # 3. v = v / s
        
        # 1. v = cov v
        v = torch.mv(cov, v)
        
        # 2. s = l2_norm(v)
        # vypočítame normu (dĺžku) vektora v
        s = torch.linalg.vector_norm(v)
        # 3. v = v / s
        v = v / s

    # The `v` is now approximately the eigenvector of the largest eigenvalue, `s`.
    # We now compute the explained variance, which is the ratio of `s` and `total_variance`.
    explained_variance = s / total_variance

    # Return the total and explained variance for ReCodEx to validate
    return total_variance, 100 * explained_variance


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    total_variance, explained_variance = main(args)
    print("Total variance: {:.2f}".format(total_variance))
    print("Explained variance: {:.2f}%".format(explained_variance))
