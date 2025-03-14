import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from compare import levenshtein_norm


def load_texts(directory: str, extensions: list[str]) -> dict[str, str]:
    filepaths = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files if file.split(".")[-1] in extensions
    ]
    return {path: open_file(path) for path in filepaths}


def open_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def compute_similarity_matrix(texts: dict[str, str]) -> pd.DataFrame:
    filenames = list(texts.keys())
    size = len(filenames)

    df = pd.DataFrame(index=filenames, columns=filenames, dtype=float)

    for i, f1 in enumerate(filenames):
        for j, f2 in enumerate(filenames):
            if i != j:
                df.at[f1, f2] = levenshtein_norm(texts[f1], texts[f2])
            else:
                df.at[f1, f2] = 1.0

    return df


def plot_heatmap(matrix: pd.DataFrame):
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    plt.title("Similarity Matrix Heatmap")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()


def main():
    directory = "./test_dir"
    extensions = ["txt"]

    texts = load_texts(directory, extensions)
    similarity_matrix = compute_similarity_matrix(texts)

    plot_heatmap(similarity_matrix)


if __name__ == '__main__':
    main()
