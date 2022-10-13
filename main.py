import pandas as pd
import torch

from Data import ModelData
from Model import Model

def main():
    # load the data
    data_path='data/data.csv'
    meta_path = 'data/meta_data.pkl'
    model_path = 'data/model.pth'

    # model_data = ModelData(data_path, meta_path)
    # model_data.save_meta_data(meta_path)
    raw_data_path = 'statements/statement.csv'
    raw_data = pd.read_csv(raw_data_path)
    # model_data = ModelData(raw_data)
    model_data = ModelData(data_path='data/data.csv', meta_path='meta_data.pkl')

    # create the model
    model = Model(model_path='', input_size=len(model_data.word_list), hidden_size=128, output_size=len(model_data.class_names))

    X = model_data.X
    # convert the data to tensors
    X = torch.tensor(model_data.X.to_numpy(), dtype=torch.float)
    y = torch.tensor(model_data.y.to_numpy(), dtype=torch.float)

    # train the model
    model.train(X, y, epochs=1000)

    # save the model
    model.save('model.pth')

    # prompt the user for description
    description = input('Enter a description: ')

    while description != 'exit':
        # predict the class
        inp = model_data.description_to_one_hot(description)
        inp = torch.tensor(inp, dtype=torch.float).unsqueeze(0)
        out = model.predict(inp).squeeze(0).argmax().item()
        # out = out.detach().numpy()
        # out = out.argmax()
        prediction = model_data.class_names[out]
        # prediction = model_data.one_hot_to_class(out)
        print(prediction)
        description = input('Enter a description: ')


if __name__ == '__main__':
    main()