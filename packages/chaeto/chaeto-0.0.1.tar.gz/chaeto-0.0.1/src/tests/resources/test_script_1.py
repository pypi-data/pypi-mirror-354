"""Script for testing."""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "polars==1.30.0",
#     "numpy==2.2.3",
# ]
# ///
import numpy as np
import polars as pl

if __name__ == '__main__':
    dframe = pl.DataFrame({"r": [0.01, -0.02, 0.015, 0.005, -0.01]})
    r_np = dframe["r"].to_numpy()
    sharpe = [np.nan if i < 3 else r_np[i - 3:i].mean() / r_np[i - 3:i].std(ddof=1) for i in range(len(r_np))]
    dframe = dframe.with_columns(pl.Series("sharpe", sharpe))
