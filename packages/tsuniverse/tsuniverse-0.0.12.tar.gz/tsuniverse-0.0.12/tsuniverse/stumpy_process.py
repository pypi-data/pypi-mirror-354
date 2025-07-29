"""The stumpy process function."""

# pylint: disable=duplicate-code,invalid-name
from typing import Any, Iterator

import numpy as np
import pandas as pd
import stumpy  # type: ignore
from timeseriesfeatures.feature import FEATURE_TYPE_LAG  # type: ignore
from timeseriesfeatures.feature import Feature  # type: ignore
from timeseriesfeatures.transform import Transform  # type: ignore
from timeseriesfeatures.transforms import TRANSFORMS  # type: ignore

_STUMPY_CACHE: dict[str, Feature] = {}


def stumpy_similarity_positive_lags(
    predictor: pd.Series,
    predictand: pd.Series,
    max_window: int,
    predictor_transform: Transform,
    column: str,
) -> Feature | None:
    """Use STUMP to find the most similar subsequence via matrix profile."""
    predictor = TRANSFORMS[predictor_transform](predictor).dropna()
    predictand = predictand.dropna()

    # Convert to numpy
    A = predictand.values.astype(np.float64)
    B = predictor.values.astype(np.float64)

    # Use the smallest viable window if too short
    m = min(max_window, len(A), len(B)) - 1
    if m < 4:
        return None

    profile = stumpy.stump(A, m, B)

    min_idx = np.argmin(profile[:, 0])
    best_dist = profile[min_idx, 0]
    match_idx = profile[min_idx, 1]

    # Estimate lag (in this case: where does the best match in B align with A?)
    lag = abs(min_idx - profile[min_idx, 1]) if not np.isnan(profile[min_idx, 1]) else 0

    if np.isnan(best_dist) or np.isinf(best_dist):
        return None
    
    lag = min_idx - int(match_idx)
    if lag <= 0:
        lag = 1

    return Feature(
        feature_type=FEATURE_TYPE_LAG,
        columns=[column],
        value1=int(lag),
        transform=str(predictor_transform),
        rank_value=-best_dist,  # negative so that higher rank is better
        rank_type="stumpy",
    )


def stumpy_process(
    df: pd.DataFrame,
    predictand: str,
    max_window: int,
    pool: Any,
) -> Iterator[Feature]:
    """Process the dataframe for tsuniverse features using STUMP similarity."""
    predictors = df.columns.values.tolist()
    cached_predictors = []

    for predictor in predictors:
        for transform in TRANSFORMS:
            key = "_".join(sorted([predictor, transform, predictand]))
            feature = _STUMPY_CACHE.get(key)
            if feature is not None:
                yield feature
                cached_predictors.append(predictor)

    for transform in TRANSFORMS:
        for feature in pool.starmap(
            stumpy_similarity_positive_lags,
            [
                (df[x], df[predictand], max_window, transform, x)
                for x in df.columns.values.tolist()
                if x != predictand and x not in cached_predictors
            ],
        ):
            if feature is None:
                continue
            key = "_".join(
                sorted(
                    [
                        feature["columns"][0],
                        transform,
                        predictand,
                    ]
                )
            )
            _STUMPY_CACHE[key] = feature
            yield feature
