# Game2048 with Keras neural network

You can run the neural network in 2 ways.

1. From CLI - 'python nn.py start'
2. From an IDE like Spyder. To run it like this make sure you comment out cli() and put start() back

If you have problems running the cli version you might want to use Anaconda prompt
or make sure you have installed corect packages.

*******
cli args

--print_board True|False

  Specifies if the board should be printed while it is being played

--transform_dataset True|False

  If set to False then cached transformed dataset will be loaded
  Fallbacks to creating a new dataset

--retrain_model True|False

  Specifies if the model should be compiled and fit with the dataset
  By default it will try to use a cached model and fallbacks to creating a new one

--games Number

  Number of games to play by the Neural Network

--games feature_scaler

  Choose which feature scaler method to use.
  one_hot | log_2 | square_root
  Default is None

--color True|False

  For Window's CMD that do not work well with color printing. True turns it on,
  False turns it off. Default is True.