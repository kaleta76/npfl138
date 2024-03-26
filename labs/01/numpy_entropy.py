#!/usr/bin/env python3
import argparse

import numpy as np

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--data_path", default="C:\\Users\\kalet\\Documents\\npfl138\\labs\\01\\numpy_entropy_data_4.txt", type=str, help="Data distribution path.")
parser.add_argument("--model_path", default="C:\\Users\\kalet\\Documents\\npfl138\\labs\\01\\numpy_entropy_model_4.txt", type=str, help="Model distribution path.")
parser.add_argument("--recodex", default=False, action="store_true", help="Evaluation in ReCodEx.")
# If you add more arguments, ReCodEx will keep them with your default values.

def main(args: argparse.Namespace) -> tuple[float, float, float]:

    # TODO: Load data distribution, each line containing a datapoint -- a string.
    zoznam = []
    with open(args.data_path, "r") as data:
        for line in data:
            line = line.rstrip("\n")
            # TODO: Process the line, aggregating data with built-in Python
            # data structures (not NumPy, which is not suitable for incremental
            # addition and string mapping).
            zoznam.append(line)
            #print(f"{line=}")
    # Nakoniec premeníme zoznam na NumPy pole
    symboly = np.array(zoznam)
    # Výpočet početnosti symbolov
    values, frequencies  = np.unique(symboly, return_counts=True)
    # Výpočet pravdepodobnosti
    p = frequencies / frequencies.sum()
    #print(f"{relative_frequencies=}")
    # TODO: Compute the entropy H(data distribution). You should not use
    # manual for/while cycles, but instead use the fact that most NumPy methods
    # operate on all elements (for example `*` is vector element-wise multiplication).
    # Compute the entropy
    entropy = -np.sum(p * np.log(p))


    # TODO: Create a NumPy array containing the data distribution. The
    # NumPy array should contain only data, not any mapping. Alternatively,
    # the NumPy array might be created after loading the model distribution.
    # Začneme vytvorením prázdneho zoznamu

    model_distribution = {}
    unique_symbols = set()
    # Potom prejdeme každý riadok v objekte model
    # TODO: Load model distribution, each line `string \t probability`.
    try:
        with open(args.model_path, "r") as model:
            for line in model:
                # Odstránime znak nového riadku na konci každého riadku
                line = line.rstrip("\n")
                string, probability = line.split("\t")  # Rozdelenie riadku
                probability = float(probability)  # Konverzia pravdepodobnosti
                if string in unique_symbols:
                    raise ValueError(f"Symbol '{string}' má viacero pravdepodobností.")
                unique_symbols.add(string)

                model_distribution[string] = probability
    except ValueError as e:
        print(e)
        exit(1)
    except Exception as e:
        print(f"Chyba pri načítaní súboru: {e}")
        exit(1)

    # TODO: Process the line, aggregating using Python data structures.

    # TODO: Create a NumPy array containing the model distribution.
        
    try:
    # Nacitanie predpovedanej distribúcie pravdepodobností z modelu
        q = np.array([model_distribution[value] for value in values])
    except KeyError as e:
    # Výnimka, ak niečo chýba v model_distribution
        crossentropy = np.inf
        kl_divergence = np.inf
        # Return the computed values for ReCodEx to validate.
        return entropy, crossentropy, kl_divergence
        #raise ValueError(f"Chýbajúca hodnota: {e}")


    # TODO: Compute cross-entropy H(data distribution, model distribution).
    # When some data distribution elements are missing in the model distribution,
    # return `np.inf`.
    crossentropy = -np.sum(p * np.log(q))

    # TODO: Compute KL-divergence D_KL(data distribution, model_distribution),
    # again using `np.inf` when needed.
    kl_divergence = np.sum(p * np.log(p/q))

    # Return the computed values for ReCodEx to validate.
    return entropy, crossentropy, kl_divergence


if __name__ == "__main__":
    #args = parser.parse_args([] if "__file__" not in globals() else None)
    # python3 numpy_entropy.py --data_path numpy_entropy_data_1.txt --model_path numpy_entropy_model_1.txt
    #argumenty = ["--data_path", "numpy_entropy_data_1.txt", "--model_path", "numpy_entropy_model_1.txt"]
    args = parser.parse_args(argumenty if "__file__" not in globals() else None)
    entropy, crossentropy, kl_divergence = main(args)
    print("Entropy: {:.2f} nats".format(entropy))
    print("Crossentropy: {:.2f} nats".format(crossentropy))
    print("KL divergence: {:.2f} nats".format(kl_divergence))
