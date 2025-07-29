# tsuniverse

<a href="https://pypi.org/project/tsuniverse/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/tsuniverse">
</a>

A library for efficiently processing a time series universe to determine causal features.

## Dependencies :globe_with_meridians:

Python 3.11.6:

- [pandas](https://pandas.pydata.org/)
- [pyarrow](https://arrow.apache.org/docs/python/index.html)
- [scikit-learn](https://scikit-learn.org/)
- [timeseries-features](https://github.com/8W9aG/timeseries-features)
- [scipy](https://scipy.org/)
- [dcor](https://dcor.readthedocs.io/en/latest/index.html)
- [numpy](https://numpy.org/)
- [pyHSICLasso](https://github.com/riken-aip/pyHSICLasso)
- [stumpy](https://stumpy.readthedocs.io/en/latest/)

## Raison D'être :thought_balloon:

`tsuniverse` aims take a universe of time series and figure out features from that universe that can be used to predict a single time series.

## Architecture :triangular_ruler:

`tsuniverse` is a functional library, meaning that each phase of the feature extraction goes through functions without side-effects. It attempts to do as much multiprocessing as it can to make this process quicker. Each feature extraction is done in different phases, those phases are:

1. Pearson Correlations.
2. Mutual Information.
3. Spearmans Rho.
4. Kendalls Tau.
5. Distance Correlations.
6. HSIC.
7. Stumpy.

## Installation :inbox_tray:

This is a python package hosted on pypi, so to install simply run the following command:

`pip install tsuniverse`

or install using this local repository:

`python setup.py install --old-and-unmanageable`

## Usage example :eyes:

The use of `tsuniverse` is entirely through code due to it being a library. It attempts to hide most of its complexity from the user, so it only has a few functions of relevance in its outward API.

### Generating Features

To generate features:

```python
import datetime

import pandas as pd

from tsuniverse.process import process

df = ... # Your timeseries dataframe
features = process(df)
```

This will produce a list of features that you can produce with [timeseries-features](https://github.com/8W9aG/timeseries-features).

## License :memo:

The project is available under the [MIT License](LICENSE).
