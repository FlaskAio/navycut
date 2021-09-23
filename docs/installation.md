# Installation
Being a Python Web framework, Python requires Python. You must need to use Python version 3.6 or later. Python includes a lightweight database called SQLite so you won’t need to set up a database just yet. Get the latest version of Python at <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a> or with your operating system’s package manager. You can verify that Python is installed by typing python from your shell;
you should see something like:

```python
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
#### Install navycut from pypi using pip:
```bash
pip install -U navycut
```
#### Install navycut from source code:
```bash
git clone https://github.com/flaskAio/navycut.git
cd navycut
python setup.py install 
```
#### To verify that Navycut can be seen by Python, type python from your shell. Then at the Python prompt, try to import navycut:
```bash
>>> import navycut
>>> print(navycut.get_version())
0.0.4
```