import os
import time
import pickle
import uuid
import shutil

import numpy as np
from mss import mss
from PIL import Image
import keyboard
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
import joblib
from pynput.keyboard import Key, Controller
kb = Controller()

# VARIABLES

KEYS_TO_STRING_LIST = {
    "WASD": ["a", "d", "w", "s"],
    "ARROW": ["left", "right", "up", "down"]
}
KEYS_TO_PYNPUT_LIST = {
    "WASD": ["w", "d", "w", "s"],
    "ARROW": [Key.left, Key.right, Key.up, Key.down]
}

# TM LEARNER CLASS

class TMLearner:
    def __init__(self,
                 name:str="tmlearn_bot",
                 keys:str="WASD",
                 data_capture_interval:int | float=0.3,
                 exec_capture_interval:int | float=0.1,
                 save_frequency:int | None=100,
                 img_size:tuple=(128, 128),
                 nn_arch:tuple=(128, 32, 16),
                 nn_random_state:int=42,
                 nn_test_percentage:float=0.2,
                 verbose:bool=True
                 ):
        """
        Parameters:
            name (str): The name of the bot. The files will be named with this name.
            keys (str): Should be "WASD" or "ARROW". Which set of keys you will be pressing as input.
            data_capture_interval (int | float): The delay in seconds to capture frames when creating a dataset.
            exec_capture_interval (int | float): The delay in seconds to capture frames when using the model.
            save_frequency (int | None): The frequency to save the database when creating a database. Set to None for no auto-saving.
            img_size (tuple): The size the image should be scaled to when formatted as training data.
            nn_arch (tuple): The architecture of the neural network.
            nn_random_state (int): The random state of the neural network. Use for reproducibility,
            nn_test_percentage (float): The percentage of the dataset to hold for testing.
            verbose (bool): Wether to allow printing debug data. Some critical information will be printed regardless.
        """
        self.name = name
        self.img_folder_name = name + "_images"
        self.data_file_name = name + "_data.pkl"
        self.model_file_name = name + "_model"

        self.input_keys = KEYS_TO_STRING_LIST[keys]
        self.output_keys = KEYS_TO_PYNPUT_LIST[keys]

        self.data_capture_interval = data_capture_interval
        self.exec_capture_interval = exec_capture_interval
        self.save_frequency = save_frequency

        self.img_size = img_size
        self.nn_arch = nn_arch
        self.nn_random_state = nn_random_state
        self.nn_test_percentage = nn_test_percentage

        self.verbose = verbose

    def delete_database(self):
        """
        Deletes all of the files of this bot.
        """
        try:
            os.remove(self.img_folder_name)
        except:
            pass
        try:
            os.remove(self.model_file_name)
        except:
            pass
        try:
            shutil.rmtree(self.img_folder_name)
        except:
            pass
        print(f"Deleted all {self.name} data.")

    def print(self, text, newline:bool=False):
        """ Print the text if verbose. """
        if self.verbose:
            print(text, "\n" if newline else "")

    # DATABASE

    def _load_database(self) -> list:
        """ Load the current database, or create a new one."""
        # Create/ensure exists the images folder
        os.makedirs(self.img_folder_name, exist_ok=True)

        try:
            # Check for the database
            with open(self.data_file_name, "rb") as f:
                data = pickle.load(f)
                self.print(f"Loaded {len(data)} existing entries.")
        except (FileNotFoundError, EOFError):
            # The database does not exist
            data = []
            self.print("No existing data found, starting new list.")

        return data
    
    def _save_database(self, data):
        """ Save the database given. """
        with open(self.data_file_name, "wb") as f:
            pickle.dump(data, f)

    def create_database(self):
        """
        Creates/adds to the existing database.
        You will be prompted to press [ENTER], and a 5 second countdown will commence. When it ends, data (screenshots + keys)
        will start being recorded. Hold the stop key, 'z' for about twice your data_capture_interval to stop and save.
        """
        data = self._load_database()

        # Wait for the user
        input(f"Press [ENTER] to begin recording.\nYou will have 5 seconds to switch to TM.\nHold 'x' for about {self.data_capture_interval * 2} seconds to stop.\nDO NOT keyboard interrupt.\n")
        for i in range(5, 0, -1):
            self.print(f"{i}...", newline=False)
            time.sleep(1)

        self.print("GO!")

        # Initalize the variables
        sct = mss()
        frames = 0

        while True:
            start = time.time()

            # Check if the stop key is pressed
            if keyboard.is_pressed("z"):
                self.print("Stopping and saving.")
                break

            # Setup the image path and name
            uuid_ = uuid.uuid4()
            img_name = f"img_{uuid_}.png"
            img_path = os.path.join(self.img_folder_name, img_name)

            # Take a screenshot, and save it
            sct_img = sct.grab(sct.monitors[0])
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(img_path)

            # Get the key states, for WASD or ARROW
            state = (
                keyboard.is_pressed(self.input_keys[0]),
                keyboard.is_pressed(self.input_keys[1]),
                keyboard.is_pressed(self.input_keys[2]),
                keyboard.is_pressed(self.input_keys[3])
            )

            # Add the data.
            data.append((img_path, state))

            # Print a debug message, proving that the keys are working.
            frames += 1
            self.print("Capture {} complete. State: {}".format(frames, state))

            # Auto-save if requested
            if self.save_frequency:
                if  frames % self.save_frequency == 0:
                    self._save_database(data)
                    self.print("Auto-saving data.")

            # Calculate the desired time to wait, and sleep.
            desired_time = start + self.data_capture_interval
            time_left = desired_time - start
            time.sleep(time_left)

        # When broken, save the database
        self._save_database(data)

    # TRAIN MODEL
    def _get_formatted_data(self):
        # Load the data from the file
        data = self._load_database()
        if not data:
            raise ValueError("No entried in database.")
        
        # Format the data and save in X and y lists for training
        X = []
        y = []
        for img_path, keys in data:
            if not os.path.exists(img_path):
                print(f"Warning: {img_path} not found, skipping.")
                continue

            # Load, convert to grayscale, resize, and flatten.
            img = Image.open(img_path).convert('L')
            img = img.resize(self.img_size)
            arr = np.array(img, dtype=np.float32).flatten() / 255.0
            X.append(arr)
            # Convert boolean tuple to integers (0 or 1)
            y.append([int(key) for key in keys])

            if len(y) % 100 == 0:
                print("{} Images loaded.".format(len(y)))

        # Convert the data into an array.
        X = np.array(X)
        y = np.array(y, dtype=int)
        return X, y
    
    def train_model(self):
        """
        Trains the neural network and saves the result.
        """
        # Retrive the data
        self.print("Loading data...")
        X, y = self._get_formatted_data()
        self.print(f"Loaded {X.shape[0]} samples.")

        # Split the data into the test and train sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.nn_test_percentage, random_state=self.nn_random_state
        )
        self.print(f"Train set size: {X_train.shape[0]}. Test set size: {y_train.shape[0]}.")

        # Create the base MLP Classifier
        base_clf = MLPClassifier(
            hidden_layer_sizes=self.nn_arch,
            activation="relu",
            solver="adam",
            max_iter=250,
            random_state=self.nn_random_state,
            verbose=self.verbose
        )
        # Wrap the classifier for multi-output classification
        clf = MultiOutputClassifier(base_clf)

        # Fit the model
        self.print("Training model...")
        clf.fit(X_train, y_train)

        # Evaluate the performance and show
        y_pred = clf.predict(X_test)
        self.print(classification_report(
            y_test, y_pred,
            target_names=["Left", "Right", "Up", "Down"]
        ))

        # Save the trained model
        joblib.dump(clf, self.model_file_name)
        self.print(f"Saved model to {self.model_file_name}")

    # RUN MODEL

    def _load_model(self):
        if not os.path.exists(self.model_file_name):
            raise FileNotFoundError(f"Model file '{self.model_file_name}' not found!")
        
        clf = joblib.load(self.model_file_name)

        self.print(f"Loaded model from '{self.model_file_name}'")
        return clf
    
    def _get_single_frame(self):
        """ Return a formatted screenshot. """
        # Get the screenshot
        sct = mss()
        sct_img = sct.grab(sct.monitors[0])

        # Format it
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img = img.convert('L').resize(self.img_size)
        arr = np.array(img, dtype=np.float32).flatten() / 255.0

        # Return it
        return arr
    
    def _apply_keys(self, state, prev_state) -> tuple:
        # State is a tuple of 4 bools
        for idx, key in enumerate(self.output_keys):
            if state[idx] and not prev_state[idx]:
                kb.press(key)
            elif not state[idx] and prev_state[idx]:
                kb.release(key)

        return state

    def run_model(self):
        # Load the CLF
        clf = self._load_model()

        # Wait for the user
        input("Press [ENTER] to begin. You will have 5 seconds to switch to TM.\n")
        for i in range(5, 0, -1):
            self.print(f"{i}... ")
            time.sleep(1)
        print("GO! (Ctrl+C to stop)")

        # Setup the loop, and loop
        prev_state = (False,) * 4
        try:
            while True:
                # Get the screenshot
                frame = self._get_single_frame()

                # Make the prediction
                pred = clf.predict([frame])[0]

                # Press the keys and set the state and prev_state variables
                state = tuple(bool(x) for x in pred)
                prev_state = self._apply_keys(state, prev_state)

                print(f"Prediction: {state}")

                # Wait
                time.sleep(self.exec_capture_interval)

        except KeyboardInterrupt:
            print("\nStopping. Releasing all keys.")

            # Release any held keys
            for idx, key in enumerate(self.output_keys):
                if prev_state[idx]:
                    kb.release(key)
            
            # Finished
            print("Done")
            exit()