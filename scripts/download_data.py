import os
import requests


def download_file(url: str, save_path: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(response.content)
    print(f"File downloaded and saved in {save_path}")


if __name__ == "__main__":
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    os.makedirs("data", exist_ok=True)
    save_path = os.path.join("data", "red_wine_quality.csv")
    download_file(url, save_path)
