import re
from typing import Optional, Iterable
from ansiplot.palette import Pretty
from ansiplot.utils import enable_ansi


class Canvas:
    """Generic class of operations that make sense for a canvas"""

    def __init__(self, palette=None, symbol_state=0):
        self.symbol_state = symbol_state
        self.legend = ""
        self.palette = Pretty if palette is None else palette

    def current_color(self):
        return self.palette.colors[self.symbol_state % len(self.palette.colors)]

    def current_colorless_symbol(self):
        return self.palette.symbols[self.symbol_state % len(self.palette.symbols)]

    def _prepare_symbol(self, title, symbol):
        if symbol is None:
            symbol = self.current_color() + self.current_colorless_symbol()
            self.symbol_state += 1
        else:
            symbol = f"{self.palette.reset_color}{symbol}"
        if title is not None:
            self.legend += f"\n {symbol} {self.palette.reset_color}{title}"
        return symbol

    @property
    def same(self):
        self.symbol_state -= 1
        return self

    def point(self, x, y, title: Optional[str] = None, symbol: Optional[str] = None):
        """Plots a single point."""
        x = float(x)
        y = float(y)
        self.scatter([x], [y], title, symbol)
        return self

    def scatter(self, x, y, title: Optional[str] = None, symbol: Optional[str] = None):
        """Plots a collection of points."""
        symbol = self._prepare_symbol(title, symbol)
        # ensure conversion to a format that we know about
        x = [float(value) for value in x]
        y = [float(value) for value in y]
        self._scatter(x, y, symbol=symbol)
        return self

    def plot(self, x, y, title: Optional[str] = None, symbol: Optional[str] = None):
        """Plots a continuous curve."""
        symbol = self._prepare_symbol(title, symbol)
        # ensure conversion to a format that we know about
        x = [float(value) for value in x]
        y = [float(value) for value in y]
        self._plot(x, y, symbol=symbol)
        return self

    def bar(self, x, y, title: Optional[str] = None, symbol: Optional[str] = None):
        """Plots a vertical var on position x that go"""
        symbol = self._prepare_symbol(title, symbol)
        if isinstance(y, Iterable):
            ymin, y = y
        elif y is None:
            ymin = 0
        else:
            ymin = 0
            y = float(y)
        x = float(x)
        self._bar(x, y, symbol=symbol, ymin=ymin)
        return self

    def hbar(self, x, y, title: Optional[str] = None, symbol: Optional[str] = None):
        """Plots a vertical var on position x that go"""
        symbol = self._prepare_symbol(title, symbol)
        if isinstance(x, Iterable):
            xmin, x = x
        elif x is None:
            xmin = 0
        else:
            xmin = 0
            x = float(x)
        y = float(y)
        self._hbar(x, y, symbol=symbol, xmin=xmin)
        return self

    def text(self, legend: bool = True, colorless: bool = False):
        plot = self._text()
        if legend:
            plot += self.legend
        else:
            plot += "\n"
        if colorless:
            plot = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", plot)
        return plot

    def show(self, legend: bool = True, colorless: bool = False):
        print(self.text(legend=legend, colorless=colorless))

    def __str__(self):
        return self.text()

    def _plot(self, x, y, symbol='*'):
        for xi, yi in zip(x, y):
            self.plot_point(xi, yi, symbol=symbol)

    def plot_point(self, x, y, symbol='*'):
        """Plot a single (x, y) point using hbar"""
        self.hbar(x, y, symbol=symbol)

    def _hbar(self, x, y, symbol='*', xmin=0):
        """Basic horizontal bar from xmin to x at y"""
        x, y = float(x), float(y)
        if x < xmin:
            x, xmin = xmin, x
        x = int(x * 2)  # scale for terminal width
        xmin = int(xmin * 2)
        bar = symbol * max(x - xmin, 1)
        print(" " * xmin + bar)

    def _text(self):
        return ""

    def vertical_histogram(self, data, bins=20, symbol='█'):
        """
        Added by Ahmet Sahiner - CS231
        Prints vertical histogram using ASCII bars
        """
        import numpy as np
        counts, edges = np.histogram(data, bins=bins)
        max_height = max(counts)
        scaled = [int(count * 20 / max_height) for count in counts]

        for h in reversed(range(1, 21)):
            row = ""
            for height in scaled:
                row += symbol if height >= h else " "
                row += " "
            print(row)

    def bar_chart_labels(self, labels, values, symbol='='):
        """
        Added by Ahmet Sahiner - Shows horizontal bar chart with labels
        """
        max_len = max(len(label) for label in labels)
        max_val = max(values)
        scaled = [int(val * 40 / max_val) for val in values]

        for label, bar_len in zip(labels, scaled):
            print(f"{label.ljust(max_len)} | {symbol * bar_len}")

    def scatter_points(self, x_vals, y_vals, symbol='*'):
        """
        Added by Ahmet Sahiner - Scatter plot in terminal using ASCII points
        """
        for x, y in zip(x_vals, y_vals):
            print(" " * int(x * 2) + symbol + f" ({x:.1f},{y:.1f})")

