import subprocess
import shutil
import os
import tarfile

def test_cli():
    if os.path.exists("test_output"):
        shutil.rmtree("test_output")
    subprocess.check_call("python -m pypi_download_pkg.cli --pkg-filter cryptography -r tests/test_data/requirements.txt --output-dir test_output")
    assert os.path.exists("test_output/cryptography-41.0.2-cp37-abi3-manylinux_2_17_aarch64.manylinux2014_aarch64.whl")
    assert os.path.exists("test_output/cryptography-41.0.2.tar.gz")
    with tarfile.open("test_output/cryptography-41.0.2.tar.gz") as tf:
        tf.extractall("test_output/cryptography-source")
    assert os.path.exists("test_output/cryptography-source/cryptography-41.0.2/setup.py")