import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================
# Load data
# =========================
file_path = r"R:\Ponds_Sites.csv"
data = pd.read_csv(file_path)

# Features and target
features = [
    'Soil Moisture', 'Soil Organic Matter', 'Permeability', 'Temperature',
    'Turbidity', 'Rainfall', 'NDVI', 'GWL', 'TWI', 'Curve Number'
]
target = 'Recharge'

X = data[features]
y = data[target]

# Output folder
output_folder = r"R:\Phd_KHU\Research_work\IWMI\Moradabad_zone\New\Model_Outputs"
os.makedirs(output_folder, exist_ok=True)

# =========================
# Models and parameter grids
# =========================
models = {
    "XGBoost": {
        "model": xgb.XGBRegressor(random_state=42, objective='reg:squarederror'),
        "params": {
            'n_estimators': [50, 100, 150, 200],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'max_depth': [3, 5, 7, 10],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 1.0]
        },
        "scale": True
    },
    "GradientBoost": {
        "model": GradientBoostingRegressor(random_state=42),
        "params": {
            'n_estimators': [50, 100, 150, 200],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'max_depth': [3, 5, 7],
            'subsample': [0.8, 0.9, 1.0]
        },
        "scale": True
    },
    "RandomForest": {
        "model": RandomForestRegressor(random_state=42),
        "params": {
            'n_estimators': [50, 100, 150, 200],
            'max_depth': [3, 5, 7, 10, None],
            'max_features': ['sqrt', 'log2', None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        },
        "scale": False
    }
}

# =========================
# Run each model
# =========================
for model_name, model_info in models.items():
    print(f"\nRunning {model_name}...\n")

    mse_list = []
    r2_list = []
    feature_importances = []
    best_params_list = []

    for epoch in range(100):
        print(f"{model_name} - Epoch {epoch+1}/100")

        # Random split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=np.random.randint(0, 1000)
        )

        # Scaling where needed
        if model_info["scale"]:
            scaler = StandardScaler()
            X_train_model = scaler.fit_transform(X_train)
            X_test_model = scaler.transform(X_test)
        else:
            X_train_model = X_train
            X_test_model = X_test

        # Base model
        base_model = model_info["model"]

        # GridSearchCV
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=model_info["params"],
            scoring='r2',
            cv=5,
            verbose=0,
            n_jobs=-1
        )

        grid_search.fit(X_train_model, y_train)
        best_model = grid_search.best_estimator_

        # Prediction
        y_pred = best_model.predict(X_test_model)

        # Metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mse_list.append(mse)
        r2_list.append(r2)
        best_params_list.append(grid_search.best_params_)

        # Feature importance
        if hasattr(best_model, "feature_importances_"):
            feature_importances.append(best_model.feature_importances_)

    # =========================
    # Results summary
    # =========================
    feature_importances_df = pd.DataFrame(feature_importances, columns=features)
    feature_importances_df['Epoch'] = range(1, len(feature_importances) + 1)

    average_importances = feature_importances_df[features].mean().sort_values(ascending=False)

    print(f"\n{model_name} Results:")
    print(f"Average MSE over 100 epochs: {np.mean(mse_list):.4f}")
    print(f"Average R2 over 100 epochs: {np.mean(r2_list):.4f}")
    print(f"Best parameters from final epoch: {best_params_list[-1]}")

    # Save feature importances
    importance_csv = os.path.join(output_folder, f"{model_name}_Feature_Importance_100Epochs.csv")
    feature_importances_df.to_csv(importance_csv, index=False)

    # Save metrics
    metrics_df = pd.DataFrame({
        "Epoch": range(1, 101),
        "MSE": mse_list,
        "R2": r2_list
    })
    metrics_csv = os.path.join(output_folder, f"{model_name}_Metrics_100Epochs.csv")
    metrics_df.to_csv(metrics_csv, index=False)

    # Plot average feature importance
    plt.figure(figsize=(10, 6))
    sns.barplot(x=average_importances.values, y=average_importances.index)
    plt.title(f'Average Feature Importance Across 100 Epochs ({model_name})')
    plt.xlabel('Average Importance Score')
    plt.ylabel('Feature')
    plt.tight_layout()

    plot_path = os.path.join(output_folder, f"{model_name}_Average_Feature_Importance.png")
    plt.savefig(plot_path, dpi=300)
    plt.show()

print("\nAll models completed successfully.")
