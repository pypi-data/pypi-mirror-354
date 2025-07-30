# TMLearner
***tmlearner* is a library that allows for training and using custom TrackMania AIs with machine learning.** It works with any version of TrackMania - or any game that uses only arrow keys, this library trains a TrackMania bot to play just like your style of driving, by feeding the neural network screenshots to predict the next keys to press
**Note: `tmlearner` must be run with administrator privileges for the `keyboard` module to work when tabbed out, which is essential for use.** 
# Features
| Feature | Support |
|--|--|
|Screenshot input|✅Supported|
|Other data (yaw, speed) input|🟥Not supported|
|Digital output|✅Supported|
|Analog output|🟨Coming soon|
# Documentation
The *tmlearner* library has two main files, the main `TMLearner` class, and two functions named `wasd_key_test` and `arrow_key_test` for testing input functionality.
## Input Testing
Execute the `wasd_key_test` and `arrow_key_test` functions depending on the keys that you prefer to test as input. Then, press some keys to test.
Example usage of the test functions:
```
>>> from tmlearner import wasd_key_test, arrow_key_test
>>> wasd_key_test()
Press some WASD keys.
*User presses keys*
W pressed
A pressed
D pressed
W pressed
S pressed
S pressed
KeyboardInterrupt
>>> arrow_key_test()
*User pressed keys*
up pressed
left pressed
down pressed
up pressed
right pressed
down pressed
down pressed
```
# TMLearner Class

## Initialization
The `TMLearner` class is the main class used to create datasets, train models, and test models.
Example usage of the `TMLearner` class:
```
>>> from tmlearner import TMLearner
>>> bot = TMLearner()
```
The various parameters are shown here:
| Parameter | Description | Type |
|--|--|--|
|`name` | The name of the bot. The files will be named with this name. | `str` |
|`keys` | Should be "WASD" or "ARROW". Which set of keys you will be pressing as input. | `str` |
|`data_capture_interval` | The delay in seconds to capture frames when creating a dataset. | `int, float` |
|`exec_capture_interval` | The delay in seconds to capture frames when using the model. | `int,  float` |
|`save_frequency` | The frequency to save the database when creating a database. Set to `None` for no auto-saving. | `int,  None` |
|`img_size` |The size images are scaled to for training | `tuple` |
|`nn_arch` | The architecture of the neural network. | `tuple` |
|`nn_random_state` |The random state of the neural network. Use for reproducibility. | `int` |
|`nn_test_percentage` | The percentage of the dataset to hold for testing. | `float` |
|`verbose` | Whether to allow printing debug data. Some critical information will be printed regardless. | `bool` |

## Deleting the Files
`TMLearner.delete_database` method will delete the database file, the image folder, and the model file. Coming soon: Delete database but keep model.
Example usage:
```
>>> bot.delete_database()
Deleted all of tmlearner_bot data.
```

## Dataset Creation
`TMLearner.create_database` creates/adds to the existing database. You will be prompted to press [ENTER], and a 5 second countdown will commence. When it ends, data (screenshots + keys) will start being recorded. Hold the stop key, 'z', for about twice your `data_capture_interval` to stop and save.
Example usage:
```
>>> bot.create_database()
Press [ENTER] to begin recording.
You will have 5 seconds to switch to TM.
Hold 'x' for about 0.5 seconds to stop.
DO NOT keyboard interrupt.

*user presses [ENTER]*
5... 4... 3... 2... 1...
GO!

Capture 1 complete. State: (False, False, True, False)
Capture 2 complete. State: (False, True, True, False)
Capture 3 complete. State: (False, True , True, False)
Capture 4 complete. State: (True, False, False, False)
*user presses 'z'*
Stopping and saving.
```
The dataset will be created and saved.

## Model Training
`TMLearner.train_model` function will train the neural network with the specified settings and save in a local file.
Example usage:
```
>>> bot.train_model()
*various debug message showing progress (if verbose), and final print showing accuracy*
```
## Using the Model
`TMLearner.run_model` will actually use the model, giving the user 5 seconds to switch to the TrackMania window, before taking screenshots, running them through the model, and executing the output. The `TMLearner.exec_capture_interval` parameter will control the frequency that images are taken and processed.
Example usage:
```
>>> bot.run_model()
Press [ENTER] to begin. You will have 5 seconds to switch to TM.

*user presses [ENTER]*
5... 4... 3... 2... 1...
GO! (Ctrl+C to stop)

Prediction: (False, False, True, False)
Prediction: (False True, True, False)
Prediction: (True, False, False, True)
*user pressed Ctrl+C*
Stopping. Releasing all keys.
Done
```
# Version History

## 1.1.0
- First release.
