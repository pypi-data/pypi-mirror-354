# punigowda

🚀 A simple Python package to demonstrate how to create and publish your own Python package to PyPI.

This package provides sample GenAI program descriptions for educational or reference purposes.

## 📦 Installation

```bash
pip install punigowda

from punigowda import print_genai_programs
print_genai_programs(n) #where n is the number of program


create a file named.pypirc in home directory and paste the following code in it

[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = api token of pypi.org