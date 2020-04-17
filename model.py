import numpy as np


def rmse(y_true, y_pred):
    loss = np.sqrt(np.mean((y_true - y_pred)**2, axis=0))
    return loss


def rmse_XGBoost(y_pred, y_true):
    y_true = y_true.get_label()
    y_pred = y_pred
    return "rmse", rmse(y_true, y_pred)


def create_feature_map(features, feature_map_path):
    outfile = open(feature_map_path, 'w')
    for i, feat in enumerate(features):
        outfile.write('{0}\t{1}\tq\n'.format(i, feat))
    outfile.close()
