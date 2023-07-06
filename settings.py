import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TKN = os.environ.get("MTEyNjM4OTg4OTM5MTM5NDkxOA.G7Cev-.0HHQKrO2NVBzfS6fbbRZdSICMgAs2CcFTx_snU")