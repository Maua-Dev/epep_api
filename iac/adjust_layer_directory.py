import os
import shutil
import subprocess
from pathlib import Path

BUILD_DIRECTORY = "build"
PYTHON_TOP_LEVEL_DIR = os.path.join(BUILD_DIRECTORY, "python")
REQUIREMENTS_FILE = "requirements-app.txt"

PROJECT_ROOT = Path(__file__).parent.parent
SHARED_CODE_SOURCE = os.path.join(PROJECT_ROOT, "src", "shared")


def adjust_layer_directory():
    """
    Prepara um diretório 'build' para uma Lambda Layer do AWS CDK.

    A função junta o código local compartilhado e as dependências externas (pip)
    na estrutura de pastas que a Lambda espera (/python).
    """
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)

    shared_code_intermediate_dir = os.path.join(PYTHON_TOP_LEVEL_DIR, "src")
    os.makedirs(shared_code_intermediate_dir)

    print(f"Copiando código de: {SHARED_CODE_SOURCE}")
    shared_code_dest = os.path.join(
        shared_code_intermediate_dir,
        os.path.basename(SHARED_CODE_SOURCE),
    )
    shutil.copytree(SHARED_CODE_SOURCE, shared_code_dest)

    requirements_path = os.path.join(PROJECT_ROOT, REQUIREMENTS_FILE)
    if os.path.exists(requirements_path):
        subprocess.check_call(
            [
                "pip",
                "install",
                "-r",
                requirements_path,
                "-t",
                PYTHON_TOP_LEVEL_DIR,
                "--no-cache-dir",
                "--platform",
                "manylinux2014_x86_64",
                "--python-version",
                "3.13",
                "--only-binary=:all:",
            ]
        )
    else:
        print(
            f"Aviso: Arquivo '{requirements_path}' não encontrado. "
            "Nenhuma dependência externa será instalada."
        )


if __name__ == "__main__":
    adjust_layer_directory()
