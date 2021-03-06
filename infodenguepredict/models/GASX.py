import numpy as np
import pandas as pd
import pyflux as pf
from datetime import datetime
import matplotlib.pyplot as plt
from infodenguepredict.data.infodengue import combined_data


def build_model(data, ar=4, sc=4, family=pf.families.Poisson, formula=None):
    if formula is None:
        formula = "casos~1"
    model = pf.GASX(data=data, ar=ar, sc=sc, family=family(), formula=formula)
    return model


if __name__ == "__main__":
    city = 3304557
    prediction_window = 5  # weeks
    # data = get_alerta_table(city)  # Nova Iguaçu: 3303609
    # Fetching exogenous vars
    # T = get_temperature_data(city)  # (3303500)
    # T = T[~T.index.duplicated()]
    # Tw = get_tweet_data(city)
    # Tw = Tw[~Tw.index.duplicated()]
    Full = combined_data(city)#data.join(T.resample('W-SUN').mean()).join(Tw.resample('W-SUN').sum()).dropna()
    # print(data.info())
    # data.casos.plot()
    # print(Full.info())
    # print(Full.describe())

    # Full.to_csv('data.csv.gz', compression='gzip')
    model = build_model(Full.dropna(), ar=4, sc=6, formula='casos~1+numero')
    fit = model.fit('PML')#'BBVI', iterations=1000, optimizer='RMSProp')

    print(fit.summary())
    model.plot_fit()
    plt.savefig('GASX_in_sample.png')
    model.plot_parameters()
    model.plot_predict(h=5, past_values=12)
    plt.savefig('GASX_prediction.png')
    plt.show()
