import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
from create_xl_for_model import get_data


healthy = 1
sick = 0


def create_data(file_name, letter):
    df = pd.read_excel(file_name)
    df.drop(df.loc[df["type"] == -1].index, inplace=True)
    df = df.iloc[np.random.permutation(len(df))]  # shuffle
    if letter != 'all':
        df = df[[col for col in df.columns if col[0] == letter or col == 'type' or col == 'name']]
        df.drop(df.loc[df["type"] == -1].index, inplace=True)
    train_x, train_y = df[0:int(len(df)*0.6)].drop(["name", "type"], axis=1), df[0:int(len(df)*0.6)]["type"].values
    test_x, test_y = df[int(len(df)*0.6):len(df)].drop(["name", "type"], axis=1),\
                    df[int(len(df)*0.6):len(df)]["type"].values
    return train_x, train_y, test_x, test_y


def create_tree(file_name, func, model_dir_name):
    models = []
    for letter in ['all', "k", "p", "c", "o", "f", "g", "s"]:
        train_x, train_y, test_x, test_y, = create_data(file_name, letter)
        model = func()
        model.fit(train_x, train_y)

        prediction_tree = model.predict(test_x)

        counter = 0
        for i in range(len(prediction_tree)):
            if prediction_tree[i] == test_y[i]:
                counter += 1

        if letter == 'all':
            print("all letters")
        else:
            print('model for bacteria in letter ', letter)
        print(str(func))
        print(counter/len(test_y)*100)
        print()
        models.append(model)
        pickle.dump(model, open(model_dir_name + letter, 'wb'))
        with open(model_dir_name + letter + '_columns', 'wb') as f:
            pickle.dump(train_x.columns, f)

    return models


def predict_from_file(file_name):
    subject = get_data(file_name)
    predictions_for_file = {}
    for model in ['decision_tree_', 'forest_']:
        for l in ['all', "k", "p", "c", "o", "f", "g", "s"]:
            letter = model + l
            loaded_model = pickle.load(open('models/'+letter, 'rb'))
            loaded_columns = pickle.load(open('models/'+letter + '_columns', 'rb'))
            df = pd.DataFrame(columns=list(loaded_columns))
            letter_subject = {}
            for col in loaded_columns:
                letter_subject[col] = subject[col] if col in subject else 0
            df = df.append(letter_subject, ignore_index=True)
            prediction = loaded_model.predict(df)
            predictions_for_file[letter] = 'healthy' if prediction == healthy else 'sick'
    return predictions_for_file


def main():
    '''
    # create models and saves them
    file_name = "df_project.xlsx"
    funcs = [DecisionTreeClassifier, RandomForestClassifier]
    models = []
    for f in funcs:
        models_dir_name = 'models/'
        if f == DecisionTreeClassifier:
            models_dir_name += 'decision_tree_'
        else:
            models_dir_name += 'forest_'
        models.append(create_tree(file_name,  f, models_dir_name))
'''
    # opens saved models and predict for patient from file
    predictions_for_file = predict_from_file('project 1/SAMN03469222.txt')
    print(predictions_for_file)


main()
