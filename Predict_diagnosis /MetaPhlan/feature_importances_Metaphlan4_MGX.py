"""This program get metagenomic data on MetaPhlan4 format and spliting data it into features and targets to predict IBD illnesses.
In order to avoid overfitting, we only used one sample with greater calprotectin levels to represent the patient.
Furthermore,after dropping the feature, it calculates the top of feature importance to evaluate the accuracy.
When the accuracy is less than 90%, break the condition.

Input: Metagenomic data on MetaPhlan4 format of IBD patients.
Output: The species name and the test accuracy.
"""
# Upload packages
import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

METAPHLAN4MGX = pd.read_csv('~/Desktop/To_prediction/Metaphlan4_all_pheno.csv').rename(columns={'Unnamed: 0' : 'External ID'})
METAPHLAN4MGX = METAPHLAN4MGX.set_index('External ID')

select_sampels_MGX = pd.read_csv('~/Desktop/selected_samples_MGX.csv')
select_sampels_MGX = select_sampels_MGX.set_index('External ID')
select_sampels_MGX.drop("Participant ID", inplace=True, axis=1)

METAPHLAN4MGX = METAPHLAN4MGX.loc[select_sampels_MGX.index,:]
METAPHLAN4MGX = METAPHLAN4MGX.loc[:,METAPHLAN4MGX.columns.str.startswith('s__')]
METAPHLAN4MGX["diagnosis"] = select_sampels_MGX.iloc[:,-1]


# features = METAPHLAN4MGX.iloc[:, :-1]
important_species = {}
Accuracy = 100
while Accuracy > 70:
    features = METAPHLAN4MGX.iloc[:,:-1]
    print(f'Number of columns before drop:{len(features.columns)}')
    targets = METAPHLAN4MGX.iloc[:, -1]

    MGX_X = features
    MGX_y = targets

    #fill NA's
    MGX_X.fillna(MGX_X.median(), inplace=True)
    MTX_X = StandardScaler().fit_transform(MGX_X)

    X_train, X_test, y_train, y_test = train_test_split(MTX_X, MGX_y, test_size=0.30, random_state=42)

    # n_estimators_RF = [5, 10, 25, 50, 100]
    n_estimators_RF = [2]
    # max_features_RF = [2,4,8,16,32,None]
    max_features_RF = [2]
    parameters_RF = {'n_estimators': n_estimators_RF,
                    'max_features': max_features_RF}
    RF_model = RandomForestClassifier(max_depth=None,
                                      min_samples_split=5, random_state=42,criterion = 'entropy')
    RF_clf = GridSearchCV(RF_model, parameters_RF, cv=5, scoring= 'accuracy') # 'completeness_score','accuracy'
    RF_clf.fit(X_train, y_train)
    print("Best Model:")
    RF_model = RF_clf.best_estimator_
    print(RF_model)
    RF_predictions = RF_model.predict(X_test)

##########################################################################
    imp_df = pd.DataFrame({
    "": features.columns,
    "feature_importances": RF_clf.best_estimator_.feature_importances_
    })
    feature_importances = imp_df.sort_values(by="feature_importances", ascending=False).rename(columns={"":"feature_name"})
##########################################################################

    dominant_species = dict(zip(feature_importances.feature_name.iloc[:1], feature_importances.feature_importances.iloc[:1]))
    METAPHLAN4MGX = METAPHLAN4MGX.drop(list(dominant_species.keys()), axis=1) # Highest feature remove
    Accuracy = round(metrics.accuracy_score(y_test, RF_predictions) * 100, 2)
    important_species[frozenset(dominant_species.keys())] = f'{Accuracy}%'
    print(f'Number of columns after drop:{len(features.columns)}')
    print(dominant_species)
    print(f'Accuracy {Accuracy}%')

    print("########################################################################")
important_species = pd.DataFrame.from_dict(important_species, orient='index', columns=["Accuracy"])
print(important_species)