import os
import re
import readline
import pandas as pd
import pickle
from dataclasses import dataclass

from log import logger

@dataclass
class LabelData:
    """LabelData class
    """
    X: pd.Series
    y: pd.Series


@dataclass
class OneHotData:
    """OneHotData class
    """
    X_keys: pd.Series
    y_keys: pd.Series
    X: pd.DataFrame
    y: pd.DataFrame


def classify_data(data: list[str]) -> LabelData:
    """classify_data function
    """
    X = pd.Series(data)
    y = pd.Series(['']*len(X))
    y_unique = []

    # set up auto complete
    def complete(text,state):
        vocab = y_unique
        results = [x for x in vocab if x.lower().startswith(text.lower())] + [None]
        return results[state]
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    # classify data
    for index, entry in enumerate(X):
        # prompt the user for a class name
        class_name = input(f'Classify "{entry}" as: ')
        if class_name == '':
            class_name = 'Other'
        if class_name == 'q':
            break
        y[index] = class_name

        # add the class name to the list of class names
        if class_name not in y_unique:
            y_unique.append(class_name)

    return LabelData(X, y)

def data_to_one_hot(data: LabelData) -> OneHotData:
    """data_to_one_hot function
    """
    freq_map = {}
    for line in data.X:
        words = re.split(' |/|-', line)
        for word in words:
            if word in freq_map and not word.isnumeric():
                freq_map[word] += 1
            else:
                freq_map[word] = 1

    # remove words that only appear once
    freq_map = {k: v for k, v in freq_map.items() if v > 1}

    X_keys = pd.Series(list(freq_map.keys()))
    y_keys = pd.Series(data.y.unique())

    X = data.X.apply(lambda x: pd.Series([1 if word in re.split(' |/|-', x) else 0 for word in X_keys]))
    y = data.y.apply(lambda x: pd.Series([1 if word == x else 0 for word in y_keys]))

    return OneHotData(X_keys, y_keys, X, y)

class ModelData:
    def __init__(self, raw_data: pd.DataFrame = None, data_path: str = None, meta_path: str = None):
        self.raw_data = raw_data

        if self.raw_data is not None:
            self.word_list = self.create_word_list()
            # if self.raw_data has column 'Class', then it is training data
            if 'Class' in self.raw_data.columns:
                self.class_names = self.raw_data['Class'].unique()
            else:
                self.class_names = []
                self.classify_data()
            
            assert self.preprocess_data()

            self.save_meta_data('meta_data.pkl')
            self.save_data('data.csv')
        elif data_path and meta_path:
            assert self.load_data(data_path)
            self.word_list, self.class_names = self.load_meta_data(meta_path)
        else:
            logger.info('No data provided')
            self.X = None
            self.y = None
            self.word_list = None
            self.class_names = None


    def load_meta_data(self, meta_path: str):
        """
        Load the meta data from self.meta_path"""
        if not meta_path:
            logger.info('No meta path provided')
            return None
        elif os.path.exists(meta_path):
            with open(meta_path, 'rb') as f:
                meta_data = pickle.load(f)
            logger.info('Loaded meta data')
            return meta_data['word_list'], meta_data['class_names']
        else:
            logger.info('Meta path does not exist')
            return None

    def save_meta_data(self, meta_path: str):
        """
        Save the meta data to meta_path"""
        if not meta_path:
            logger.info('No meta path provided')
        else:
            meta_data = {
                'word_list': self.word_list,
                'class_names': self.class_names
            }
            with open(meta_path, 'wb') as f:
                pickle.dump(meta_data, f)
            logger.info('Saved meta data')

    def description_to_one_hot(self, description):
        """
        Create a one-hot vector for each word in the word_list
        
        Returns: one_hot (list)"""
        words = re.split(' |/|-', description)
        one_hot = [0] * len(self.word_list)
        for word in words:
            word = word.upper()
            if word in self.word_list:
                one_hot[self.word_list.index(word)] = 1

        return one_hot
    
    def one_hot_to_class(self, one_hot):
        """
        Convert a one-hot vector to a class name
        
        Returns: class_name (str)"""
        return self.class_names[one_hot]

    def preprocess_data(self):
        """
        Create a one-hot vector for each word in the word_list
        
        Returns: X (pandas.DataFrame), y (pandas.DataFrame)"""
        # create a dataframe with the words as columns
        X = pd.DataFrame(columns=self.word_list)

        # add a column for the classification
        for index, row in self.raw_data.iterrows():
            # create a one-hot vector for each word in the word_list
            one_hot = self.description_to_one_hot(row['Description'])

            X.loc[index] = one_hot

        try:
            y = self.raw_data['Class'].apply(lambda x: self.class_names.index(x))
        except KeyError:
            logger.info('No Class column in raw_data')
            return False

        # convert y to one-hot
        y = pd.get_dummies(y)

        self.X = X
        self.y = y

        return True


    def classify_data(self):
        """
        Classify the data in self.raw_data by prompting the user for a class name for each row"""
        readline.parse_and_bind("tab: complete")

        def complete(text,state):
            volcab = self.class_names
            results = [x for x in volcab if x.lower().startswith(text.lower())] + [None]
            return results[state]

        readline.set_completer(complete)

        # add a column for the classification
        for index, row in self.raw_data.iterrows():
            # prompt the user for a class name
            class_name = input(f'Classify "{row["Description"]}" - ${row["Transaction Amount"]:.2f} as: ')
            if class_name == '':
                class_name = 'Other'
            if class_name == 'q':
                break
            self.raw_data.loc[index, 'Class'] = class_name

            # add the class name to the list of class names
            if class_name not in self.class_names:
                self.class_names.append(class_name)


    def load_data(self, data_path: str):
        """
        Load the data from self.data_path"""
        if not data_path:
            logger.info('No data path provided')
            return None
        elif os.path.exists(data_path):
            data = pd.read_csv(data_path, index_col=False)
            logger.info('Loaded data')
            X = data.drop('Class', axis=1)
            y = data['Class']
            y = pd.get_dummies(y)
            self.X = X
            self.y = y
            return True
        else:
            logger.info('Data path does not exist')
            return None

    def save_data(self, data_path: str):
        """
        Save the data to data_path"""
        if not data_path:
            logger.info('No data path provided')
        else:
            data = pd.concat([self.X, self.y], axis=1)
            data.to_csv(data_path, index=False)
            logger.info('Saved data')

    def create_word_list(self):
        """
        Create a list of keywords from the Description column of self.raw_data
        
        Returns: word_list (list)"""
        word_list = {}
        for description in self.raw_data['Description']:
            words = re.split(' |/|-', description)[:-2]
            for word in words:
                if len(word) >= 2 and not word.replace('#', '').isnumeric():
                    if word not in word_list:
                        word_list[word] = 1
                    else:
                        word_list[word] += 1
                
        # remove words that only appear once
        word_list = {k: v for k, v in word_list.items() if v > 1}

        # convert to list of keys
        word_list = list(word_list.keys())

        return word_list