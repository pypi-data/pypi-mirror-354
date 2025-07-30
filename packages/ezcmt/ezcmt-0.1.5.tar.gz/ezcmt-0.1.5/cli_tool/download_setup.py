import argparse
import gdown
import shutil
import os
import subprocess
from .json_utils import write_json,read_json

def add_subparser(subparsers):
    download_parser = subparsers.add_parser(
        "download-model",
        help = "Download the commit message generator model."
    )

    setup_parser = subparsers.add_parser(
        "setup-model",
        help = "Setup the model."
    )

    download_parser.set_defaults(func=download)

    setup_parser.set_defaults(func=setup)

def download(args):
    model_downloaded = read_json("model_downloaded")

    if model_downloaded:
        print("The model is already downloaded.")
    else:
        model_folder = "ezcmt-model"
        os.mkdir(model_folder)

        gdown.download("https://drive.google.com/uc?id=1yteR3xbPi12ATNAO9Ys1nX-iAd_7qpnB",
                    model_folder + "/Modelfile")

        gdown.download("https://drive.google.com/uc?id=1N3Jdi1Xctn4DRLhD6-jvu4Qe_m1yWD-E",
                    model_folder + "/ezcmt.gguf")
        
        gdown.download("https://drive.google.com/uc?id=1uWTnCZJ2mR7fbJfrUWFSLjxOgT3YdxSg",
                    model_folder + "/qwen2.5-coder.gguf")
        
        print("Download done.")

        write_json("model_downloaded",True)

def setup(args):
    if read_json("setup_done"):
        print("Setup is already done.")
    else:
        if read_json("ollama_installed"):
            result = subprocess.Popen(["ollama","create","-f","ezcmt-model/Modelfile","_ezcmt"])
            if result.returncode == 0:
                print("An error occured. Perhaps Ollama isnt installed?")
            print("Setup done.")
            write_json("setup_done",True)
        else:
            print("Cannot setup when Ollama isnt installed.")