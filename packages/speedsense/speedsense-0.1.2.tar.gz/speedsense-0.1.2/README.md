# SpeedSense

This is a Python package that tries to give its users the time complexity of any function you desire. There are limitations to this
library, which we are still working on.

Currently, the types of functions for which the library works are:
1. Single-variable input functions  
2. Non-recursive functions  
3. In-built library support is not available at the moment


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable) to install speedsense:

```bash
pip install speedsense
```

## Usage

For using this package you need [inspect](https://docs.python.org/3/library/inspect.html) which is a part of Python Standard Library so no need to install it separately.

```python
from speedsense.tc_estimator import compute_complexity
import inspect

def userfunc(n):
    # write your function here
    pass

code =  inspect.getsource(userfunc)
compute_complexity(code)  # prints the time complexity
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
