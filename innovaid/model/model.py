from pathlib import Path

from sktime.classification.interval_based import TimeSeriesForestClassifier
from sktime.datasets import load_arrow_head
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from Innovaid2023.innovaid.dataloading.loader import load_gt, load_set

samples = load_set(Path("data/processed/samples"))
gt = load_gt(Path("data/processed/ground_truth.csv"))
X_train, X_test, y_train, y_test = train_test_split(X, y)

classifier = TimeSeriesForestClassifier()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
score = accuracy_score(y_test, y_pred)

print(score)
