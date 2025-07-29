import io
import math
import base64
from datetime import datetime
from io import BytesIO
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def sparta_1914efb7e8(obj):
    if isinstance(obj, dict):
        return {k: sparta_1914efb7e8(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sparta_1914efb7e8(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj


def sparta_8fcab127bf(series: pd.Series) ->bool:
    try:
        converted = pd.to_numeric(series, errors='coerce')
        return pd.api.types.is_numeric_dtype(converted) and not converted.isna(
            ).all()
    except Exception:
        return False


def sparta_c9ea6b80d8(series: pd.Series) ->bool:
    if pd.api.types.is_categorical_dtype(series):
        return True
    if pd.api.types.is_object_dtype(series):
        unique_ratio = series.nunique(dropna=False) / max(1, len(series))
        return unique_ratio < 0.1 or series.nunique(dropna=False) <= 20
    return False


def sparta_88b6102bcf(series: pd.Series) ->bool:
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    try:
        converted = pd.to_datetime(series, errors='coerce')
        return converted.notna().mean() > 0.9
    except Exception:
        return False


def sparta_eaff4496a7(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def sparta_1cc28d8e2d(fig, B_DARK_THEME=False):
    """
    
    """
    font_scale = 1.1
    legend_color = '#757575'
    legend_background = 'white'
    grid_color = '#343434'
    axis_tick = '#dcdcdc'
    axis_labels = '#757575'
    axis_title_label_color = '#333333'
    title_color = 'black'
    subtitle_color = 'black'
    if B_DARK_THEME:
        grid_color = '#dddddd'
        axis_title_label_color = 'white'
        axis_labels = '#c1c1c1'
        axis_tick = '#dddddd'
        legend_color = '#333333'
        legend_background = 'white'
        title_color = 'white'
        subtitle_color = 'white'
    for text_obj in fig.findobj(match=lambda x: hasattr(x, 'set_fontsize')):
        current_size = text_obj.get_fontsize()
        text_obj.set_fontsize(current_size * font_scale)
    for ax in fig.axes:
        ax.set_facecolor('white')
        ax.grid(True, color=grid_color, linewidth=0.25, linestyle=':')
        ax.tick_params(colors=axis_tick)
        if ax.title:
            ax.set_title(ax.get_title(), fontsize=16, color=
                axis_title_label_color, fontname='Arial')
        if ax.xaxis.label:
            ax.xaxis.label.set_color(axis_title_label_color)
        if ax.yaxis.label:
            ax.yaxis.label.set_color(axis_title_label_color)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_color(axis_labels)
        for line in ax.get_lines():
            line.set_linewidth(1.5)
        for spine in ax.spines.values():
            spine.set_visible(False)
        legend = ax.get_legend()
        if legend:
            legend.get_frame().set_facecolor(legend_background)
            if B_DARK_THEME:
                legend.get_frame().set_edgecolor('none')
            else:
                legend.get_frame().set_edgecolor('#dcdcdc')
                legend.get_frame().set_linewidth(1.0)
            for text in legend.get_texts():
                text.set_fontname('Arial')
                text.set_color(legend_color)
    if hasattr(fig, '_suptitle') and fig._suptitle is not None:
        fig._suptitle.set_color(title_color)
    fig.patch.set_facecolor('white')
    fig.set_size_inches(10, 6)
    return fig


def sparta_3706e613e0(data_df):
    """
    
    """
    data_df.index = data_df.index.astype(str)
    return data_df

#END OF QUBE
