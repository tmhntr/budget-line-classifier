# AI Budget Line Classifier

 [![PyTorch](https://img.shields.io/badge/framework-pytorch-orange.svg)](https://pytorch.org/)

This app trains and utilizes a neural network to help classify credit card payments into categories based on the vendor description. Categories may be determined at runtime by the user. The algorithm requires a training dataset provided by the user (in the form of a credit card statement csv file, available from most banks).

The app prompts users to label the data, then trains the model based on these labels.

## Current functionality

- [x] Train neural network based on labeled data
- [x] Get data labels from user
- [x] Inference category based on description

<!-- add in a todo list -->

## Setup

To run this app, you will need to install the following:

- [Python](https://www.python.org/downloads/)
- [PyTorch](https://pytorch.org/get-started/locally/)
- [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
- [Numpy](https://numpy.org/install/)

## Usage

To run the app, use the following command:

```bash
python main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPL3](https://www.gnu.org/licenses/gpl-3.0.txt)

## Authors

- Timothy Hunter

## Todo

- [ ] Add in budgeting functionality (excel, visualizations, etc)
