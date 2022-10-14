# load model.pth and use it to predict the budget line for a new transaction
import os
import torch
import logging

from net import Net

logger = logging.getLogger(__name__)
# log to console
logger.addHandler(logging.StreamHandler())
if os.environ.get('DEBUG'):
    logger.setLevel(logging.DEBUG)



class Model:
    def __init__(self, model_path = 'model.pth', input_size = 54, hidden_size = 128, output_size = 15):
        self.input_size = input_size
        self.output_size = output_size

        self.model = Net(input_size, hidden_size, output_size)
        
        if not model_path:
            logger.info('No model path provided, initializing a new model')
        elif os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path))
            logger.info('Loaded model')
        else:
            logger.info('Model path does not exist, initializing a new model')

    
    def save(self, model_path = 'model.pth'):
        torch.save(self.model.state_dict(), model_path)
        logger.info('Saved model')

    def train(self, X: torch.Tensor, y: torch.Tensor, epochs: int = 1000):
        # check if X and y are the correct shape
        assert X.shape[1] == self.input_size
        assert y.shape[1] == self.output_size

        assert X.shape[0] == y.shape[0]

        # Create a loss function
        loss_fn = torch.nn.MSELoss(reduction='sum')

        # Create an optimizer
        learning_rate = 1e-4
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)

        # separate the data into training and testing
        X_train = X[:int(len(X) * 0.8)]
        X_test = X[int(len(X) * 0.8):]

        y_train = y[:int(len(y) * 0.8)]
        y_test = y[int(len(y) * 0.8):]

        # train the model
        for t in range(epochs):
            # Forward pass: compute predicted y by passing x to the model.
            y_pred = self.model(X_train)

            # Compute and print loss.
            loss = loss_fn(y_pred, y_train)
            if t % 100 == 99:
                print(t, loss.item())

            # Zero gradients, perform a backward pass, and update the weights.
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # test the model
        with torch.no_grad():
            y_pred = self.model(X_test)
            loss = loss_fn(y_pred, y_test)
            print("Test loss:", loss.item())

    def predict(self, one_hot: torch.Tensor):
        # one_hot = description_to_one_hot(description)
        # one_hot = torch.tensor(one_hot, dtype=torch.float32)
        prediction = self.model(one_hot)
        return prediction


