import os

from crypto_env.dataloader.ethloader import ETHLoader

loader = ETHLoader(base_dir=os.getcwd(), features=[])

for idx, item in loader:
    print(f"idx: {idx}, value: {str(item)}")