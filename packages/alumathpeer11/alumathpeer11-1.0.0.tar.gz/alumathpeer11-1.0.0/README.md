# alumathpeer11

Pure Python matrix operations library without external dependencies.

## Features

- Matrix multiplication for different dimensions
- Efficient loop-based implementation
- No external dependencies
- Simple and intuitive API

## Installation

````bash
pip install alumathpeer11

from alumathpeer11 import Matrix, create_matrix

# Create matrices
m1 = create_matrix([[1, 2], [3, 4]])
m2 = create_matrix([[5, 6], [7, 8]])

# Matrix multiplication
result = m1 * m2
print(result)
## Step 2: Publishing to PyPI

### Prerequisites:
1. **Install required tools:**
   ```bash
   pip install setuptools wheel twine

   cd alumathpeer11
python setup.py sdist bdist_wheel
````
