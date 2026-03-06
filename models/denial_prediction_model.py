import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

df = pd.read_csv("cleaned_claim_dataset.csv")

features = [
    "Department",
    "Procedure_Code",
    "Insurance_Type",
    "Claim_Amount",
    "Documentation_Delay_Days",
    "Length_of_Stay",
    "Previous_Denial_Count"
]

target = "Denial_Flag"

X = df[features].copy()
y = df[target]

numeric_features = [
    "Claim_Amount",
    "Documentation_Delay_Days",
    "Length_of_Stay",
    "Previous_Denial_Count"
]

scaler = StandardScaler()
X.loc[:, numeric_features] = scaler.fit_transform(X[numeric_features])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=2000, class_weight="balanced")

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_prob)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("ROC-AUC:", roc_auc)

df["Denial_Probability"] = model.predict_proba(X)[:, 1]

def risk_level(p):
    if p < 0.3:
        return "Low"
    elif p < 0.7:
        return "Medium"
    else:
        return "High"

df["Risk_Level"] = df["Denial_Probability"].apply(risk_level)

predictions = df[["Claim_ID", "Denial_Probability", "Risk_Level"]]
predictions.to_csv("denial_model_predictions.csv", index=False)

metrics = pd.DataFrame({
    "Accuracy":[accuracy],
    "Precision":[precision],
    "Recall":[recall],
    "F1_Score":[f1],
    "ROC_AUC":[roc_auc]
})

metrics.to_csv("denial_model_metrics.csv", index=False)

print("Denial prediction model completed")