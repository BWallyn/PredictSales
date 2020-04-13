import pandas as pd

def preprocessing(data_sales, data_store):
    convert_levels_store = {
        'StoreType': {'a': 0, 'b': 3, 'c': 2, 'd': 1},
        'Assortment': {'a': 0, 'b': 2, 'c': 1},
        'PromoInterval': {'Jan,Apr,Jul,Oct': 2, 'Feb,May,Aug,Nov': 1, 'Mar,Jun,Sept,Dec': 0}
    }
    convert_levels_sales = {'StateHoliday': {'0': 0, 'a': 1, 'b': 2, 'c': 3}}
    data_store.replace(convert_levels_store, inplace=True)
    data_sales.replace(convert_levels_sales, inplace=True)
    data_sales['year'] = pd.to_datetime(data_sales['Date'], format='%Y-%m-%d').dt.year
    data_sales['month'] = pd.to_datetime(data_sales['Date'], format='%Y-%m-%d').dt.month
    data_sales.drop(columns=['Date'], inplace=True)
    # Replace NaNs
    # competition: we consider there is no competition when NaN
    data_store.loc[:, 'CompetitionDistance'] = data_store.loc[:, 'CompetitionDistance'].fillna(value=0.)
    data_store.loc[:, 'CompetitionOpenSinceMonth'] = data_store.loc[:, 'CompetitionOpenSinceMonth'].fillna(value=0.)
    data_store.loc[:, 'CompetitionOpenSinceYear'] = data_store.loc[:, 'CompetitionOpenSinceYear'].fillna(value=0.)
    # Promo2: we consider that there is no promo when NaN
    data_store.loc[:, 'Promo2SinceWeek'] = data_store.loc[:, 'Promo2SinceWeek'].fillna(value=0.)
    data_store.loc[:, 'Promo2SinceYear'] = data_store.loc[:, 'Promo2SinceYear'].fillna(value=0.)
    data_store.loc[:, 'PromoInterval'] = data_store.loc[:, 'PromoInterval'].fillna(value=0.)
    return data_sales, data_store

def merge_data(data_sales, data_store, remove_outliers=False):
    data_merged = data_sales.merge(data_store, left_on='Store', right_on='Store', how='left')
    if remove_outliers:
        # One store with a huge number of customers
        data_merged = data_merged[data_merged['Customers'] <= 6000]
        # Two stores with competition before 1980
        data_merged = data_merged[(data_merged['CompetitionOpenSinceYear'] >= 1980) | (data_merged['CompetitionOpenSinceYear'] == 0.)]
        # Two stores with competition distance >= 5000
        data_merged = data_merged[data_merged['CompetitionDistance'] <= 5000]
    return data_merged