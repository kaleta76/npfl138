#!/usr/bin/env python3
import argparse
import os
os.environ.setdefault("KERAS_BACKEND", "torch")  # Use PyTorch backend unless specified otherwise

import keras
import numpy as np
import torch

from mnist import MNIST

DEBUG = True

def debug_print(msg):
    if DEBUG:
        print(msg)



parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--examples", default=1024, type=int, help="MNIST examples to use.")
parser.add_argument("--iterations", default=64, type=int, help="Iterations of the power algorithm.")
parser.add_argument("--recodex", default=False, action="store_true", help="Evaluation in ReCodEx.")
parser.add_argument("--seed", default=42, type=int, help="Random seed.")
parser.add_argument("--threads", default=1, type=int, help="Maximum number of threads to use.")
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
    data = keras.ops.convert_to_tensor(mnist.train.data["images"][data_indices] / 255, dtype="float32")
    #debug_print(f"{data.size()=}")
    # TODO: Data has shape [args.examples, MNIST.H, MNIST.W, MNIST.C].
    # We want to reshape it to [args.examples, MNIST.H * MNIST.W * MNIST.C].
    # We can do so using `keras.ops.reshape(data, new_shape)` with new shape
    # `[data.shape[0], data.shape[1] * data.shape[2] * data.shape[3]]`.

    # zmena tvaru dát pomocou keras
    data = keras.ops.reshape(data,[args.examples, MNIST.H * MNIST.W * MNIST.C])
    #data1 = data.reshape(args.examples, MNIST.H * MNIST.W * MNIST.C)

    #debug_print(f"{torch.equal(data, data1)=}")


    # TODO: Now compute mean of every feature. Use `keras.ops.mean`, and set
    # `axis` to zero -- therefore, the mean will be computed across the first
    # dimension, so across examples.

    # vypocet priemernej hodnoty - mean pre kazdy prvok tensoru axis = 0
    mean = keras.ops.mean(data, axis=0)
    #mean1 = torch.mean(data, dim=0)
    #debug_print(f"{torch.equal(mean, mean1)=}")

    #debug_print(f"{mean.size()=}")

    # TODO: Compute the covariance matrix. The covariance matrix is
    #   (data - mean)^T * (data - mean) / data.shape[0]
    # where transpose can be computed using `keras.ops.transpose` and
    # matrix multiplication using either Python operator @ or `keras.ops.matmul`.

    # Odoberieme priemernú hodnotu od dát
    data_centered = data - mean

    #debug_print(f"{data_centered.size()=}")

    # Vypočítame transpozíciu centrovanej matice
    data_centered_T = keras.ops.transpose(data_centered)
    #data_centered_T1 = torch.transpose(data_centered, 0, 1)
    #debug_print(f"{torch.equal(data_centered_T, data_centered_T1)=}")

    #debug_print(f"{data_centered_T.size()=}")
    # Vypočítame maticu kovariancie
    cov = keras.ops.matmul(data_centered_T,data_centered) / data.shape[0]
    #cov1 = data_centered_T @ data_centered / data.shape[0]
    #debug_print(f"{torch.equal(cov, cov1)=}")

    #debug_print(f"{cov.size()=}")

    # TODO: Compute the total variance, which is the sum of the diagonal
    # of the covariance matrix. To extract the diagonal use `keras.ops.diagonal`,
    # and to sum a tensor use `keras.ops.sum`.

    # Získame diagonálu matice kovariancie
    cov_diag = keras.ops.diagonal(cov)
    #cov_diag1 = torch.diagonal(cov)
    #debug_print(f"{torch.equal(cov_diag, cov_diag1)=}")

    #debug_print(f"{cov_diag.size()=}")

    # Vypočítame súčet diagonály, čo je celková variancia
    total_variance = keras.ops.sum(cov_diag)
    #total_variance1 = torch.sum(cov_diag)
    #debug_print(f"{total_variance=}, {total_variance1=}")

    # TODO: Now run `args.iterations` of the power iteration algorithm.
    # Start with a vector of `cov.shape[0]` ones of type `"float32"` using `keras.ops.ones`.

    #v = keras.ops.ones(cov.shape[0], dtype=torch.float32)
    v = keras.ops.ones(cov.shape[0], dtype=torch.float32)
    #v1 = torch.ones(cov.shape[0], dtype=torch.float32)
    #debug_print(f"{torch.equal(v, v1)=}")

    #debug_print(f"{v.size()=}")

    for i in range(args.iterations):
        # TODO: In the power iteration algorithm, we compute
        # 1. v = cov v
        #    The matrix-vector multiplication can be computed as regular matrix multiplication.
        # 2. s = l2_norm(v)
        #    The l2_norm can be computed using for example `keras.ops.norm`.
        # 3. v = v / s

        # 1. v = cov v
        # urobime maticovo-vektorové násobenie matice kovariancie a vektora v
        #v1 = torch.mv(cov, v)
        # Výpočet maticovo-vektorového násobenia
        v = keras.ops.dot(cov, v)
        #debug_print(f"{torch.equal(v1, v2)=},{v1.size()},{v2.size()}")

        # 2. s = l2_norm(v)
        s = keras.ops.norm(v)
        #s2 = torch.linalg.vector_norm(v2)

        #debug_print(f"{torch.equal(s1, s2)=}")        
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
