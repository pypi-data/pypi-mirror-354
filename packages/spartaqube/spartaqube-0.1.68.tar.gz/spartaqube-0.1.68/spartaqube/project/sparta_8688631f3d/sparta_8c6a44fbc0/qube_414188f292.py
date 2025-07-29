import io
import math
import random
import base64
from datetime import datetime
from io import BytesIO
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from project.sparta_8688631f3d.sparta_8c6a44fbc0.qube_a1901df5d7 import format_plot_style


def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj


def is_numeric_column(series: pd.Series) ->bool:
    try:
        converted = pd.to_numeric(series, errors='coerce')
        return pd.api.types.is_numeric_dtype(converted) and not converted.isna(
            ).all()
    except Exception:
        return False


def is_categorical_column(series: pd.Series) ->bool:
    if pd.api.types.is_categorical_dtype(series):
        return True
    if pd.api.types.is_object_dtype(series):
        unique_ratio = series.nunique(dropna=False) / max(1, len(series))
        return unique_ratio < 0.1 or series.nunique(dropna=False) <= 20
    return False


def is_datetime_column(series: pd.Series) ->bool:
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    try:
        converted = pd.to_datetime(series, errors='coerce')
        return converted.notna().mean() > 0.9
    except Exception:
        return False


def to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def plot_correlation_matrix_base64(df: pd.DataFrame, B_DARK_THEME=False) ->str:
    """
    Generate a base64-encoded correlation matrix heatmap for numeric columns in a DataFrame."""
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.shape[1] < 2:
        return ''
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, linewidths=0.5,
        linecolor='gray', ax=ax)
    ax.set_title('Correlation Matrix Heatmap')
    plt.tight_layout()
    fig = format_plot_style(fig, B_DARK_THEME)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return image_base64


def plot_pairwise_correlation_base64(df: pd.DataFrame, B_DARK_THEME=False
    ) ->str:
    """
    Generate a base64-encoded correlation matrix heatmap for numeric columns in a DataFrame."""
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.shape[1] < 2:
        return ''
    pair_plot = sns.pairplot(numeric_df, diag_kind='hist')
    pair_plot.fig.suptitle('Pairplot: Distributions & Relationships', y=1.02)
    buf = io.BytesIO()
    pair_plot.fig.savefig(buf, format='png', bbox_inches='tight',
        transparent=True)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(pair_plot.fig)
    return image_base64


def analyze_columns(df: pd.DataFrame, columns: list[str], B_DARK_THEME=False
    ) ->dict:
    """
    Returns full columns analysis of a dataframe
    """
    df['__sq_index__'] = df.index
    columns = ['__sq_index__'] + columns
    report = {}
    numeric_df = pd.DataFrame()
    numeric_col_dict = dict()
    nb_numeric = 0
    nb_categorical = 0
    nb_datetime = 0
    for col in columns:
        if is_numeric_column(df[col]):
            nb_numeric += 1
        elif is_categorical_column(df[col]):
            nb_categorical += 1
        elif is_datetime_column(df[col]):
            nb_datetime += 1
    report['Summary'] = dict()
    shape_rel = {'num_rows': df.shape[0], 'num_columns': df.shape[1],
        'num_numeric': nb_numeric, 'num_categorical': nb_categorical,
        'num_datetime': nb_datetime}
    report['Summary']['shape_rel'] = shape_rel
    dataset_summary = {'total_cells': df.size, 'non_null_cells': int(df.notnull().sum().sum()), 'null_cells': int(df.isnull().sum().sum()),
        'null_percent': round(df.isnull().sum().sum() / df.size * 100, 2),
        'memory_usage_MB': round(df.memory_usage(deep=True).sum() / 1024 **
        2, 2), 'density_percent': round(df.notnull().sum().sum() / df.size *
        100, 2)}
    report['Summary']['dataset_summary'] = dataset_summary
    print('df stats')
    print(df)
    for col in columns:
        is_col_numeric = is_numeric_column(df[col])
        numeric_col_dict[col] = is_col_numeric
        numeric_series = None
        if is_col_numeric:
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            numeric_df[col] = numeric_series
        col_data = df[col]
        analysis = {}
        analysis['type'] = col_data.dtype.name
        analysis['missing'] = int(col_data.isnull().sum())
        analysis['unique'] = col_data.nunique()
        analysis['description'] = col_data.describe(include='all').to_dict()
        try:
            col_numeric = numeric_series
        except Exception:
            col_numeric = pd.Series(dtype='float64')
        analysis['description'] = sanitize_for_json(col_data.describe(
            include='all').to_dict())
        if is_col_numeric:
            Q1 = col_numeric.quantile(0.25)
            Q3 = col_numeric.quantile(0.75)
            IQR = Q3 - Q1
            try:
                min_val = float(sanitize_for_json(col_numeric.min()))
            except:
                min_val = 'N/A'
            try:
                q1_val = float(sanitize_for_json(Q1))
            except:
                q1_val = 'N/A'
            try:
                median_val = float(sanitize_for_json(col_numeric.median()))
            except:
                median_val = 'N/A'
            try:
                q3_val = float(sanitize_for_json(Q3))
            except:
                q3_val = 'N/A'
            try:
                max_val = float(sanitize_for_json(col_numeric.max()))
            except:
                max_val = 'N/A'
            try:
                iqr_val = float(sanitize_for_json(IQR))
            except:
                iqr_val = 'N/A'
            try:
                mean_val = float(sanitize_for_json(col_numeric.mean()))
            except:
                mean_val = 'N/A'
            try:
                std_val = float(sanitize_for_json(col_numeric.std()))
            except:
                std_val = 'N/A'
            try:
                skew_val = float(sanitize_for_json(col_numeric.skew()))
            except:
                skew_val = 'N/A'
            try:
                kurtosis_val = float(sanitize_for_json(col_numeric.kurt()))
            except:
                kurtosis_val = 'N/A'
            analysis['numeric_summary'] = {'min': min_val, 'Q1 (25%)':
                q1_val, 'median (50%)': median_val, 'Q3 (75%)': q3_val,
                'max': max_val, 'IQR': iqr_val, 'mean': mean_val, 'std':
                std_val, 'skew': skew_val, 'kurtosis': kurtosis_val}
            try:
                adf_dict = adf_test(numeric_series.tolist())
                kpss_dict = kpss_test(numeric_series.tolist())
                analysis['adf'] = adf_dict
                analysis['kpss'] = kpss_dict
            except:
                pass
        if col_data.nunique(dropna=False) <= 20:
            analysis['value_counts'] = sanitize_for_json(col_data.value_counts(dropna=False).to_dict())
        data_quality = {'missing_values': int(col_data.isnull().sum()),
            'missing_percent': round(col_data.isnull().mean() * 100, 2),
            'is_constant': col_data.nunique(dropna=False) <= 1,
            'duplicate_rows': int(col_data.duplicated().sum()),
            'mixed_types': col_data.apply(type).nunique() > 1}
        analysis['data_quality'] = data_quality
        if is_col_numeric:
            suggestion = 'No suggestions'
            suggestion_type = 0
            if abs(col_numeric.skew()) > 1.5:
                suggestion = 'Highly skewed, consider log transform.'
                suggestion_type = 1
            if col_numeric.nunique() < 5:
                suggestion = 'Very few unique values, maybe categorical?'
                suggestion_type = 1
            smart_flags = suggestion
            top_freq = col_numeric.value_counts(normalize=True, dropna=False
                ).values[0]
            if top_freq > 0.8:
                smart_flags = 'Highly imbalanced column (most frequent > 80%).'
                suggestion_type = 1
            analysis['smart_flags'] = smart_flags
            analysis['suggestion_type'] = suggestion_type
        plotting_color = '#757575'
        plt.rcParams.update({'axes.edgecolor': plotting_color,
            'xtick.color': plotting_color, 'ytick.color': plotting_color,
            'text.color': plotting_color, 'axes.labelcolor': plotting_color,
            'figure.facecolor': 'none', 'axes.facecolor': 'none',
            'savefig.facecolor': 'none', 'savefig.edgecolor': 'none'})
        fig, ax = plt.subplots(figsize=(8, 6))
        col_title = col
        if col == '__sq_index__':
            col_title = 'Index'
        if is_col_numeric:
            data = col_numeric.dropna()
            sns.histplot(data, kde=True, ax=ax, edgecolor='none')
            ax.set_title(f'Histogram: {col_title}')
            ax.set_xlabel(col_title)
        else:
            col_data.value_counts(dropna=False).head(10).plot(kind='bar', ax=ax
                )
            ax.set_title(f'Top Categories: {col_title}')
            ax.set_xlabel(col_title)
        plt.tight_layout()
        fig = format_plot_style(fig, B_DARK_THEME)
        histogram_base64 = to_base64(fig)
        if is_col_numeric:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x=data, ax=ax, whiskerprops=dict(color=
                plotting_color), capprops=dict(color=plotting_color),
                medianprops=dict(color=plotting_color), flierprops=dict(
                markerfacecolor=plotting_color, markeredgecolor=plotting_color)
                )
            ax.set_title(f'Boxplot: {col}')
            mean_val = data.mean()
            median_val = data.median()
            ax.text(mean_val, 0.05, f'Mean: {mean_val:.2f}', color='red',
                ha='center', va='bottom', fontsize=10)
            ax.text(median_val, -0.05, f'Median: {median_val:.2f}', color=
                'red', ha='center', va='top', fontsize=10)
            ax.set_yticks([])
            plt.tight_layout()
            fig = format_plot_style(fig, B_DARK_THEME)
            analysis['boxplot_base64'] = to_base64(fig)
        analysis['histogram_base64'] = histogram_base64
        report[col] = sanitize_for_json(analysis)
    print('report keys')
    print(report.keys())
    return report


def analyze_columns_corr(df: pd.DataFrame, columns: list[str], B_DARK_THEME
    =False) ->dict:
    """
    Correlation chart (separated from the function above because plot_pairwise_correlation_base64 can be slow)
    """
    report = {}
    numeric_df = pd.DataFrame()
    for col in columns:
        is_col_numeric = is_numeric_column(df[col])
        if is_col_numeric:
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            numeric_df[col] = numeric_series
    if numeric_df.shape[1] > 1:
        report['_correlation_matrix'] = dict()
        report['_correlation_matrix']['plot_base64'
            ] = plot_correlation_matrix_base64(numeric_df, B_DARK_THEME=
            B_DARK_THEME)
        report['_correlation_matrix']['pairwise_plot_base64'
            ] = plot_pairwise_correlation_base64(numeric_df, B_DARK_THEME=
            B_DARK_THEME)
    return report


def adf_test(data: list, title=''):
    series = pd.Series(data).dropna()
    result = adfuller(series.dropna(), autolag='AIC')
    res_dict = {'adf_statistic': float(result[0]), 'p_value': float(result[
        1]), 'is_stationary': bool(result[1] < 0.05)}
    for key, value in result[4].items():
        res_dict[f'Critical Value ({key})'] = float(value)
    return res_dict


def kpss_test(data: list, title=''):
    series = pd.Series(data).dropna()
    result = kpss(series, regression='ct', nlags='auto')
    res_dict = {'adf_statistic': float(result[0]), 'p_value': float(result[
        1]), 'is_stationary': bool(result[1] > 0.05)}
    for key, value in result[3].items():
        res_dict[f'Critical Value ({key})'] = float(value)
    return res_dict


def simple_scatter_with_trendline(df: pd.DataFrame, x_col: str, y_col: str,
    B_DARK_THEME=False) ->dict:
    result = {}
    cols_all = [x_col]
    if y_col not in cols_all:
        cols_all += [y_col]
    df = df[cols_all].dropna().copy()
    X = df[x_col]
    X = pd.to_numeric(X, errors='coerce')
    y = df[y_col]
    y = pd.to_numeric(y, errors='coerce')
    print('x_col >> ')
    print(x_col)
    print('y_col >> ')
    print(y_col)
    print('y')
    print(y)
    x_mean = X.mean()
    y_mean = y.mean()
    cov = ((X - x_mean) * (y - y_mean)).sum()
    var_x = ((X - x_mean) ** 2).sum()
    slope = cov / var_x
    intercept = y_mean - slope * x_mean
    trend = slope * X + intercept
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=X, y=y, ax=ax, label='Data')
    ax.plot(X, trend, color='red', label=
        f'Trendline\ny = {slope:.2f}x + {intercept:.2f}')
    ax.set_title(f'Scatter Plot with Regression Line\n{y_col} vs {x_col}',
        color='#757575')
    ax.set_xlabel(x_col, color='#757575')
    ax.set_ylabel(y_col, color='#757575')
    ax.tick_params(axis='x', colors='#757575')
    ax.tick_params(axis='y', colors='#757575')
    for spine in ['left', 'bottom', 'top', 'right']:
        ax.spines[spine].set_color('#757575')
    ax.legend()
    fig = format_plot_style(fig, B_DARK_THEME=B_DARK_THEME)
    result['scatter_plot'] = to_base64(fig)
    result['regression_equation'] = f'y = {slope:.4f} * x + {intercept:.4f}'
    return result


def train_test_split_custom(X, y=None, test_size=0.25, shuffle=True,
    random_seed=None):
    """
    Splits arrays or matrices into random train and test subsets.Parameters:
    - X: list or array-like (features)
    - y: list or array-like (labels), optional
    - test_size: float (fraction of data to use for test set)
    - shuffle: bool (whether to shuffle before splitting)
    - random_seed: int (random seed for reproducibility)

    Returns:
    - X_train, X_test[, y_train, y_test]
    """
    if random_seed is not None:
        random.seed(random_seed)
    n_samples = len(X)
    indices = list(range(n_samples))
    if shuffle:
        random.shuffle(indices)
    test_size_int = int(n_samples * test_size)
    test_indices = indices[:test_size_int]
    train_indices = indices[test_size_int:]
    X_train = [X[i] for i in train_indices]
    X_test = [X[i] for i in test_indices]
    if y is not None:
        y_train = [y[i] for i in train_indices]
        y_test = [y[i] for i in test_indices]
        return X_train, X_test, y_train, y_test
    else:
        return X_train, X_test


def is_sklearn_installed():
    try:
        import sklearn
        return True
    except ImportError:
        return False


def multi_x_column_analysis(df: pd.DataFrame, x_cols: list[str], y_col: str,
    in_sample=True, test_size=0.2, window: int=30, B_DARK_THEME=False) ->dict:
    """'
    Linear Regression
    """
    results = {}
    cols_all = x_cols.copy()
    if y_col not in cols_all:
        cols_all += [y_col]
    df = df[cols_all].dropna().copy()
    for col in cols_all:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()
    X = df[x_cols]
    y = df[y_col]
    if in_sample:
        X_train, X_test, y_train, y_test = X, X, y, y
    else:
        random_state = 42
        if is_sklearn_installed():
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y,
                test_size=test_size, random_state=random_state)
        else:
            X_train, X_test, y_train, y_test = train_test_split_custom(X, y,
                test_size=test_size, random_state=random_state)
    X_train_aug = X_train.copy()
    X_train_aug['Intercept'] = 1.0
    model_train = sm.OLS(y_train, X_train_aug).fit()
    beta_train = model_train.params
    X_test_aug = X_test.copy()
    X_test_aug['Intercept'] = 1.0
    y_test_pred = X_test_aug.dot(beta_train)
    X_full_aug = X.copy()
    X_full_aug['Intercept'] = 1.0
    model_full = sm.OLS(y, X_full_aug).fit()
    beta_full = model_full.params
    y_pred_full = X_full_aug.dot(beta_full)
    regression_eq = ' + '.join([f'{beta_full[col]:.4f} * {col}' for col in
        x_cols])
    regression_eq += f" + {beta_full['Intercept']:.4f}"
    results['regression_equation'] = f'y = {regression_eq}'
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(y.index, y.values, label='Actual', color='gray')
    ax.plot(y.index, y_pred_full.values, linestyle='--', label=
        'Predicted (Full Sample)', color='orange')
    ax.set_title('OLS: Full Sample Prediction')
    ax.set_xlabel('Index')
    ax.set_ylabel('Target')
    ax.legend()
    fig = format_plot_style(fig, B_DARK_THEME)
    results['full_pred_plot'] = to_base64(fig)
    if not in_sample:
        fig_test, ax_test = plt.subplots(figsize=(10, 5))
        ax_test.plot(y_test.index, y_test.values, label='Actual (Test)',
            color='gray')
        ax_test.plot(y_test.index, y_test_pred.values, linestyle='--',
            label='Predicted (Test)', color='blue')
        ax_test.set_title('OLS: Test Set Prediction')
        ax_test.set_xlabel('Index')
        ax_test.set_ylabel('Target')
        ax_test.legend()
        fig_test = format_plot_style(fig_test, B_DARK_THEME)
        results['test_pred_plot'] = to_base64(fig_test)
    rolling_betas = []
    rolling_alphas = []
    rolling_resid_stds = []
    idx_vals = []
    if len(df) > window:
        for i in range(window, len(df)):
            X_win = df[x_cols].iloc[i - window:i].copy()
            y_win = df[y_col].iloc[i - window:i].copy()
            X_win['Intercept'] = 1.0
            model_win = sm.OLS(y_win, X_win).fit()
            beta_win = model_win.params
            y_hat = X_win.dot(beta_win)
            resid = y_win - y_hat
            rolling_betas.append(beta_win[x_cols])
            rolling_alphas.append(beta_win['Intercept'])
            rolling_resid_stds.append(resid.std())
            idx_vals.append(df.index[i])
        beta_df = pd.DataFrame(rolling_betas, index=idx_vals)
        results['rolling_betas'] = dict()
        for col in x_cols:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(beta_df.index, beta_df[col], label=f'Rolling Beta: {col}')
            ax.axhline(beta_full[col], linestyle='--', color='red', label=
                f'Full Beta = {beta_full[col]:.2f}')
            ax.set_title(f'{window}-Window Rolling Beta — {col}', color=
                '#757575')
            ax.set_ylabel(y_col, color='#757575')
            ax.tick_params(axis='x', colors='#757575')
            ax.tick_params(axis='y', colors='#757575')
            for spine in ['left', 'bottom', 'top', 'right']:
                ax.spines[spine].set_color('#757575')
            ax.legend()
            fig = format_plot_style(fig, B_DARK_THEME)
            results['rolling_betas'][col] = {'img64': to_base64(fig),
                'rolling_betas_json': pd.DataFrame(beta_df[col]).to_json(
                orient='split')}
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(idx_vals, rolling_alphas, label='Rolling Alpha (Intercept)',
            color='purple')
        ax.axhline(beta_full['Intercept'], linestyle='--', color='red',
            label=f"Full Alpha = {beta_full['Intercept']:.2f}")
        ax.set_title(f'{window}-Window Rolling Intercept (Alpha)', color=
            '#757575')
        ax.set_ylabel(y_col, color='#757575')
        ax.tick_params(axis='x', colors='#757575')
        ax.tick_params(axis='y', colors='#757575')
        for spine in ['left', 'bottom', 'top', 'right']:
            ax.spines[spine].set_color('#757575')
        ax.legend()
        fig = format_plot_style(fig, B_DARK_THEME)
        results['rolling_alpha_plot'] = {'img64': to_base64(fig),
            'rolling_alphas_json': pd.DataFrame({'Rolling alphas':
            rolling_alphas}, index=idx_vals).to_json(orient='split')}
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(idx_vals, rolling_resid_stds, label='Rolling Residual Std',
            color='orange')
        ax.axhline((y - y_pred_full).std(), color='red', linestyle='--',
            label='Full History Residual Std')
        ax.set_title(f'{window}-Window Rolling Residual Std', color='#757575')
        ax.set_ylabel(y_col, color='#757575')
        ax.tick_params(axis='x', colors='#757575')
        ax.tick_params(axis='y', colors='#757575')
        for spine in ['left', 'bottom', 'top', 'right']:
            ax.spines[spine].set_color('#757575')
        ax.legend()
        fig = format_plot_style(fig, B_DARK_THEME)
        results['rolling_residual_std_plot'] = {'img64': to_base64(fig),
            'rolling_residuals_json': pd.DataFrame({'Residuals':
            rolling_resid_stds}, index=idx_vals).to_json(orient='split')}
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(y.index, y.values, label='Actual')
    ax.plot(y.index, y_pred_full.values, linestyle='--', label=
        'Predicted (Full Sample)', color='orange')
    ax.set_title('OLS: Full Sample Prediction')
    ax.set_xlabel('Index')
    ax.set_ylabel('Target')
    ax.legend()
    fig = format_plot_style(fig, B_DARK_THEME)
    results['full_pred_plot'] = to_base64(fig)
    y_pred_full_df = y_pred_full.to_frame()
    y_pred_full_df.columns = ['Prediction']
    y_pred_full_df['Actual'] = y
    y_pred_full_df = y_pred_full_df[['Actual', 'Prediction']]
    results['y_pred_full_json'] = y_pred_full_df.to_json(orient='split')
    residuals_full = y - y_pred_full_df['Prediction']
    x_residuals = range(len(residuals_full.values))
    fig_resid_full, ax_resid_full = plt.subplots(figsize=(8, 4))
    ax_resid_full.scatter(x_residuals, residuals_full.values, alpha=0.6,
        color='red')
    ax_resid_full.axhline(0, linestyle='--', color='black')
    ax_resid_full.set_title('Residuals (Full Set)')
    ax_resid_full.set_xlabel('Index')
    ax_resid_full.set_ylabel('Residual')
    fig_resid_full = format_plot_style(fig_resid_full, B_DARK_THEME)
    results['full_residuals_plot'] = to_base64(fig_resid_full)
    results['full_residuals_json'] = residuals_full.to_frame().to_json(orient
        ='split')
    X_last = df[x_cols].iloc[[-1]].copy()
    X_last['Intercept'] = 1.0
    X_last = X_last[model_full.params.index]
    last_pred_full = model_full.predict(X_last).iloc[0]
    results['last_pred_values'] = f'{y.iloc[-1]:.2f}'
    results['last_pred_full'] = f'{last_pred_full:.2f}'
    if not in_sample:
        fig_test, ax_test = plt.subplots(figsize=(10, 5))
        ax_test.plot(y_test.values, label='Actual (Test)')
        ax_test.plot(y_test_pred.values, linestyle='--', label=
            'Predicted (Full Sample)', color='orange')
        ax_test.set_title('OLS: Test Set Prediction')
        ax_test.set_xlabel('Index')
        ax_test.set_ylabel('Target')
        ax_test.legend()
        fig_test = format_plot_style(fig_test, B_DARK_THEME)
        y_test_pred_df = y_test_pred.to_frame()
        y_test_pred_df.columns = ['Prediction']
        y_test_pred_df['Actual'] = y_test
        y_test_pred_df = y_test_pred_df[['Actual', 'Prediction']]
        results['test_pred_plot'] = to_base64(fig_test)
        results['test_pred_json'] = y_test_pred_df.to_json(orient='split')
        residuals_test = y_test - y_test_pred_df['Prediction']
        x_residuals = range(len(residuals_test.values))
        fig_resid, ax_resid = plt.subplots(figsize=(8, 4))
        ax_resid.scatter(x_residuals, residuals_test.values, alpha=0.6,
            color='red')
        ax_resid.axhline(0, linestyle='--', color='black')
        ax_resid.set_title('Residuals (Test Set)')
        ax_resid.set_xlabel('Index')
        ax_resid.set_ylabel('Residual')
        fig_resid = format_plot_style(fig_resid, B_DARK_THEME)
        results['test_residuals_plot'] = to_base64(fig_resid)
        results['test_residuals_json'] = residuals_test.to_frame().to_json(
            orient='split')
    return results


def plot_rolling_correlation(df: pd.DataFrame, col_x: str, col_y: str,
    window: int=30, B_DARK_THEME=False) ->str:
    """
    Compute and plot rolling correlation between two columns.Returns:
        A base64-encoded PNG image of the plot."""
    cols_all = [col_x]
    if col_y not in cols_all:
        cols_all += [col_y]
    df = df[cols_all].dropna()
    idx_val = [i for i in range(len(df))]
    X = df[col_x]
    X = pd.to_numeric(X, errors='coerce')
    Y = df[col_y]
    Y = pd.to_numeric(Y, errors='coerce')
    rolling_corr = df[col_x].rolling(window).corr(Y)
    full_corr = df[col_x].corr(df[col_y])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(idx_val, rolling_corr, label=f'{window}-period Rolling Corr',
        color='#2196f3')
    ax.axhline(full_corr, color='red', linestyle='--', label=
        f'Full Corr = {full_corr:.2f}')
    ax.set_title(f'Rolling Correlation — {col_x} vs {col_y}', color='#757575')
    ax.set_xlabel('Index', color='#757575')
    ax.set_ylabel('Correlation', color='#757575')
    ax.tick_params(axis='x', colors='#757575')
    ax.tick_params(axis='y', colors='#757575')
    for spine in ax.spines.values():
        spine.set_color('#757575')
    ax.legend()
    fig = format_plot_style(fig, B_DARK_THEME=B_DARK_THEME)
    rolling_corr_to_cp = rolling_corr.to_frame()
    rolling_corr_to_cp.columns = [f'Rolling Correlation {window}']
    return {'img64': to_base64(fig), 'rolling_corr_json':
        rolling_corr_to_cp.to_json(orient='split'), 'full_corr': full_corr}


def regression_summary_table_html(df: pd.DataFrame, x_cols: list, y_col: str
    ) ->str:
    """
    Fit a linear regression using statsmodels and return the full summary table as HTML string."""
    cols_all = x_cols.copy()
    if y_col not in cols_all:
        cols_all += [y_col]
    df_clean = df[cols_all].dropna().copy()
    for col in cols_all:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    df_clean = df_clean.dropna()
    X = sm.add_constant(df_clean[x_cols])
    y = df_clean[y_col]
    model = sm.OLS(y, X).fit()
    return model.summary().as_html()


def relationship_explorer(df: pd.DataFrame, y_col: str, x_cols: list,
    in_sample=True, test_size=0.2, rw_beta=30, rw_corr=30, B_DARK_THEME=False
    ) ->dict:
    """
    Run relationship explorer analysis
    """
    reports = multi_x_column_analysis(df, x_cols, y_col, in_sample=
        in_sample, test_size=test_size, window=rw_beta, B_DARK_THEME=
        B_DARK_THEME)
    scatter_reports = {}
    correlations_reports = {}
    stationary_tests = {}
    is_col_numeric = is_numeric_column(df[y_col])
    numeric_series = None
    if is_col_numeric:
        numeric_series = pd.to_numeric(df[y_col], errors='coerce')
        adf_dict = adf_test(numeric_series.tolist())
        kpss_dict = kpss_test(numeric_series.tolist())
        stationary_tests[y_col] = {'adf': adf_dict, 'kpss': kpss_dict}
    for x in x_cols:
        scatter_reports[x] = simple_scatter_with_trendline(df, x, y_col,
            B_DARK_THEME=B_DARK_THEME)
        correlations_reports[x] = plot_rolling_correlation(df, x, y_col,
            window=rw_corr, B_DARK_THEME=B_DARK_THEME)
        is_col_numeric = is_numeric_column(df[x])
        numeric_series = None
        if is_col_numeric:
            numeric_series = pd.to_numeric(df[x], errors='coerce')
            adf_dict = adf_test(numeric_series.tolist())
            kpss_dict = kpss_test(numeric_series.tolist())
            stationary_tests[x] = {'adf': adf_dict, 'kpss': kpss_dict}
    scatter_reports_all = {'scatter': scatter_reports}
    correlations_reports = {'correlations': correlations_reports}
    stationary_tests = {'stationary_tests': stationary_tests}
    combined = {**reports, **scatter_reports_all, **correlations_reports,
        **stationary_tests}
    combined['stats_models_multivariate_html'] = regression_summary_table_html(
        df, x_cols, y_col)
    return combined


def change_title_color(fig, B_DARK_THEME):
    title_color = '#333333'
    if B_DARK_THEME:
        title_color = 'white'
    for ax in fig.axes:
        title_text = ax.get_title()
        if title_text:
            ax.set_title(title_text, color=title_color)
    if fig._suptitle:
        fig._suptitle.set_color(title_color)
    return fig


def time_series_analysis(df: pd.DataFrame, x_col: str, y_cols: list,
    B_DARK_THEME=False, start_date=None, end_date=None, date_type=None):
    """
    
    """
    import quantstats as qs
    from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import convert_dataframe_to_json
    print('time_series_analysis')
    print(df)
    print('x_col')
    print(x_col)
    print('y_cols')
    print(y_cols)
    print('B_DARK_THEME > ' + str(B_DARK_THEME))
    print('start_date > ' + str(start_date))
    print('end_date > ' + str(end_date))
    print('date_type > ' + str(date_type))
    df = df.dropna()
    try:
        if x_col == 'Index':
            df.index = pd.to_datetime(df.index)
        else:
            df.index = pd.to_datetime(df[x_col])
    except Exception:
        pass
    df = df.sort_index(ascending=True)
    if df.index.tz is not None:
        df.index = df.index.tz_convert(None)
    if date_type is not None:
        if date_type != -1:
            if date_type != 7:
                from dateutil.relativedelta import relativedelta
                today = pd.Timestamp.now().normalize()
                date_ranges = {'MTD': today.replace(day=1), 'YTD': today.replace(month=1, day=1), '3M': today - relativedelta(
                    months=3), '6M': today - relativedelta(months=6), '1Y':
                    today - relativedelta(years=1), '3Y': today -
                    relativedelta(years=3), '5Y': today - relativedelta(
                    years=5)}
                if date_type == 0:
                    df = df[df.index >= date_ranges['3M']]
                elif date_type == 1:
                    df = df[df.index >= date_ranges['6M']]
                elif date_type == 2:
                    df = df[df.index >= date_ranges['1Y']]
                elif date_type == 3:
                    df = df[df.index >= date_ranges['3Y']]
                elif date_type == 4:
                    df = df[df.index >= date_ranges['5Y']]
                elif date_type == 5:
                    df = df[df.index >= date_ranges['MTD']]
                elif date_type == 6:
                    df = df[df.index >= date_ranges['YTD']]
                elif date_type == 7:
                    pass
        else:
            if start_date is not None:
                if len(start_date) > 0:
                    start_date = pd.to_datetime(start_date).tz_localize(None
                        ).normalize()
                    df = df[df.index >= start_date]
            if end_date is not None:
                if len(end_date) > 0:
                    end_date = pd.to_datetime(end_date).tz_localize(None
                        ).normalize()
                    df = df[df.index <= end_date]
    if len(df) == 0:
        raise Exception(
            'Empty dataframe, please control the input data and applied dates filters...This filters may not be appropriate and conduct to empty dataframe'
            )
    rf = 0
    metrics_df = pd.DataFrame()
    for idx, col in enumerate(y_cols):
        returns_series = df[col]
        returns_series.index = pd.to_datetime(returns_series.index)
        metrics_basic = qs.reports.metrics(returns_series, rf=rf, mode=
            'basic', display=False, strategy_title='Returns Analysis',
            benchmark_title='Benchmark')
        if idx == 0:
            metrics_df = metrics_basic
            metrics_df.columns = [col]
        else:
            metrics_df[col] = metrics_basic
    metrics_json = convert_dataframe_to_json(metrics_df)
    ret_df = df[y_cols]
    if x_col == 'Index':
        ret_df.index = pd.to_datetime(ret_df.index)
    else:
        ret_df.index = pd.to_datetime(ret_df[x_col])
    ret_df = ret_df.sort_index(ascending=True)
    perf_df = 100 * (ret_df + 1).cumprod()
    fig, ax = plt.subplots(figsize=(8, 4))
    for column in perf_df.columns:
        ax.plot(perf_df.index, perf_df[column], label=column)
    ax.set_title('Performances', fontsize=16, color='#757575')
    ax.set_xlabel('Date', color='#757575')
    ax.set_ylabel('Performances', color='#757575')
    ax.legend(loc='upper left')
    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5,
        alpha=0.4, color='gray')
    ax.tick_params(axis='x', colors='#757575')
    ax.tick_params(axis='y', colors='#757575')
    ax.spines['bottom'].set_color('#757575')
    ax.spines['left'].set_color('#757575')
    for spine in ['left', 'bottom', 'top', 'right']:
        ax.spines[spine].set_color('#757575')
    fig.tight_layout()
    fig = format_plot_style(fig, B_DARK_THEME)
    perf_64 = to_base64(fig)
    cols_analysis = dict()
    for idx, col in enumerate(y_cols):
        data = ret_df[col]
        fig_heatmap = qs.plots.monthly_heatmap(data, show=False, ylabel=False)
        fig_heatmap = change_title_color(fig_heatmap, B_DARK_THEME=B_DARK_THEME
            )
        fig_yearly_returns = qs.plots.yearly_returns(data, show=False,
            ylabel=False)
        fig_yearly_returns = change_title_color(fig_yearly_returns,
            B_DARK_THEME=B_DARK_THEME)
        fig_quantiles = qs.plots.distribution(data, show=False, ylabel=False)
        fig_quantiles = change_title_color(fig_quantiles, B_DARK_THEME=
            B_DARK_THEME)
        fig, ax = plt.subplots(figsize=(8, 4))
        plotting_color = '#757575'
        sns.histplot(data, kde=True, ax=ax, edgecolor='none')
        ax.set_title(f'Histogram: {col}')
        ax.set_title(f'Histogram', color='#757575')
        ax.tick_params(axis='x', colors='#757575')
        ax.tick_params(axis='y', colors='#757575')
        ax.spines['bottom'].set_color('#757575')
        ax.spines['left'].set_color('#757575')
        for spine in ['left', 'bottom', 'top', 'right']:
            ax.spines[spine].set_color('#757575')
        plt.tight_layout()
        fig = format_plot_style(fig, B_DARK_THEME)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        daily_ret_histgram = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()
        fig_hist = qs.plots.histogram(data, show=False, ylabel=False)
        fig_hist = change_title_color(format_plot_style(fig_hist,
            B_DARK_THEME=B_DARK_THEME), B_DARK_THEME=B_DARK_THEME)
        fig_returns = qs.plots.returns(data, show=False, ylabel=False)
        fig_returns = change_title_color(format_plot_style(fig_returns,
            B_DARK_THEME=B_DARK_THEME), B_DARK_THEME=B_DARK_THEME)
        fig_log_returns = qs.plots.log_returns(data, show=False, ylabel=False)
        fig_log_returns = change_title_color(format_plot_style(
            fig_log_returns, B_DARK_THEME=B_DARK_THEME), B_DARK_THEME=
            B_DARK_THEME)
        fig_distribution = qs.plots.distribution(data, show=False, ylabel=False
            )
        fig_distribution = change_title_color(format_plot_style(
            fig_distribution, B_DARK_THEME=B_DARK_THEME), B_DARK_THEME=
            B_DARK_THEME)
        fig_drawdowns = qs.plots.drawdown(data, show=False, ylabel=False)
        fig_drawdowns = change_title_color(format_plot_style(fig_drawdowns,
            B_DARK_THEME=B_DARK_THEME), B_DARK_THEME=B_DARK_THEME)
        fig_drawdowns_periods = qs.plots.drawdowns_periods(data, show=False,
            ylabel=False)
        fig_drawdowns_periods = change_title_color(format_plot_style(
            fig_drawdowns_periods, B_DARK_THEME=B_DARK_THEME), B_DARK_THEME
            =B_DARK_THEME)
        try:
            fig_rolling_vol = qs.plots.rolling_volatility(data, show=False,
                ylabel=False)
            fig_rolling_vol = change_title_color(format_plot_style(
                fig_rolling_vol, B_DARK_THEME=B_DARK_THEME), B_DARK_THEME=
                B_DARK_THEME)
            fig_rolling_vol = to_base64(fig_rolling_vol)
        except Exception as e:
            fig_rolling_vol = {'errorMsg': str(e)}
        try:
            fig_rolling_sharpe = qs.plots.rolling_sharpe(data, show=False,
                ylabel=False)
            fig_rolling_sharpe = change_title_color(format_plot_style(
                fig_rolling_sharpe, B_DARK_THEME=B_DARK_THEME),
                B_DARK_THEME=B_DARK_THEME)
            fig_rolling_sharpe = to_base64(fig_rolling_sharpe)
        except Exception as e:
            fig_rolling_sharpe = {'errorMsg': str(e)}
        try:
            fig_rolling_sortino = qs.plots.rolling_sortino(data, show=False,
                ylabel=False)
            fig_rolling_sortino = change_title_color(format_plot_style(
                fig_rolling_sortino, B_DARK_THEME=B_DARK_THEME),
                B_DARK_THEME=B_DARK_THEME)
            fig_rolling_sortino = to_base64(fig_rolling_sortino)
        except Exception as e:
            fig_rolling_sortino = {'errorMsg': str(e)}
        cols_analysis[col] = {'heatmap': to_base64(fig_heatmap),
            'yearlyReturns': to_base64(fig_yearly_returns), 'histogram':
            to_base64(fig_hist), 'returns': to_base64(fig_returns),
            'log_returns': to_base64(fig_log_returns), 'distribution':
            to_base64(fig_distribution), 'rolling_vol': fig_rolling_vol,
            'rolling_sharpe': fig_rolling_sharpe, 'rolling_sortino':
            fig_rolling_sortino, 'quantiles': to_base64(fig_quantiles),
            'dd': to_base64(fig_drawdowns), 'dd_period': to_base64(
            fig_drawdowns_periods), 'daily_ret_histgram': daily_ret_histgram}
    index_as_str = [ts.isoformat() for ts in df.index.tolist()]
    return {'metrics': metrics_json, 'perf_64': perf_64, 'cols_analysis':
        cols_analysis, 'datesArr': index_as_str}


def plot_scree(explained_variance_ratio, cumulative_variance):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(range(1, len(explained_variance_ratio) + 1),
        explained_variance_ratio, alpha=0.5, align='center')
    ax.step(range(1, len(cumulative_variance) + 1), cumulative_variance,
        where='mid', label='Cumulative Explained Variance')
    ax.set_ylabel('Explained Variance Ratio')
    ax.set_xlabel('Principal Components')
    ax.set_title('Explained Variance')
    ax.legend(loc='best')
    ax.grid(True)
    return fig


def plot_loadings_heatmap(loadings):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(loadings, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('PCA Loadings Heatmap')
    ax.set_xlabel('Principal Components')
    ax.set_ylabel('Features')
    return fig


def plot_biplot(scores_df, loadings, features):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(scores_df['PC1'], scores_df['PC2'], alpha=0.5)
    for i, feature in enumerate(features):
        ax.arrow(0, 0, loadings.iloc[i, 0], loadings.iloc[i, 1], color='r',
            alpha=0.5)
        ax.text(loadings.iloc[i, 0] * 1.15, loadings.iloc[i, 1] * 1.15,
            feature, color='g', ha='center', va='center')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_title('PCA Biplot')
    ax.grid(True)
    return fig


def plot_pc_time_series(scores_df):
    fig, ax = plt.subplots(figsize=(10, 5))
    scores_df.plot(ax=ax, title='Principal Component Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('Score')
    ax.grid(True)
    return fig


def generate_pca_summary(explained_variance_ratio, loadings, top_n_features=2):
    """
    Generate a natural language summary of PCA results.Parameters:
    - explained_variance_ratio: list of floats from PCA
    - loadings: pd.DataFrame with features as rows, PCs as columns
    - top_n_features: int, number of top features to list per PC

    Returns:
    - str: summary text
    """
    total_var = sum(explained_variance_ratio[:2]) * 100
    summary = (
        f"The first 2 components explain <span class='pageNavTitle'>{total_var:.1f}%</span> of the variance."
        )
    for i in range(2):
        summary += '<li>'
        pc_name = f'PC{i + 1}'
        pc_loadings = loadings[i].abs().sort_values(ascending=False)
        top_features = pc_loadings.head(top_n_features).index.tolist()
        features_text = ' and '.join(top_features)
        summary += f' {pc_name} is heavily driven by {features_text}.'
        summary += '</li>'
    return summary


def run_pca(df: pd.DataFrame, y_cols: list, n_components: int=3,
    explained_variance: float=90, scale: bool=True, components_mode: int=1,
    B_DARK_THEME=False):
    """
    
    """
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    df = df.dropna()
    df = df[y_cols]
    try:
        df = df.sort_index(ascending=True)
    except:
        pass
    if scale:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df)
    components_mode = int(components_mode)
    if components_mode == 1:
        pca = PCA(n_components=int(n_components))
    elif components_mode == 2:
        print('explained_variance >>> ' + str(explained_variance))
        pca = PCA(n_components=float(explained_variance) / 100)
    else:
        raise ValueError(
            'components_mode must be 1 (variance) or 2 (fixed number)')
    scores = pca.fit_transform(scaled_data)
    explained_variance_ratio = list(pca.explained_variance_ratio_)
    cumulative_variance = pd.Series(explained_variance_ratio).cumsum().tolist()
    components_df = pd.DataFrame(pca.components_, columns=df.columns)
    scores_df = pd.DataFrame(scores, columns=[f'PC{i + 1}' for i in range(
        scores.shape[1])])
    loadings = components_df.T.multiply(pca.explained_variance_ ** 0.5, axis=1)
    result = {'res': 1, 'explained_variance_ratio':
        explained_variance_ratio, 'cumulative_variance':
        cumulative_variance, 'components': components_df, 'scores':
        scores_df, 'loadings': loadings}
    fig1 = plot_scree(result['explained_variance_ratio'], result[
        'cumulative_variance'])
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    fig2 = plot_loadings_heatmap(result['loadings'])
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    fig3 = plot_biplot(result['scores'], result['loadings'], df.columns)
    fig3 = format_plot_style(fig3, B_DARK_THEME)
    fig4 = plot_pc_time_series(result['scores'])
    fig4 = format_plot_style(fig4, B_DARK_THEME)
    scree_64 = to_base64(fig1)
    loadings_heatmap64 = to_base64(fig2)
    biplot64 = to_base64(fig3)
    ts64 = to_base64(fig4)
    summary_text = generate_pca_summary(explained_variance_ratio=result[
        'explained_variance_ratio'], loadings=result['loadings'])
    res_dict = {'res': 1, 'scree_64': scree_64, 'loadings_heatmap64':
        loadings_heatmap64, 'biplot64': biplot64, 'ts64': ts64,
        'summary_text': summary_text, 'pca_json': scores_df.to_json(orient=
        'split'), 'loadings_json': loadings.to_json(orient='split'),
        'variance_ratio_json': pd.DataFrame(explained_variance_ratio).to_json(orient='split'), 'components_json': components_df.to_json(
        orient='split')}
    return res_dict


def run_clustering_kmeans(df: pd.DataFrame, y_cols: list, n_clusters: int=3,
    B_DARK_THEME=False):
    """
    
    """
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score
    df = df[y_cols].dropna()
    X = df[y_cols]
    print('X X X')
    print(y_cols)
    print(X)
    print('n_clusters >>> ' + str(n_clusters))
    for col in X.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    df['Cluster'] = labels
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    sil_score = silhouette_score(X_scaled, labels)
    print(f'Silhouette Score: {sil_score:.3f}')
    cluster_summary = df.groupby('Cluster').agg(['mean', 'std'])
    print('\nCluster Summary Statistics:')
    print(cluster_summary)
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    scatter = ax1.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='Set2', s=50
        )
    ax1.set_title('KMeans Clustering (2D PCA)')
    ax1.set_xlabel('Principal Component 1')
    ax1.set_ylabel('Principal Component 2')
    fig1.colorbar(scatter, ax=ax1, label='Cluster')
    fig1.tight_layout()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    inertias = []
    k_range = range(1, 10)
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(k_range, inertias, marker='o')
    ax2.set_title('Elbow Method for Optimal k')
    ax2.set_xlabel('Number of clusters (k)')
    ax2.set_ylabel('Inertia')
    ax2.grid(True)
    fig2.tight_layout()
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    melted_df = df.copy()
    melted_df['Cluster'] = melted_df['Cluster'].astype(str)
    melted_df = melted_df.melt(id_vars='Cluster', var_name='Feature',
        value_name='Value')
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='Feature', y='Value', hue='Cluster', data=melted_df, ax=ax3)
    ax3.set_title('Feature Distributions by Cluster')
    ax3.tick_params(axis='x', rotation=45)
    fig3.tight_layout()
    fig3 = format_plot_style(fig3, B_DARK_THEME)
    flat_columns = [f'{col[0]} ({col[1]})' for col in cluster_summary.columns]
    summary_col_unique = []
    for col in cluster_summary.columns:
        if col[0] not in summary_col_unique:
            summary_col_unique.append(col[0])
    cluster_summary_dict = {'data': cluster_summary.values.tolist(),
        'index': cluster_summary.index.tolist(), 'columns': flat_columns,
        'columns_unique': summary_col_unique}
    cluster_df = df
    elbow_df = pd.DataFrame(inertias, index=k_range)
    return {'res': 1, 'kmean64': to_base64(fig1), 'elbow64': to_base64(fig2
        ), 'boxplot64': to_base64(fig3), 'sil_score': sil_score.round(2),
        'cluster_summary': cluster_summary_dict, 'cluster_json': cluster_df.to_json(orient='split'), 'elbow_json': elbow_df.to_json(orient=
        'split'), 'melted_json': melted_df.to_json(orient='split')}


def run_clustering_dbscan(df: pd.DataFrame, y_cols: list, epsilon: float=
    0.5, min_samples: int=5, B_DARK_THEME=False):
    """
    
    """
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score
    df = df[y_cols].dropna()
    X = df[y_cols]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
    labels = dbscan.fit_predict(X_scaled)
    df['Cluster'] = labels
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    valid_mask = [(label != -1) for label in labels]
    valid_labels = [label for i, label in enumerate(labels) if valid_mask[i]]
    valid_data = [X_scaled[i] for i in range(len(X_scaled)) if valid_mask[i]]
    if len(set(valid_labels)) > 1:
        sil_score = silhouette_score(valid_data, valid_labels)
    else:
        sil_score = None
    df_valid = df[df['Cluster'] != -1]
    cluster_summary = df_valid.groupby('Cluster').agg(['mean', 'std'])
    flat_columns = [f'{col[0]} ({col[1]})' for col in cluster_summary.columns]
    cluster_summary_dict = {'data': cluster_summary.values.tolist(),
        'index': cluster_summary.index.tolist(), 'columns': flat_columns}
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    scatter = ax1.scatter([point[0] for point in X_pca], [point[1] for
        point in X_pca], c=labels, cmap='Set2', s=50)
    ax1.set_title('DBSCAN Clustering (2D PCA)')
    ax1.set_xlabel('Principal Component 1')
    ax1.set_ylabel('Principal Component 2')
    fig1.colorbar(scatter, ax=ax1, label='Cluster')
    fig1.tight_layout()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    melted_df = df_valid.copy()
    melted_df['Cluster'] = melted_df['Cluster'].astype(str)
    melted_df = melted_df.melt(id_vars='Cluster', var_name='Feature',
        value_name='Value')
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='Feature', y='Value', hue='Cluster', data=melted_df, ax=ax2)
    ax2.set_title('Feature Distributions by Cluster (DBSCAN)')
    ax2.tick_params(axis='x', rotation=45)
    fig2.tight_layout()
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    cluster_df = df
    return {'res': 1, 'pca64': to_base64(fig1), 'boxplot64': to_base64(fig2
        ), 'cluster_summary': cluster_summary_dict, 'cluster_json':
        cluster_df.to_json(orient='split'), 'melted_json': melted_df.to_json(orient='split')}


def run_correlation_network(df: pd.DataFrame, y_cols: list, threshold:
    float=0.5, B_DARK_THEME=False):
    """
    
    """
    import networkx as nx
    df = df[y_cols].dropna()
    corr_matrix = df.corr()
    edges = []
    columns = list(corr_matrix.columns)
    threshold = float(threshold)
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            var1 = columns[i]
            var2 = columns[j]
            corr_value = corr_matrix.loc[var1, var2]
            if abs(corr_value) >= threshold:
                edges.append((var1, var2, {'weight': corr_value}))
    G = nx.Graph()
    G.add_edges_from(edges)
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    weights = [abs(attr['weight']) for _, _, attr in G.edges(data=True)]
    nx.draw(G, pos, ax=ax1, with_labels=True, width=weights, edge_color=
        weights, edge_cmap=plt.cm.viridis, node_color='skyblue', node_size=
        2000, font_size=10)
    ax1.set_title('Correlation Network (|p| ≥ 0.5)')
    fig1.tight_layout()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax2)
    ax2.set_title('Correlation Matrix Heatmap')
    fig2.tight_layout()
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    return {'res': 1, 'nx64': to_base64(fig1), 'corr64': to_base64(fig2),
        'correlation_json': corr_matrix.to_json(orient='split')}


def run_tsne(df: pd.DataFrame, y_cols: list, n_components: int=2,
    perplexity: int=30, B_DARK_THEME=False) ->dict:
    """
    Run tsne analysis
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    from sklearn.cluster import KMeans
    df = df[y_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    n_components = min(n_components, 3)
    kmeans = KMeans(n_clusters=n_components, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    perplexity = min(int(perplexity), len(df) - 1)
    tsne = TSNE(n_components=n_components, perplexity=perplexity, n_iter=
        400, random_state=42)
    X_tsne = tsne.fit_transform(X_scaled)
    df_tsne = pd.DataFrame(X_tsne)
    df_tsne['Cluster'] = labels.astype(str)
    cols = list(df_tsne.columns)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    scatter2 = ax2.scatter(df_tsne[cols[0]], df_tsne[cols[1]], c=labels,
        cmap='Set2', s=50)
    ax2.set_title('t-SNE Projection (Colored by KMeans Clusters)')
    ax2.set_xlabel('Component 1')
    ax2.set_ylabel('Component 2')
    fig2.colorbar(scatter2, ax=ax2, label='Cluster')
    fig2.tight_layout()
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    return {'res': 1, 'tsne64': to_base64(fig2), 'tsne': df_tsne.to_json(
        orient='split')}


def adjusted_r2(r2, n, k):
    return 1 - (1 - r2) * ((n - 1) / (n - k - 1)) if n > k + 1 else None


def run_polynomial_regression(df: pd.DataFrame, y_target: str, x_cols: list,
    degree: int=2, standardize=True, in_sample=True, test_size=0.2,
    B_DARK_THEME=False) ->dict:
    """
    Run polynomial regression
    """
    from sklearn.preprocessing import StandardScaler, PolynomialFeatures
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_squared_error
    from math import sqrt
    target = df[y_target]
    y = target
    df = df[x_cols].dropna()
    X = df
    if in_sample:
        X_train, X_test, y_train, y_test = X.astype(float), X.astype(float
            ), y.astype(float), y.astype(float)
        y_train = y_train.astype(float)
        y_test = y_test.astype(float)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
                X_train.index)
            X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=
                X_test.index)
            X_scaled_full = scaler.transform(X)
        else:
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            X_train_scaled = X_train.values
            X_test_scaled = X_test.values
            X_scaled_full = X.astype(float).values
    else:
        random_state = 42
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size
            =test_size, random_state=random_state)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_scaled_full = scaler.transform(X)
        else:
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            X_train_scaled = X_train.values
            X_test_scaled = X_test.values
            X_scaled_full = X.astype(float).values
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train_scaled)
    X_test_poly = poly.transform(X_test_scaled)
    X_full_poly = poly.transform(X_scaled_full)
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    y_pred = model.predict(X_test_poly)
    y_pred_full = model.predict(X_full_poly)
    r2 = r2_score(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    adj_r2 = adjusted_r2(r2, len(y_test), X_test_poly.shape[1])
    metrics = {'R2': round(r2, 4), 'Adjusted R2': round(adj_r2, 4) if 
        adj_r2 is not None else None, 'RMSE': round(rmse, 4), 'MAE': round(
        mae, 4)}
    terms = poly.get_feature_names_out(x_cols)
    coefs = model.coef_
    intercept = model.intercept_

    def format_term(term, coef):
        term = term.replace('^', '<sup>') + '</sup>' if '^' in term else term
        return f'{coef:.4f} × {term}'
    equation = f'{intercept:.4f}'
    for coef, term in zip(coefs, terms):
        formatted = format_term(term, coef)
        sign = ' + ' if coef >= 0 else ' - '
        equation += sign + formatted.lstrip('-')
    set_text = 'test'
    if in_sample:
        set_text = 'full'
    narrative = (
        f"The polynomial regression model of degree <span class='whiteLabel' style='font-weight:bold'>{degree}</span> using features <span class='whiteLabel' style='font-weight:bold'>{x_cols}</span> {'with' if standardize else 'without'} standardization achieved:<br><span class='whiteLabel' style='font-weight:bold'>R2 of {metrics['R2']}</span><br><span class='whiteLabel' style='font-weight:bold'>RMSE of {metrics['RMSE']}</span><br>"
         + (
        f"<span class='whiteLabel' style='font-weight:bold'>Adjusted R2 of {metrics['Adjusted R2']}</span><br>"
         if adj_r2 is not None else '') +
        f"on the <span style='text-decoration:underline'>{set_text} set</span>.<br><span class='whiteLabel' style='font-weight:bold'>Last value: {y.iloc[-1]:.2f}</span><br><span class='whiteLabel' style='font-weight:bold'>Next step prediction: {y_pred_full[-1]:.2f}</span><br>"
         + (
        f"<br><span class='whiteLabel' style='font-weight:bold'>The polynomial equation is:</span><br><code class='whiteLabel' style='font-weight:bold; font-family:monospace; display:inline-block; padding:7px'>{equation}</code>"
         if equation is not None else ''))
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(y_test.values, label='Actual', marker='o')
    ax1.plot(y_pred, label='Predicted (Polynomial)', linestyle='--')
    ax1.set_title('Actual vs Predicted (Test Set)')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Target')
    ax1.legend()
    fig1.tight_layout()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    pred_df = pd.DataFrame(y_test.values, index=y_test.index, columns=[
        'Actual Values'])
    pred_df['Predictions'] = y_pred
    residuals = y_test.values - y_pred
    x_residuals = range(len(residuals))
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(x_residuals, residuals, color='red', alpha=0.6)
    ax2.axhline(0, color='black', linestyle='--')
    ax2.set_title('Residual Plot (Test Set)')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Residual')
    fig2.tight_layout()
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    residuals_df = pd.DataFrame(residuals, index=x_residuals, columns=[
        'Residuals'])
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.scatter(y_test, y_pred, alpha=0.7)
    ax3.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color=
        'black', linestyle='--')
    ax3.set_title('Prediction vs Actual (Test Set)')
    ax3.set_xlabel('Actual')
    ax3.set_ylabel('Predicted')
    fig3.tight_layout()
    fig3 = format_plot_style(fig3, B_DARK_THEME)
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.plot(y.index, y.values, label='Actual')
    ax4.plot(y.index, y_pred_full, linestyle='--', label=
        'Full Sample Prediction')
    ax4.set_title('Polynomial Regression: Full Sample Prediction')
    ax4.set_xlabel('Index')
    ax4.set_ylabel('Target')
    ax4.legend()
    fig4 = format_plot_style(fig4, B_DARK_THEME)
    y_pred_full_df = pd.DataFrame(y_pred_full)
    y_pred_full_df.columns = ['Prediction']
    y_pred_full_df['Actual'] = y
    y_pred_full_df = y_pred_full_df[['Actual', 'Prediction']]
    return {'res': 1, 'narrative': narrative, 'metrics': metrics, 'pred64':
        to_base64(fig1), 'res64': to_base64(fig2), 'predScatter64':
        to_base64(fig3), 'pred_json': pred_df.to_json(orient='split'),
        'residuals_json': residuals_df.to_json(orient='split'), 'pred_json':
        pred_df.to_json(orient='split'), 'fig_full64': to_base64(fig4),
        'pred_full_json': y_pred_full_df.to_json(orient='split')}


def run_decision_tree_regression(df: pd.DataFrame, y_target: str, x_cols:
    list, max_depth=None, in_sample=True, standardize=True, test_size=0.2,
    B_DARK_THEME=False) ->dict:
    """
    Run Decision tree regression
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeRegressor, export_text
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.model_selection import train_test_split
    from sklearn.tree import plot_tree
    from sklearn.inspection import PartialDependenceDisplay
    from math import sqrt
    target = df[y_target]
    y = target
    df = df[x_cols].dropna()
    X = df
    random_state = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=
        test_size, random_state=random_state)
    if in_sample:
        X_train, X_test, y_train, y_test = X.astype(float), X.astype(float
            ), y.astype(float), y.astype(float)
        y_train = y_train.astype(float)
        y_test = y_test.astype(float)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=
                y_test.index)
        else:
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test.values, columns=x_cols, index=
                y_test.index)
    elif standardize:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=y_test.index
            )
    else:
        X_train = X_train.astype(float)
        X_test = X_test.astype(float)
        X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test.values, columns=x_cols, index=y_test.index
            )
    model = DecisionTreeRegressor(max_depth=max_depth, random_state=
        random_state)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    metrics = {'R2': round(r2, 4), 'RMSE': round(rmse, 4), 'MAE': round(mae, 4)
        }
    X_last = df[x_cols].iloc[[-1]].copy()
    if standardize:
        X_last_scaled = scaler.transform(X_last)
    else:
        X_last_scaled = X_last.values
    y_last_pred = model.predict(X_last_scaled)[0]
    set_text = 'test'
    if in_sample:
        set_text = 'full'
    narrative = (
        f"The decision tree regression model using features {x_cols} {'with' if standardize else 'without'} standardization achieved:<br> <span class='whiteLabel' style='font-weight:bold'>R2 of {metrics['R2']}</span><br><span class='whiteLabel' style='font-weight:bold'>RMSE of {metrics['RMSE']}</span><br><span class='whiteLabel' style='font-weight:bold'>MAE of {metrics['MAE']}</span><br>on the <span style='text-decoration:underline'>{set_text} set</span>.<br><span class='whiteLabel' style='font-weight:bold'>Last value: {y.iloc[-1]:.2f}</span><br><span class='whiteLabel' style='font-weight:bold'>Next step prediction: {y_last_pred:.2f}</span><br>"
        )
    if standardize:
        X_full_scaled = scaler.transform(df[x_cols])
    else:
        X_full_scaled = df[x_cols].astype(float).values
    y_pred_full = model.predict(X_full_scaled)
    y_full = y
    fig_full, ax_full = plt.subplots(figsize=(10, 5))
    ax_full.plot(y_full.index, y_full.values, label='Actual')
    ax_full.plot(y_full.index, y_pred_full, linestyle='--', label=
        'Predicted (Full Sample)', color='orange')
    ax_full.set_title('Decision Tree: Full Sample Prediction')
    ax_full.set_xlabel('Index')
    ax_full.set_ylabel('Target')
    ax_full.legend()
    fig_full = format_plot_style(fig_full, B_DARK_THEME)
    full_sample_pred = y_full
    full_sample_pred = full_sample_pred.to_frame()
    full_sample_pred['Prediction'] = y_pred_full
    full_sample_pred.columns = ['Actual', 'Prediction']
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(y_test.values, label='Actual', marker='o')
    ax1.plot(y_pred, label='Predicted', linestyle='--')
    ax1.set_title(f'Actual vs Predicted ({set_text.capitalize()} Set)')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Target')
    ax1.legend()
    fig1.tight_layout()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    pred_df = pd.DataFrame(y_test.values, index=y_test.index, columns=[
        'Actual Values'])
    pred_df['Predictions'] = y_pred
    residuals = y_test.values - y_pred
    x_residuals = range(len(residuals))
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(x_residuals, residuals, color='red', alpha=0.6)
    ax2.axhline(0, color='black', linestyle='--')
    ax2.set_title(f'Residual Plot ({set_text.capitalize()} Set)')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Residual')
    fig2.tight_layout()
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    residuals_df = pd.DataFrame(residuals, index=x_residuals, columns=[
        'Residuals'])
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.scatter(y_test, y_pred, alpha=0.7)
    ax3.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color=
        'black', linestyle='--')
    ax3.set_title(f'Prediction vs Actual ({set_text.capitalize()} Set)')
    ax3.set_xlabel('Actual')
    ax3.set_ylabel('Predicted')
    fig3.tight_layout()
    fig3 = format_plot_style(fig3, B_DARK_THEME)
    tree_rules = export_text(model, feature_names=x_cols)
    fig_tree, ax = plt.subplots(figsize=(12, 8))
    plot_tree(model, feature_names=x_cols, filled=True, rounded=True,
        fontsize=10, ax=ax)
    fig_tree = format_plot_style(fig_tree, B_DARK_THEME)
    importances = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': x_cols, 'Importance': importances}
        ).sort_values(by='Importance', ascending=False)
    fig_feature, ax = plt.subplots(figsize=(6, 4))
    ax.barh(importance_df['Feature'], importance_df['Importance'])
    ax.set_title('Feature Importance (Decision Tree)')
    ax.invert_yaxis()
    fig_feature = format_plot_style(fig_feature, B_DARK_THEME)
    fig_partial_deps, ax = plt.subplots(figsize=(12, 6))
    PartialDependenceDisplay.from_estimator(model, X_test, features=x_cols,
        ax=ax)
    fig_partial_deps = format_plot_style(fig_partial_deps, B_DARK_THEME)
    leaf_values = model.predict(X_train)
    fig_leaf, ax = plt.subplots()
    ax.hist(leaf_values, bins=10, color='skyblue')
    ax.set_title('Distribution of Leaf Node Predictions')
    ax.set_xlabel('Predicted Value')
    fig_leaf = format_plot_style(fig_leaf, B_DARK_THEME)
    leaf_df = pd.DataFrame(leaf_values)
    return {'res': 1, 'narrative': narrative, 'tree_rules': tree_rules,
        'metrics': metrics, 'pred64': to_base64(fig1), 'res64': to_base64(
        fig2), 'predScatter64': to_base64(fig3), 'figTree64': to_base64(
        fig_tree), 'figFeature64': to_base64(fig_feature), 'figPartialDeps':
        to_base64(fig_partial_deps), 'figLeaf': to_base64(fig_leaf),
        'residuals_json': residuals_df.to_json(orient='split'), 'pred_json':
        pred_df.to_json(orient='split'), 'leaf_json': leaf_df.to_json(
        orient='split'), 'full_sample_pred_json': full_sample_pred.to_json(
        orient='split'), 'fig_full64': to_base64(fig_full)}


def run_decision_tree_regression_grid_search(df: pd.DataFrame, y_target:
    str, x_cols: list, max_depth=None, in_sample=False, standardize=True,
    test_size=0.2, B_DARK_THEME=False) ->dict:
    """
    Run Decision tree regression Grid Search
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeRegressor, export_text
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.model_selection import train_test_split
    from sklearn.tree import plot_tree
    from sklearn.inspection import PartialDependenceDisplay
    from sklearn.model_selection import GridSearchCV
    from math import sqrt
    target = df[y_target]
    y = target
    df = df[x_cols].dropna()
    X = df
    random_state = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=
        test_size, random_state=random_state)
    if in_sample:
        X_train, X_test, y_train, y_test = X.astype(float), X.astype(float
            ), y.astype(float), y.astype(float)
        y_train = y_train.astype(float)
        y_test = y_test.astype(float)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=
                y_test.index)
        else:
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test.values, columns=x_cols, index=
                y_test.index)
    elif standardize:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=y_test.index
            )
    else:
        X_train = X_train.astype(float)
        X_test = X_test.astype(float)
        X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test.values, columns=x_cols, index=y_test.index
            )
    param_grid = {'max_depth': list(range(2, 11)) + [None]}
    grid = GridSearchCV(estimator=DecisionTreeRegressor(random_state=42),
        param_grid=param_grid, scoring='neg_mean_squared_error', cv=5,
        n_jobs=-1)
    grid.fit(X_train, y_train)
    model = grid.best_estimator_
    best_depth = grid.best_params_['max_depth']
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    metrics = {'R2': round(r2, 4), 'RMSE': round(rmse, 4), 'MAE': round(mae,
        4), 'Best max_depth': best_depth}
    cv_results = pd.DataFrame(grid.cv_results_)
    fig_cv, ax = plt.subplots()
    ax.plot(cv_results['param_max_depth'], -cv_results['mean_test_score'],
        marker='o')
    ax.set_title('CV RMSE vs max_depth')
    ax.set_xlabel('max_depth')
    ax.set_ylabel('Mean RMSE')
    ax.grid(True)
    fig_cv.tight_layout()
    fig_cv = format_plot_style(fig_cv, B_DARK_THEME)
    tree_rules = export_text(model, feature_names=x_cols)
    fig_tree, ax = plt.subplots(figsize=(12, 8))
    plot_tree(model, feature_names=x_cols, filled=True, rounded=True,
        fontsize=10, ax=ax)
    fig_tree = format_plot_style(fig_tree, B_DARK_THEME)
    grid_df = -cv_results['mean_test_score'].to_frame()
    grid_df.index = cv_results['param_max_depth'].values
    grid_df.columns = ['RMSE vs max_depth']
    return {'res': 1, 'best_depth': best_depth, 'fig_cv_curve': to_base64(
        fig_cv), 'tree_rules': tree_rules, 'figTree64': to_base64(fig_tree),
        'grid_json': grid_df.to_json(orient='split')}


def run_random_forest_regression(df: pd.DataFrame, y_target: str, x_cols:
    list, n_estimators=100, max_depth=None, in_sample=False, standardize=
    True, test_size=0.2, B_DARK_THEME=False) ->dict:
    """
    Run Random Forest regression (structured like your decision tree version)
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.model_selection import train_test_split
    from sklearn.inspection import PartialDependenceDisplay
    from math import sqrt
    target = df[y_target]
    y = target
    df = df[x_cols].dropna()
    X = df
    random_state = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=
        test_size, random_state=random_state)
    if in_sample:
        X_train, X_test, y_train, y_test = X.astype(float), X.astype(float
            ), y.astype(float), y.astype(float)
        y_train = y_train.astype(float)
        y_test = y_test.astype(float)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=
                y_test.index)
        else:
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test.values, columns=x_cols, index=
                y_test.index)
    elif standardize:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=y_test.index
            )
    else:
        X_train = X_train.astype(float)
        X_test = X_test.astype(float)
        X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test.values, columns=x_cols, index=y_test.index
            )
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=
        max_depth, random_state=random_state)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    metrics = {'R2': round(r2, 4), 'RMSE': round(rmse, 4), 'MAE': round(mae, 4)
        }
    if standardize:
        X_full_scaled = scaler.transform(df[x_cols])
    else:
        X_full_scaled = df[x_cols].astype(float).values
    y_pred_full = model.predict(X_full_scaled)
    y_full = y
    set_text = 'test'
    if in_sample:
        set_text = 'full'
    narrative = (
        f"The random forest regression model using features {x_cols} {'with' if standardize else 'without'} standardization and <span class='whiteLabel'>n_estimators={n_estimators}, max_depth={max_depth}</span> achieved:<br><span class='whiteLabel' style='font-weight:bold'>R2 of {metrics['R2']}</span><br><span class='whiteLabel' style='font-weight:bold'>RMSE of {metrics['RMSE']}</span><br><span class='whiteLabel' style='font-weight:bold'>MAE of {metrics['MAE']}</span><br>on the <span style='text-decoration:underline'>{set_text} set</span>.<br><span class='whiteLabel' style='font-weight:bold'>Last value: {y.iloc[-1]:.2f}</span><br><span class='whiteLabel' style='font-weight:bold'>Next step prediction: {y_pred_full[-1]:.2f}</span><br>"
        )
    fig_full, ax_full = plt.subplots(figsize=(10, 5))
    ax_full.plot(y_full.index, y_full.values, label='Actual')
    ax_full.plot(y_full.index, y_pred_full, linestyle='--', label=
        'Predicted (Full Sample)', color='orange')
    ax_full.set_title('Random Forest Tree: Full Sample Prediction')
    ax_full.set_xlabel('Index')
    ax_full.set_ylabel('Target')
    ax_full.legend()
    fig_full = format_plot_style(fig_full, B_DARK_THEME)
    full_sample_pred = y_full
    full_sample_pred = full_sample_pred.to_frame()
    full_sample_pred['Prediction'] = y_pred_full
    full_sample_pred.columns = ['Actual', 'Prediction']
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(y_test.values, label='Actual', marker='o')
    ax1.plot(y_pred, label='Predicted', linestyle='--')
    ax1.set_title('Actual vs Predicted (Test Set)')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Target')
    ax1.legend()
    fig1.tight_layout()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    pred_df = pd.DataFrame(y_test.values, index=y_test.index, columns=[
        'Actual Values'])
    pred_df['Predictions'] = y_pred
    residuals = y_test.values - y_pred
    x_residuals = range(len(residuals))
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(x_residuals, residuals, color='red', alpha=0.6)
    ax2.axhline(0, color='black', linestyle='--')
    ax2.set_title('Residual Plot (Test Set)')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Residual')
    fig2.tight_layout()
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    residuals_df = pd.DataFrame(residuals, index=x_residuals, columns=[
        'Residuals'])
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.scatter(y_test, y_pred, alpha=0.7)
    ax3.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color=
        'black', linestyle='--')
    ax3.set_title('Prediction vs Actual (Test Set)')
    ax3.set_xlabel('Actual')
    ax3.set_ylabel('Predicted')
    fig3.tight_layout()
    fig3 = format_plot_style(fig3, B_DARK_THEME)
    importances = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': x_cols, 'Importance': importances}
        ).sort_values(by='Importance', ascending=False)
    fig_feature, ax = plt.subplots(figsize=(6, 4))
    ax.barh(importance_df['Feature'], importance_df['Importance'])
    ax.set_title('Feature Importance (Random Forest)')
    ax.invert_yaxis()
    fig_feature = format_plot_style(fig_feature, B_DARK_THEME)
    fig_partial_deps, ax = plt.subplots(figsize=(12, 6))
    PartialDependenceDisplay.from_estimator(model, X_test, features=x_cols,
        ax=ax)
    fig_partial_deps = format_plot_style(fig_partial_deps, B_DARK_THEME)
    return {'res': 1, 'narrative': narrative, 'metrics': metrics, 'pred64':
        to_base64(fig1), 'res64': to_base64(fig2), 'predScatter64':
        to_base64(fig3), 'figFeature64': to_base64(fig_feature),
        'figPartialDeps': to_base64(fig_partial_deps), 'residuals_json':
        residuals_df.to_json(orient='split'), 'pred_json': pred_df.to_json(
        orient='split'), 'full_sample_pred_json': full_sample_pred.to_json(
        orient='split'), 'fig_full64': to_base64(fig_full)}


def run_random_forest_regression_grid_search(df: pd.DataFrame, y_target:
    str, x_cols: list, n_estimators=100, max_depth=None, in_sample=False,
    standardize=True, test_size=0.2, B_DARK_THEME=False) ->dict:
    """
    Run Decision tree regression Grid Search
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import DecisionTreeRegressor, export_text
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.model_selection import train_test_split
    from sklearn.tree import plot_tree
    from sklearn.inspection import PartialDependenceDisplay
    from sklearn.model_selection import GridSearchCV
    from math import sqrt
    target = df[y_target]
    y = target
    df = df[x_cols].dropna()
    X = df
    random_state = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=
        test_size, random_state=random_state)
    if in_sample:
        X_train, X_test, y_train, y_test = X.astype(float), X.astype(float
            ), y.astype(float), y.astype(float)
        y_train = y_train.astype(float)
        y_test = y_test.astype(float)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=
                y_test.index)
        else:
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
                y_train.index)
            X_test = pd.DataFrame(X_test.values, columns=x_cols, index=
                y_test.index)
    elif standardize:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=y_test.index
            )
    else:
        X_train = X_train.astype(float)
        X_test = X_test.astype(float)
        X_train = pd.DataFrame(X_train.values, columns=x_cols, index=
            y_train.index)
        X_test = pd.DataFrame(X_test.values, columns=x_cols, index=y_test.index
            )
    param_grid = {'max_depth': list(range(2, 11)) + [None]}
    rf = RandomForestRegressor(random_state=random_state)
    grid = GridSearchCV(rf, param_grid, cv=5, scoring=
        'neg_mean_squared_error', n_jobs=-1)
    grid.fit(X_train, y_train)
    model = grid.best_estimator_
    best_depth = grid.best_params_['max_depth']
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    metrics = {'R2': round(r2, 4), 'RMSE': round(rmse, 4), 'MAE': round(mae,
        4), 'Best max_depth': best_depth}
    cv_results = pd.DataFrame(grid.cv_results_)
    fig_cv, ax = plt.subplots()
    ax.plot(cv_results['param_max_depth'], -cv_results['mean_test_score'],
        marker='o')
    ax.set_title('CV RMSE vs max_depth')
    ax.set_xlabel('max_depth')
    ax.set_ylabel('Mean RMSE')
    ax.grid(True)
    fig_cv.tight_layout()
    fig_cv = format_plot_style(fig_cv, B_DARK_THEME)
    grid_df = -cv_results['mean_test_score'].to_frame()
    grid_df.index = cv_results['param_max_depth'].values
    grid_df.columns = ['RMSE vs max_depth']
    return {'res': 1, 'best_depth': best_depth, 'fig_cv_curve': to_base64(
        fig_cv), 'grid_json': grid_df.to_json(orient='split')}


def run_quantile_regression(df: pd.DataFrame, y_target: str, x_cols: list,
    quantiles: list, standardize=True, in_sample=True, test_size=0.2,
    B_DARK_THEME=False) ->dict:
    """
    Run Quantile Regression using statsmodels
    """
    import statsmodels.api as sm
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_absolute_error
    from math import sqrt
    import matplotlib.pyplot as plt
    quantiles = [float(elem) for elem in quantiles]
    target = df[y_target]
    y = target
    df = df[x_cols].dropna()
    X = df
    if in_sample:
        X_train, X_test, y_train, y_test = X.astype(float), X.astype(float
            ), y.astype(float), y.astype(float)
        y_train = y_train.astype(float)
        y_test = y_test.astype(float)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
                X_train.index)
            X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=
                X_test.index)
        X_train_sm = sm.add_constant(X_train).astype(float)
        X_test_sm = sm.add_constant(X_test).astype(float)
        fits = {q: sm.QuantReg(y_train, X_train_sm).fit(q=q) for q in quantiles
            }
        preds = {q: fit.predict(X_test_sm) for q, fit in fits.items()}
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size
            =test_size, random_state=42)
        if standardize:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
                X_train.index)
            X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=
                X_test.index)
        else:
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            y_train = y_train.astype(float)
            y_test = y_test.astype(float)
        X_train_sm = sm.add_constant(X_train).astype(float)
        X_test_sm = sm.add_constant(X_test).astype(float)
        y_train = y_train.astype(float)
        y_test = y_test.astype(float)
        fits = {q: sm.QuantReg(y_train, X_train_sm).fit(q=q) for q in quantiles
            }
        preds = {q: fit.predict(X_test_sm) for q, fit in fits.items()}
    fig, ax = plt.subplots(figsize=(8, 5))
    x_feature = x_cols[0]
    x_vals = X_test[x_feature]
    ax.scatter(x_vals, y_test, color='gray', alpha=0.4, label='Actual')
    sorted_df = pd.DataFrame({x_feature: x_vals, 'Actual': y_test})
    summaries = dict()
    narratives = dict()
    regression_formulas = dict()
    for q in quantiles:
        pred_q = preds[q]
        if not isinstance(pred_q, pd.Series):
            pred_q = pd.Series(pred_q, index=X_test.index)
        sorted_df[f'Quantile_{q}'] = pred_q
        model = sm.QuantReg(y_train, X_train_sm)
        res_q = model.fit(q=q)
        fits[q] = res_q
        summaries[q] = res_q.summary().as_html()
        rmse = round(((y_test - preds[q]) ** 2).mean() ** 0.5, 4)
        mae = round((y_test - preds[q]).abs().mean(), 4)
        narratives[q] = (
            f"<b>Quantile {q}:</b><br>RMSE = <span class='whiteLabel' style='font-weight:bold'>{rmse}</span><br>MAE = <span class='whiteLabel' style='font-weight:bold'>{mae}</span><br><br>"
            )
        model_fit = fits[q]
        coef = model_fit.params
        terms = [f'{round(coef[feature], 4)} × {feature}' for feature in
            coef.index if feature != 'const']
        intercept = round(coef['const'], 4)
        formula = f'y = {intercept} + ' + ' + '.join(terms)
        regression_formulas[q] = formula
    sorted_df = sorted_df.sort_values(by=x_feature)
    for q in quantiles:
        ax.plot(sorted_df[x_feature], sorted_df[f'Quantile_{q}'], label=
            f'Quantile {q}', linewidth=2)
    quantiles_sorted = sorted(quantiles)
    ax.set_xlabel(x_feature)
    ax.set_ylabel(y_target)
    ax.set_title('Quantile Regression Trendlines')
    ax.legend()
    ax.fill_between(sorted_df[x_feature], sorted_df[
        f'Quantile_{str(quantiles_sorted[0])}'], sorted_df[
        f'Quantile_{str(quantiles_sorted[-1])}'], color='blue', alpha=0.2,
        label='Prediction Interval (10%-90%)')
    fig = format_plot_style(fig, B_DARK_THEME)
    fig_resid, ax = plt.subplots(figsize=(8, 5))
    residuals_all = pd.DataFrame()
    for q in quantiles:
        pred_q = preds[q]
        if not isinstance(pred_q, pd.Series):
            pred_q = pd.Series(pred_q, index=X_test.index)
        pred_q = pred_q.loc[y_test.index]
        residuals = y_test - pred_q
        residuals_all[f'Quantile {q}'] = residuals
        print(f'len pred_q > {q}')
        print(len(pred_q))
        ax.scatter(y_test.index, residuals, label=f'Quantile {q}', alpha=0.5)
    ax.axhline(0, color='black', linestyle='--')
    ax.set_title('Residuals by Quantile')
    ax.set_xlabel('Index')
    ax.set_ylabel('Residual (Actual - Predicted)')
    ax.legend()
    fig_resid = format_plot_style(fig_resid, B_DARK_THEME)
    return {'res': 1, 'fig64': to_base64(fig), 'summaries': summaries,
        'narratives': narratives, 'fig_resid64': to_base64(fig_resid),
        'regression_formulas': regression_formulas, 'quantiles_json':
        sorted_df.to_json(orient='split'), 'residuals_json': residuals_all.to_json(orient='split')}


def run_rolling_regression(df: pd.DataFrame, y_target: str, x_cols: list,
    window: int=60, standardize: bool=True, test_size=0.2, B_DARK_THEME:
    bool=False) ->dict:
    """
    Rolling Regression with Forecasting
    """
    from statsmodels.regression.rolling import RollingOLS
    import statsmodels.api as sm
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    from sklearn.linear_model import LinearRegression
    from math import sqrt
    y = df[y_target].astype(float)
    X = df[x_cols].astype(float)
    if standardize:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=x_cols, index=X.index
            )
    X_sm = sm.add_constant(X)
    model = RollingOLS(endog=y, exog=X_sm, window=window)
    res = model.fit()
    X_valid = X_sm.loc[res.params.index]
    y_pred = (res.params * X_valid).sum(axis=1)
    y_true = y[y_pred.index]
    residuals = y_true - y_pred
    rmse = sqrt(((y_true - y_pred) ** 2).mean())
    mae = mean_absolute_error(y_true, y_pred)
    last_X = X.iloc[[-1]]
    X_forecast_sm = sm.add_constant(last_X, has_constant='add')
    X_forecast_sm = X_forecast_sm[res.params.columns]
    last_params = res.params.iloc[-1]
    forecast_value = (X_forecast_sm.iloc[0] * last_params).sum()
    last_idx = df.index[-1]
    prev_idx = df.index[-2]
    step = last_idx - prev_idx
    forecast_index = [last_idx + step]
    narrative = (
        f"RollingOLS (window={window}) estimates changing linear relationships between {x_cols} and {y_target} over time. The model achieved:<br><span class='whiteLabel' style='font-weight:bold'>RMSE of {round(rmse, 4)}</span><br><span class='whiteLabel' style='font-weight:bold'>MAE of {round(mae, 4)}</span><br> on the fitted rolling predictions.<br>It also performed a final out-of-sample forecast for the next step: {forecast_value:.2f}."
        )
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(y.index, y, label='Actual')
    y_pred_trimmed = y_pred.iloc[window:]
    ax1.plot(y_pred_trimmed.index, y_pred_trimmed.values, linestyle='--',
        label='Predicted')
    ax1.set_title('RollingOLS: Actual vs Predicted')
    ax1.legend()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(y_true.index, residuals, alpha=0.6)
    ax2.axhline(0, color='black', linestyle='--')
    ax2.set_title('Residuals (RollingOLS)')
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    residuals_df = pd.DataFrame({'Residuals': residuals}, index=y_true.index)
    pred_df = pd.DataFrame({'Actual': y_true, 'Predicted': y_pred}, index=
        y_true.index)
    coef_df = res.params.copy()
    coef_df.index.name = 'Index'
    rolling_charts = {}
    rolling_coeff_dict = {}
    for col in coef_df.columns:
        fig, ax = plt.subplots(figsize=(8, 4))
        coef_df[col].plot(ax=ax, label=col, linewidth=2)
        ax.set_title(f'Rolling Coefficient: {col}')
        ax.set_xlabel('Index' if df.index.name is None else df.index.name)
        ax.set_ylabel('Coefficient Value')
        ax.legend()
        fig = format_plot_style(fig, B_DARK_THEME)
        rolling_charts[col] = to_base64(fig)
        rolling_coeff_dict[col] = coef_df[col].to_json(orient='split')
    return {'res': 1, 'narrative': narrative, 'fig64': to_base64(fig1),
        'fig_resid64': to_base64(fig2), 'pred_json': pred_df.to_json(orient
        ='split'), 'residuals_json': residuals_df.to_json(orient='split'),
        'rolling_charts': rolling_charts, 'rolling_coeff_dict':
        rolling_coeff_dict}


def run_recursive_regression(df: pd.DataFrame, y_target: str, x_cols: list,
    standardize=True, B_DARK_THEME=False) ->dict:
    """
    Recursive Regression
    Recursive Least Squares is a variant of linear regression that updates its coefficient estimates sequentially as new data becomes available. (Expanding)
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    from math import sqrt
    results = {}
    df = df[[y_target] + x_cols].dropna().copy()
    for col in ([y_target] + x_cols):
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()
    X = df[x_cols].astype(float)
    y = df[y_target].astype(float)
    X_train, X_test, y_train, y_test = X.astype(float), X.astype(float
        ), y.astype(float), y.astype(float)
    y_train = y_train.astype(float)
    y_test = y_test.astype(float)
    if standardize:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        X_train = pd.DataFrame(X_train_scaled, columns=x_cols, index=
            X_train.index)
        X_test = pd.DataFrame(X_test_scaled, columns=x_cols, index=X_test.index
            )
    X_train_sm = sm.add_constant(X_train).astype(float)
    model = sm.RecursiveLS(endog=y_train, exog=X_train_sm)
    res = model.fit()
    coeff_filtered = res.recursive_coefficients.filtered
    fig_coeffs = res.plot_recursive_coefficient(range(model.k_exog), alpha=
        None, figsize=(10, 6))
    coeffs_df = pd.DataFrame(coeff_filtered).T
    coeffs_df.columns = X_train_sm.columns
    coeffs_df.index = X_train_sm.index
    pred_df = y_train.to_frame()
    pred_df.columns = ['Actual']
    pred_df['Prediction'] = 0
    for col in X_train_sm.columns:
        pred_df['Prediction'] += (coeffs_df[col] * X_train_sm[col]).astype(
            float)
    y_pred = pred_df['Prediction']
    residuals = pred_df['Actual'] - pred_df['Prediction']
    residuals_df = residuals.to_frame()
    residuals.columns = ['Residuals']
    rmse = sqrt(mean_squared_error(pred_df['Actual'], pred_df['Prediction']))
    mae = mean_absolute_error(pred_df['Actual'], pred_df['Prediction'])
    metrics = {'RMSE': round(rmse, 4), 'MAE': round(mae, 4)}
    narrative = (
        f"Recursive Least Squares regression using features <span class='whiteLabel' style='font-weight:bold'>{x_cols}</span> {'with' if standardize else 'without'} standardization achieved:<br><span class='whiteLabel' style='font-weight:bold'>RMSE of {metrics['RMSE']}</span><br><span class='whiteLabel' style='font-weight:bold'>MAE of {metrics['MAE']}</span><br>on the <span style='text-decoration:underline'>full set</span>."
        )
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(y_test.index, y_test.values, label='Actual')
    ax1.plot(y_test.index, y_pred, label='Predicted', linestyle='--', color
        ='orange')
    ax1.set_title('RecursiveLS: Actual vs Predicted')
    ax1.legend()
    fig1 = format_plot_style(fig1, B_DARK_THEME)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.scatter(y_test.index, residuals, alpha=0.6, color='red')
    ax2.axhline(0, linestyle='--', color='black')
    ax2.set_title('Residuals (RecursiveLS)')
    fig2 = format_plot_style(fig2, B_DARK_THEME)
    coef_dict = {}
    fig_coeffs = {}
    for i, col in enumerate(list(coeffs_df.columns)):
        coef_series = pd.Series(coeffs_df[col], index=coeffs_df.index)
        coef_dict[col] = coef_series.to_json(orient='split')
        fig, ax = plt.subplots(figsize=(10, 4))
        coef_series.plot(ax=ax, label=f'{col} (Recursive)')
        ax.set_title(f'Recursive Coefficient for {col}')
        ax.legend()
        fig = format_plot_style(fig, B_DARK_THEME)
        fig_coeffs[col] = to_base64(fig)
    pred_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}, index=
        y_test.index)
    residuals_df = pd.DataFrame({'Residual': residuals}, index=y_test.index)
    return {'res': 1, 'narrative': narrative, 'metrics': metrics, 'pred64':
        to_base64(fig1), 'res64': to_base64(fig2), 'residuals_json':
        residuals.to_json(orient='split'), 'pred_json': pred_df.to_json(
        orient='split'), 'residuals_json': residuals_df.to_json(orient=
        'split'), 'recursive_coeffs_json': coef_dict,
        'recursive_coeffs_figs': fig_coeffs}


def generate_feature_importance_summary(importance_df, top_n=None):
    """
    Generate a natural language summary of the top N most important features.Parameters:
        importance_df (pd.DataFrame): DataFrame with columns ['Feature', 'Importance']
        top_n (int): Number of top features to include in the summary

    Returns:
        str: Auto-generated explanation
    """
    if importance_df.empty:
        return 'No feature importance data is available.'
    if top_n is None:
        top_n = len(importance_df)
    top_n = min(top_n, len(importance_df))
    total = importance_df['Importance'].sum()
    importance_df = importance_df.copy()
    importance_df['Percent'] = importance_df['Importance'] / total * 100
    top_features = importance_df.head(top_n)
    lines = []
    for i, row in top_features.iterrows():
        feature = row['Feature']
        percent = row['Percent']
        lines.append(
            f"• <span class='pageNavTitle whiteLabel'>{feature}</span> contributes approximately <span style='color:red'>{percent:.1f}%</span> of the total importance."
            )
    summary = (
        f'Among all input features, the most influential {top_n} are:<br>' +
        '<br>'.join(lines))
    return summary


def run_features_importance_randomforest(df: pd.DataFrame, y_target: str,
    x_cols: list, n_estimators=100, max_depth=None, min_samples_split=2,
    min_samples_leaf=1, max_features='sqrt', bootstrap=True, B_DARK_THEME=False
    ) ->dict:
    """
    Run feautres importance with randomforest
    """
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    target = df[y_target]
    df = df[x_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    if max_depth == -1:
        max_depth = None
    model = RandomForestRegressor(n_estimators=n_estimators, criterion=
        'squared_error', max_depth=max_depth, min_samples_split=
        min_samples_split, min_samples_leaf=min_samples_leaf,
        min_weight_fraction_leaf=0.0, max_features=max_features,
        max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=bootstrap,
        oob_score=False, n_jobs=None, random_state=None, verbose=0,
        warm_start=False, ccp_alpha=0.0, max_samples=None)
    model.fit(X_scaled, target)
    importances = model.feature_importances_
    features = df.columns
    importance_df = pd.DataFrame({'Feature': features, 'Importance':
        importances}).sort_values(by='Importance', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(importance_df['Feature'], importance_df['Importance'], color=
        'skyblue')
    ax.set_xlabel('Importance')
    ax.set_title('Feature Importance (Random Forest)')
    ax.invert_yaxis()
    fig.tight_layout()
    fig = format_plot_style(fig, B_DARK_THEME)
    summary = ''
    try:
        summary = generate_feature_importance_summary(importance_df)
    except:
        pass
    return {'res': 1, 'figImportance64': to_base64(fig), 'summary': summary,
        'importance_json': importance_df.to_json(orient='split')}


def run_features_importance_xgboost(df: pd.DataFrame, y_target: str, x_cols:
    list, B_DARK_THEME=False) ->dict:
    """
    Not implemented yet (due to installation of xgboost...)    
    """
    from sklearn.preprocessing import StandardScaler
    from xgboost import XGBClassifier
    target = df[y_target]
    df = df[x_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss',
        random_state=42)
    model.fit(X_scaled, target)
    importance_values = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': df.columns, 'Importance':
        importance_values}).sort_values(by='Importance', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(importance_df['Feature'], importance_df['Importance'], color=
        'lightgreen')
    ax.set_xlabel('Importance')
    ax.set_title('Feature Importance (XGBoost)')
    ax.invert_yaxis()
    fig.tight_layout()
    fig = format_plot_style(fig, B_DARK_THEME)
    summary = ''
    try:
        summary = generate_feature_importance_summary(importance_df)
    except:
        pass
    return {'res': 1, 'figImportance64': to_base64(fig), 'summary': summary}


def run_mutual_information(df: pd.DataFrame, y_target: str, x_cols: list,
    B_DARK_THEME=False) ->dict:
    """
    Run mutual information
    """
    from sklearn.feature_selection import mutual_info_regression
    correlation = df[x_cols + [y_target]].corr()[y_target][x_cols]
    target = df[y_target]
    df = df[x_cols].dropna()
    X = df.astype(float)
    y = target.astype(float)
    mi_scores = mutual_info_regression(X, y, random_state=42)
    mi_df = pd.DataFrame({'Feature': x_cols, 'MI Score': mi_scores})
    mi_df.sort_values('MI Score', ascending=True, inplace=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(mi_df['Feature'], mi_df['MI Score'], color='royalblue', alpha=0.8)
    ax.set_title('Mutual Information Scores', fontsize=14)
    ax.set_xlabel('MI Score', fontsize=12)
    ax.set_ylabel('Feature', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig = format_plot_style(fig, B_DARK_THEME)
    mi_matrix = pd.DataFrame(index=x_cols, columns=x_cols)
    for col1 in x_cols:
        for col2 in x_cols:
            mi_score = mutual_info_regression(df[[col1]], df[col2])[0]
            mi_matrix.loc[col1, col2] = mi_score
    mi_matrix = mi_matrix.astype(float)
    fig_heatmap, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(mi_matrix, annot=True, cmap='coolwarm', center=0,
        linewidths=0.5, linecolor='gray', ax=ax)
    ax.set_title('Heatmap of Mutual Information')
    plt.tight_layout()
    fig_heatmap = format_plot_style(fig_heatmap, B_DARK_THEME)
    comparison_df = pd.DataFrame({'Feature': x_cols, 'Correlation':
        correlation.values, 'Mutual Information': mi_scores})
    fig_comp_correl, ax = plt.subplots(figsize=(10, 5))
    x = range(len(x_cols))
    width = 0.4
    ax.bar([(i - width / 2) for i in x], comparison_df['Correlation'],
        width=width, label='Correlation', color='skyblue')
    ax.bar([(i + width / 2) for i in x], comparison_df['Mutual Information'
        ], width=width, label='Mutual Information', color='orange')
    ax.set_xticks(x)
    ax.set_xticklabels(comparison_df['Feature'], rotation=45)
    ax.set_title('Comparison: Correlation vs Mutual Information')
    ax.set_ylabel('Score')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    fig_comp_correl.tight_layout()
    fig_comp_correl = format_plot_style(fig_comp_correl, B_DARK_THEME)
    return {'res': 1, 'mi64': to_base64(fig), 'heatmap64': to_base64(
        fig_heatmap), 'compCorre64': to_base64(fig_comp_correl), 'mi_json':
        mi_df.to_json(orient='split'), 'mi_matrix_json': mi_matrix.to_json(
        orient='split'), 'corr_comp_json': comparison_df.to_json(orient=
        'split')}

#END OF QUBE
