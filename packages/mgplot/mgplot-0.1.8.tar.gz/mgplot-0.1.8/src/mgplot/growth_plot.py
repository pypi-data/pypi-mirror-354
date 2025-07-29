"""
growth_plot.py:
plot period and annual/through-the-year growth rates on the same axes.
- calc_growth()
- growth_plot()
- series_growth_plot()
"""

# --- imports
from typing import Final, Any
from pandas import Series, DataFrame, Period, PeriodIndex, period_range
from numpy import nan
from matplotlib.pyplot import Axes
from tabulate import tabulate

from mgplot.bar_plot import bar_plot
from mgplot.line_plot import line_plot
from mgplot.axis_utils import map_periodindex
from mgplot.test import prepare_for_test
from mgplot.settings import DataT
from mgplot.axis_utils import set_labels
from mgplot.utilities import check_clean_timeseries, constrain_data
from mgplot.kw_type_checking import (
    validate_kwargs,
    report_kwargs,
    validate_expected,
    ExpectedTypeDict,
)
from mgplot.keyword_names import (
    # - common
    AX,
    REPORT_KWARGS,
    LABEL_SERIES,
    MAX_TICKS,
    WIDTH,
    COLOR,
    STYLE,
    ANNOTATE,
    ANNOTATE_COLOR,
    ROUNDING,
    FONTSIZE,
    FONTNAME,
    ROTATION,
    # - line related
    LINE_WIDTH,
    LINE_COLOR,
    LINE_STYLE,
    ANNOTATE_LINE,
    LINE_ROUNDING,
    LINE_FONTSIZE,
    LINE_FONTNAME,
    LINE_ANNO_COLOR,
    # - bar related
    ANNOTATE_BARS,
    BAR_ROUNDING,
    BAR_ROTATION,
    BAR_WIDTH,
    BAR_COLOR,
    BAR_ANNO_COLOR,
    BAR_FONTSIZE,
    BAR_FONTNAME,
    PLOT_FROM,
    ABOVE,
)

# --- constants
type TransitionKwargs = dict[str, tuple[str, Any]]

# - overarching constants
ANNUAL = "annual"
PERIODIC = "periodic"

# - constants for the line plot
# - transition of kwargs from growth_plot to line_plot
common_transitions: TransitionKwargs = {
    # arg-to-growth_plot : (arg-to-line_plot, default_value)
    LABEL_SERIES: (LABEL_SERIES, True),
    AX: (AX, None),
    MAX_TICKS: (MAX_TICKS, None),
    PLOT_FROM: (PLOT_FROM, None),
    REPORT_KWARGS: (REPORT_KWARGS, None),
}

to_line_plot: TransitionKwargs = common_transitions | {
    # arg-to-growth_plot : (arg-to-line_plot, default_value)
    LINE_WIDTH: (WIDTH, None),
    LINE_COLOR: (COLOR, "darkblue"),
    LINE_STYLE: (STYLE, None),
    ANNOTATE_LINE: (ANNOTATE, True),
    LINE_ROUNDING: (ROUNDING, None),
    LINE_FONTSIZE: (FONTSIZE, None),
    LINE_FONTNAME: (FONTNAME, None),
    LINE_ANNO_COLOR: (ANNOTATE_COLOR, None),
}

# - constants for the bar plot
to_bar_plot: TransitionKwargs = common_transitions | {
    # arg-to-growth_plot : (arg-to-bar_plot, default_value)
    BAR_WIDTH: (WIDTH, 0.8),
    BAR_COLOR: (COLOR, "#dd0000"),
    ANNOTATE_BARS: (ANNOTATE, True),
    BAR_ROUNDING: (ROUNDING, None),
    ABOVE: (ABOVE, False),
    BAR_ROTATION: (ROTATION, None),
    BAR_FONTSIZE: (FONTSIZE, None),
    BAR_FONTNAME: (FONTNAME, None),
    BAR_ANNO_COLOR: (ANNOTATE_COLOR, None),
}

GROWTH_KW_TYPES: Final[ExpectedTypeDict] = {
    # --- options passed to the line plot
    LINE_WIDTH: (float, int),
    LINE_COLOR: str,
    LINE_STYLE: str,
    ANNOTATE_LINE: (type(None), bool),  # None, True
    LINE_ROUNDING: (bool, int),  # None, True or rounding
    LINE_FONTSIZE: (str, int, float),  # fontsize for the line annotations
    LINE_FONTNAME: str,  # font name for the line annotations
    LINE_ANNO_COLOR: (str, bool, type(None)),  # color for the line annotations
    # --- options passed to the bar plot
    ANNOTATE_BARS: (type(None), bool),
    BAR_FONTSIZE: (str, int, float),
    BAR_FONTNAME: str,
    BAR_ROUNDING: (bool, int),
    BAR_WIDTH: float,
    BAR_COLOR: str,
    BAR_ANNO_COLOR: (str, type(None)),
    BAR_ROTATION: (int, float),
    ABOVE: bool,
    # --- common options
    AX: (Axes, type(None)),
    PLOT_FROM: (type(None), Period, int),
    LABEL_SERIES: (bool),
    MAX_TICKS: int,
}
validate_expected(GROWTH_KW_TYPES, "growth_plot")

SERIES_GROWTH_KW_TYPES: Final[ExpectedTypeDict] = {
    "ylabel": (str, type(None)),
} | GROWTH_KW_TYPES
validate_expected(SERIES_GROWTH_KW_TYPES, "growth_plot")


# --- functions
def calc_growth(series: Series) -> DataFrame:
    """
    Calculate annual and periodic growth for a pandas Series,
    where the index is a PeriodIndex.

    Args:
    -   series: A pandas Series with an appropriate PeriodIndex.

    Returns a two column DataFrame:

    Raises
    -   TypeError if the series is not a pandas Series.
    -   TypeError if the series index is not a PeriodIndex.
    -   ValueError if the series is empty.
    -   ValueError if the series index does not have a frequency of Q, M, or D.
    -   ValueError if the series index has duplicates.
    """

    # --- sanity checks
    if not isinstance(series, Series):
        raise TypeError("The series argument must be a pandas Series")
    if not isinstance(series.index, PeriodIndex):
        raise TypeError("The series index must be a pandas PeriodIndex")
    if series.empty:
        raise ValueError("The series argument must not be empty")
    if series.index.freqstr[0] not in ("Q", "M", "D"):
        raise ValueError("The series index must have a frequency of Q, M, or D")
    if series.index.has_duplicates:
        raise ValueError("The series index must not have duplicate values")

    # --- ensure the index is complete and the date is sorted
    complete = period_range(start=series.index.min(), end=series.index.max())
    series = series.reindex(complete, fill_value=nan)
    series = series.sort_index(ascending=True)

    # --- calculate annual and periodic growth
    ppy = {"Q": 4, "M": 12, "D": 365}[PeriodIndex(series.index).freqstr[:1]]
    annual = series.pct_change(periods=ppy) * 100
    periodic = series.pct_change(periods=1) * 100
    periodic_name = {4: "Quarterly", 12: "Monthly", 365: "Daily"}[ppy] + " Growth"
    return DataFrame(
        {
            "Annual Growth": annual,
            periodic_name: periodic,
        }
    )


def package_kwargs(mapping: TransitionKwargs, **kwargs: Any) -> dict[str, Any]:
    """
    Package the keyword arguments for plotting functions.
    Substitute defaults where arguments are not provided
    (unless the default is None).

    Args:
    -   mapping: A mapping of original keys to  a tuple of (new-key, default value).
    -   kwargs: The original keyword arguments.

    Returns:
    -   A dictionary with the packaged keyword arguments.
    """
    return {
        v[0]: kwargs.get(k, v[1])
        for k, v in mapping.items()
        if k in kwargs or v[1] is not None
    }


def growth_plot(
    data: DataT,
    **kwargs,
) -> Axes:
    """
    Plot annual growth (as a line) and periodic growth (as bars)
    on the same axes.

    Args:
    -   data: A pandas DataFrame with two columns:
    -   kwargs:
        -   line_width: The width of the line (default is 2).
        -   line_color: The color of the line (default is "darkblue").
        -   line_style: The style of the line (default is "-").
        -   annotate_line: None | bool | int | str - fontsize to annotate
            the line (default is "small", which means the line is annotated with
            small text).
        -   rounding: None | bool | int - the number of decimal places to round
            the line (default is 0).
        -   bar_width: The width of the bars (default is 0.8).
        -   bar_color: The color of the bars (default is "indianred").
        -   annotate_bar: None | int | str - fontsize to annotate the bars
            (default is "small", which means the bars are annotated with
            small text).
        -   bar_rounding: The number of decimal places to round the
            annotations to (default is 1).
        -   plot_from: None | Period | int -- if:
            -   None: the entire series is plotted
            -   Period: the plot starts from this period
            -   int: the plot starts from this +/- index position
        -   max_ticks: The maximum number of ticks to show on the x-axis
            (default is 10).

    Returns:
    -   axes: The matplotlib Axes object.

    Raises:
    -   TypeError if the annual and periodic arguments are not pandas Series.
    -   TypeError if the annual index is not a PeriodIndex.
    -   ValueError if the annual and periodic series do not have the same index.
    """

    # --- check the kwargs
    me = "growth_plot"
    report_kwargs(called_from=me, **kwargs)
    kwargs = validate_kwargs(GROWTH_KW_TYPES, me, **kwargs)

    # --- data checks
    data = check_clean_timeseries(data, me)
    if len(data.columns) != 2:
        raise TypeError("The data argument must be a pandas DataFrame with two columns")
    data, kwargs = constrain_data(data, **kwargs)

    # --- get the series of interest ...
    annual = data[data.columns[0]]
    periodic = data[data.columns[1]]

    # --- series names
    annual.name = "Annual Growth"
    periodic.name = {"M": "Monthly", "Q": "Quarterly", "D": "Daily"}[
        PeriodIndex(periodic.index).freqstr[:1]
    ] + " Growth"

    # --- convert PeriodIndex periodic growth data to integer indexed data.
    saved_pi = map_periodindex(periodic)
    if saved_pi is not None:
        periodic = saved_pi[0]  # extract the reindexed DataFrame

    # --- simple bar chart for the periodic growth
    if BAR_ANNO_COLOR not in kwargs or kwargs[BAR_ANNO_COLOR] is None:
        kwargs[BAR_ANNO_COLOR] = "black" if kwargs.get(ABOVE, False) else "white"
    selected = package_kwargs(to_bar_plot, **kwargs)
    axes = bar_plot(periodic, **selected)

    # --- and now the annual growth as a line
    selected = package_kwargs(to_line_plot, **kwargs)
    line_plot(annual, ax=axes, **selected)

    # --- fix the x-axis labels
    if saved_pi is not None:
        set_labels(axes, saved_pi[1], kwargs.get("max_ticks", 10))

    # --- and done ...
    return axes


def series_growth_plot(
    data: DataT,
    **kwargs,
) -> Axes:
    """
    Plot annual and periodic growth in percentage terms from
    a pandas Series, and finalise the plot.

    Args:
    -   data: A pandas Series with an appropriate PeriodIndex.
    -   kwargs:
        -   takes the same kwargs as for growth_plot()
    """

    # --- check the kwargs
    me = "series_growth_plot"
    report_kwargs(called_from=me, **kwargs)
    kwargs = validate_kwargs(SERIES_GROWTH_KW_TYPES, me, **kwargs)

    # --- sanity checks
    if not isinstance(data, Series):
        raise TypeError(
            "The data argument to series_growth_plot() must be a pandas Series"
        )

    # --- calculate growth and plot - add ylabel
    ylabel: str | None = kwargs.pop("ylabel", None)
    if ylabel is not None:
        print(f"Did you intend to specify a value for the 'ylabel' in {me}()?")
    ylabel = "Growth (%)" if ylabel is None else ylabel
    growth = calc_growth(data)
    ax = growth_plot(growth, **kwargs)
    ax.set_ylabel(ylabel)
    return ax


# --- test code
if __name__ == "__main__":
    print("Testing")
    prepare_for_test("growth_plot")
    series_ = Series([1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])
    series_.index = period_range("2020Q1", periods=len(series_), freq="Q")
    growth_ = calc_growth(series_)
    text_ = tabulate(growth_, headers="keys", tablefmt="pipe")  # type: ignore[arg-type]
    print(text_)
