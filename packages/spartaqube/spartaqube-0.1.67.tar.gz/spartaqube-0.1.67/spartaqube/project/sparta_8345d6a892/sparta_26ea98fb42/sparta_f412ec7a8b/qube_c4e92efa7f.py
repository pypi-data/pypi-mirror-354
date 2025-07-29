_F='Example to run a simple linear regression'
_E='code'
_D='sub_description'
_C='description'
_B='title'
_A='from spartaqube import Spartaqube as Spartaqube'
def sparta_b68f8c4340():A=_A;type='OLS';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='OLS',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_80c940361d():A=_A;type='Polynomial Regression';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='PolynomialRegression',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_beffc13eb7():A=_A;type='Decision Tree Regression';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='DecisionTreeRegression',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_da7c650f5f():A=_A;type='Random Forest Regression';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='RandomForestRegression',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_dc0d9d4c0f():A=_A;type='Clustering';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='clustering',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_fb66245ab7():A=_A;type='Correlation Network';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='correlation_network',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_53e1ae9289():A=_A;type='PCA';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='pca',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_ee989e275a():A=_A;type='TSNE';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='tsne',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_e84e320c93():A=_A;type='Features importance';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='features_importance',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_a5401e19e6():A=_A;type='Mutual Information';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='mutual_information',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_b25ce6c5cd():A=_A;type='Quantile Regression';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='quantile_regression',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_8edd918964():A=_A;type='Rolling Regression';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='rolling_regression',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]
def sparta_200a023ac7():A=_A;type='Recursive Regression';return[{_B:f"{type.capitalize()}",_C:_F,_D:'',_E:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for SPX (ticker symbol: ^SPX)
spx_price_df = yf.Ticker(\"^SPX\").history(period=\"1y\")[['Close']]
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")[['Close']]
apple_price_df = apple_price_df.reindex(spx_price_df.index)
data_df = pd.concat([spx_price_df, apple_price_df], axis=1).pct_change().dropna()
data_df.columns = ['SPX', 'AAPL']

# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='recursive_regression',
  x=data_df['SPX'],
  y=data_df['AAPL'],
  title='Example',
  height=500
)
plot_example"""}]