from regressalot.models import (
    run_random_forest,
    run_xgboost,
    run_linear_regression,
    run_decision_tree
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt

class AutoMLRunner:
    def __init__(self, data, target, task='classification'):
        self.df = pd.read_csv(data) if isinstance(data, str) else data
        self.target = target
        self.task = task
        features = self.df.drop(columns=[target])
        self.X = pd.get_dummies(features, drop_first=True)
        self.y = self.df[target]

    def run(self):
        results = {}
        predictions = {}
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        print("Running Linear Regression...")
        lr_model, lr_preds = run_linear_regression(X_train, X_test, y_train, self.task)
        results["Linear Regression"] = self.evaluate(lr_preds, y_test, lr_model, X_train, y_train, return_score=True)
        predictions["Linear Regression"] = (y_test, lr_preds)

        print("Running Decision Tree...")
        dt_model, dt_preds = run_decision_tree(X_train, X_test, y_train, self.task)
        results["Decision Tree"] = self.evaluate(dt_preds, y_test, dt_model, X_train, y_train, return_score=True)
        predictions["Decision Tree"] = (y_test, dt_preds)

        print("Running Random Forest...")
        rf_model, rf_preds = run_random_forest(X_train, X_test, y_train, self.task)
        results["Random Forest"] = self.evaluate(rf_preds, y_test, rf_model, X_train, y_train, return_score=True)
        predictions["Random Forest"] = (y_test, rf_preds)

        print("Running XGBoost...")
        xgb_model, xgb_preds = run_xgboost(X_train, X_test, y_train, self.task)
        results["XGBoost"] = self.evaluate(xgb_preds, y_test, xgb_model, X_train, y_train, return_score=True)
        predictions["XGBoost"] = (y_test, xgb_preds)

        print("\nModel Performance Summary (Ranked by Test R^2):")
        sorted_models = sorted(results.items(), key=lambda item: item[1].get("Test R^2", 0), reverse=True)
        for i, (model, metrics) in enumerate(sorted_models, 1):
            print(f"{i}. {model}:")
            for metric, value in metrics.items():
                if isinstance(value, (int, float)):
                    print(f"   {metric}: {value:.4f}")
                else:
                    print(f"   {metric}: {value}")

        self.plot_predictions(predictions)

    def evaluate(self, preds, y_true, model=None, X_train=None, y_train=None, return_score=False):
        if self.task == 'classification':
            acc = accuracy_score(y_true, preds)
            if return_score:
                return {"Accuracy": acc}
            print("Accuracy:", acc)
        elif self.task == 'regression':
            rmse = mean_squared_error(y_true, preds) ** 0.5
            r2 = r2_score(y_true, preds)
            eps = 1e-10
            rmspe = ((100 * ((y_true - preds) / (y_true + eps))**2).mean()) ** 0.5
            over_preds = sum(preds > y_true)
            under_preds = sum(preds < y_true)

            train_rmse = mean_squared_error(y_train, model.predict(X_train)) ** 0.5 if model else None
            train_r2 = r2_score(y_train, model.predict(X_train)) if model else None

            overfit_flag = "Yes" if train_r2 is not None and train_r2 - r2 > 0.1 else "No"

            if return_score:
                return {
                    "Test RMSE": rmse,
                    "Test R^2": r2,
                    "Train RMSE": train_rmse,
                    "Train R^2": train_r2,
                    "RMSPE": rmspe,
                    "Over-predictions": over_preds,
                    "Under-predictions": under_preds,
                    "Overfitting": overfit_flag
                }
            print("Test RMSE:", rmse)
            print("Test R^2:", r2)
            print("Train RMSE:", train_rmse)
            print("Train R^2:", train_r2)
            print("RMSPE:", rmspe)
            print("Over-predictions:", over_preds)
            print("Under-predictions:", under_preds)

    def plot_predictions(self, predictions):
        for model_name, (y_true, y_pred) in predictions.items():
            plt.figure(figsize=(6, 4))
            plt.scatter(y_true, y_pred, alpha=0.6)
            plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
            plt.xlabel("Actual")
            plt.ylabel("Predicted")
            plt.title(f"Actual vs Predicted - {model_name}")
            plt.grid(True)
            plt.tight_layout()
            plt.show()