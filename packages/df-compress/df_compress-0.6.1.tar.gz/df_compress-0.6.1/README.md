[![Build](https://github.com/phchavesmaia/df-compress/actions/workflows/main.yaml/badge.svg)](https://github.com/phchavesmaia/df-compress/actions/workflows/main.yaml) 
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![PyPI](https://img.shields.io/pypi/v/df-compress?label=pypi%20package)
[![DOI](https://zenodo.org/badge/960013907.svg)](https://doi.org/10.5281/zenodo.15148480)

# df-compress
A python package to compress pandas DataFrames akin to Stata's `compress` command. This function may prove particularly helpfull to those dealing with large datasets.

## Installation
You can install `df-compress` by running the following command:
```python
pip install df_compress
```

## How to use
After installing the package use the following import: 
```python
from df_compress import compress
```

## Example
It follows a reproducible example on `df-compress` usage:
```python
from df_compress import compress
import pandas as pd
import numpy as np

df = pd.DataFrame(columns=["Year","State","Value","Int_value"])
df.Year = np.random.randint(low=2000,high=2023,size=200).astype(str)
df.State = np.random.choice(['RJ','SP','ES','MT'],size=200)
df.Value= np.random.rand(200,1)
df.Int_value = df.Value*10 // 1

compress(df, show_conversions=True) # which modifies the original DataFrame without needing to reassign it
```
Which will print for you the transformations and memory saved:
```
Initial memory usage: 0.02 MB
Final memory usage: 0.00 MB
Memory reduced by: 0.02 MB (91.3%)

Variable type conversions:
   column    from       to  memory saved (MB)
     Year  object    int16           0.009727
    State  object category           0.009178
    Value float64  float32           0.000763
Int_value float64     int8           0.001335
```
## Optional Parameters
The function has three optimal parameters (arguments):
  - `convert_strings` (bool): Whether to attempt to parse object columns as numbers
    - defaults to `True`
  - `numeric_threshold` (float): Indicates the proportion of valid numeric entries needed to convert a string to numeric
    - defaults to `0.999`   
  - `show_conversions` (bool): whether to report the changes made column by column
    - defaults to `False`

