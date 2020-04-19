import pandas as pd


def merge_data(data_sales, data_store, remove_outliers=False):
    data_merged = data_sales.merge(data_store, left_on='Store', right_on='Store', how='left')
    if remove_outliers:
        # One store with a huge number of customers
        data_merged = data_merged[data_merged['Customers'] <= 6000]
        # Two stores with competition before 1980
        data_merged = data_merged[(data_merged['CompetitionOpenSinceYear'] >= 1980) | 
                                  (data_merged['CompetitionOpenSinceYear'] == 0.)]
        # Two stores with competition distance >= 5000
        data_merged = data_merged[data_merged['CompetitionDistance'] <= 5000]
    return data_merged


def preprocessing(data_sales, data_store, remove_outliers=False):
    # features
    features = []
    # convert date to datetime
    data_sales['Date'] = pd.to_datetime(data_sales['Date'], format='%Y-%m-%d')
    # assume store open, if not provided
    data_sales.fillna(1, inplace=True)
    # consider only open stores for training
    data_sales = data_sales[data_sales['Open'] != 0]
    # merge sales and store
    data = merge_data(data_sales, data_store, remove_outliers=remove_outliers)
    # remove NaNs
    data['CompetitionDistance'].fillna(data['CompetitionDistance'].median(), inplace=True)
    data.fillna(0, inplace=True)
    data.loc[data.Open.isnull(), 'Open'] = 1
    # Use some properties directly
    features.extend(['Store', 'CompetitionDistance', 'Promo', 'Promo2', 'SchoolHoliday'])
    # Label encode some features
    features.extend(['StoreType', 'Assortment', 'StateHoliday'])
    data['StoreType'] = data['StoreType'].map({'a': 0, 'b': 3, 'c': 2, 'd': 1})
    data['Assortment'] = data['Assortment'].map({'a': 0, 'b': 2, 'c': 1})
    data['StateHoliday'] = data['StateHoliday'].map({0: 0, '0': 0, 'a': 1, 'b': 1, 'c': 1})
    features.extend(['DayOfWeek', 'Month', 'Day', 'Year', 'WeekOfYear'])
    data['Year'] = data.Date.dt.year
    data['Month'] = data.Date.dt.month
    data['Day'] = data.Date.dt.day
    data['WeekOfYear'] = data.Date.dt.weekofyear
    # Calculate time competition open time in months
    features.append('CompetitionOpen')
    data['CompetitionOpen'] = 12 * (data.Year - data.CompetitionOpenSinceYear) + \
        (data.Month - data.CompetitionOpenSinceMonth)
    # Promo open time in months
    features.append('PromoOpen')
    data['PromoOpen'] = 12 * (data.Year - data.Promo2SinceYear) + (data.WeekOfYear - data.Promo2SinceWeek) / 4.0
    data['PromoOpen'] = data.PromoOpen.apply(lambda x: x if x > 0 else 0)
    data.loc[data.Promo2SinceYear == 0, 'PromoOpen'] = 0
    return data, features
