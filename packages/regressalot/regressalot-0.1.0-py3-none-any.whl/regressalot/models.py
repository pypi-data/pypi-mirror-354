from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
import xgboost as xgb

def run_random_forest(X_train, X_test, y_train, task):
    if task == 'classification':
        model = RandomForestClassifier()
    else:
        model = RandomForestRegressor(max_depth=8, min_samples_split=10, min_samples_leaf=5)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return model, preds

def run_xgboost(X_train, X_test, y_train, task):
    if task == 'classification':
        model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    else:
        model = xgb.XGBRegressor(max_depth=6, learning_rate=0.1, n_estimators=100, subsample=0.8, colsample_bytree=0.8)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return model, preds

def run_linear_regression(X_train, X_test, y_train, task):
    if task == 'classification':
        model = LogisticRegression(max_iter=1000)
    else:
        model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return model, preds

def run_decision_tree(X_train, X_test, y_train, task):
    if task == 'classification':
        model = DecisionTreeClassifier()
    else:
        model = DecisionTreeRegressor(max_depth=5, min_samples_split=10, min_samples_leaf=5)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return model, preds
