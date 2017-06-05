"""
This Module implements time series models using R's tscount package
via the rpy2 library
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rpy2.robjects import pandas2ri
pandas2ri.activate()
from rpy2.robjects import r
from rpy2.rlike.container import TaggedList
from rpy2.robjects.packages import importr
from infodenguepredict.data.infodengue import get_alerta_table

def build_model(data):
    model = tsglm(data.casos,  model=TaggedList([52, 3], tags=['past_obs', 'past_mean']), distr='nbinom')
    return model

def plot_forecast(data, fcast):
    index = pd.date_range(start=data.index.max(), periods=len(fcast[3]) + 1, freq='W')[1:]
    forecast = pd.Series(fcast[3], index=index)
    lowerpi = pd.Series(fcast[4], index=index)
    upperpi = pd.Series(fcast[5], index=index)
    plt.plot(data.index, data.casos_est, color='b', alpha=0.5)
    plt.plot(forecast.index, forecast.values, color='red')
    plt.fill_between(forecast.index,
                      lowerpi.values,
                      upperpi.values,
                      alpha=0.2, color='red')


if __name__ == "__main__":
    data = get_alerta_table(3304557)  # Nova Iguaçu: 3303609
    tscount = importr('tscount')
    tsglm = r('tsglm')



    model = build_model(data)
    print(r.summary(model))
    r.plot(model)
    # fcast = forecast.forecast(model, h=5, level=95.0)
    # print(fcast[3], fcast[4], fcast[5])
    # plot_forecast(data=data, fcast=fcast)
    # plt.show()




