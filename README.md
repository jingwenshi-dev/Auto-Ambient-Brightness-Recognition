# Auto Ambient Brightness Recognition

## Description

This application is create during [Deerhacks](https://www.deerhacks.ca/) hackathon in 2023.

This is an app which allows Windows laptop users to auto-adjust the screen brightness for whom does not have a light sensor.

## Run

To pack the whole python directory into an application, please follow the instruction below:

1.  `cd App`
2. Edit `main.py`:
   1. Replace line 14 with `weight_path = '../../Weight3.ckpt'`
   2. Replace line 100 with `cv2.imwrite("../../temp_img.png", frame)` 
   3. Replace line 101 with `self.result = predict_image(model, "../../temp_img.png").
3. `pip3 intall pyinstaller`
4. `pyinstaller --name=AutoBrightnessAdjuster main.py`
5. When finished, run `AutoBrightnessAdjuster.exe` under `dist` folder.

Otherwise:

1. Install all packages in `requirements.txt`
2. Run `main.py`

## Data Collection & Augmentation

The data collection process takes place at the University of Toronto, where team members utilize their phone cameras to record videos. Within each classroom, the lighting is adjustable to four levels. Team members capture videos of themselves walking within the lecture hall under various ambient brightness levels, aiming to record a diverse range of backgrounds to minimize bias and increase the dataset's variability.

Every fifteenth frame of each video is extracted and saved as a picture. Subsequently, the dataset is divided into training, validation, and test sets, with a ratio of 60:20:20, respectively.

## Model Implementation

The application used a Convolution Neural Network (CNN) to predict the ambient brightness and make a decision to adjust the screen brightness with 4 levels (i.e. 12%, 37%, 62%, 87%). 

##### Hyperparameters:

- Adam optimizer is used for faster convergence.
- Learning Rate: 0.001
- Momentum: 0.9
  - Empirically, this combination of LR and Momentum is well performed.
- Output Channels: 2
  - There is no need to implement a complex model for recognizing ambient brightness. Otherwise, a overfit will happen as tested so far.

##### Early Stopping:

- The fourth weight (i.e. [Wight3.ckpt](https://github.com/jingwenshi-dev/Auto-Ambient-Brightness-Recognition/blob/main/checkpoint/Weight3.ckpt)) is selected to be the final model to prevent overfit since validation and test accuracy has already reached 99%.

For more a detailed solution, please refer to [CNN.ipynb](https://github.com/jingwenshi-dev/Auto-Ambient-Brightness-Recognition/blob/main/CNN.ipynb).

## UI & Interface Implementation

At every second, the [application](https://github.com/jingwenshi-dev/Auto-Ambient-Brightness-Recognition/blob/main/App/main.py) will capture a 480p picture through the webcam and store it on your local computer only (i.e. no internet access needed). The application will also create a CNN object and load the weights into the model as the application started.

The [interface](https://github.com/jingwenshi-dev/Auto-Ambient-Brightness-Recognition/blob/main/App/ModelPredictionInterface.py) contains a CNN class and will read the stored weight. There is a function which takes a picture as the parameter and produces the asperate screen brightness.

## Limitation

The application's ability to auto-adjust the screen brightness is limited to four discrete levels due to the absence of a continuously and smoothly adjustable light source at the University of Toronto. Consequently, the dataset utilized by the application is restricted to categorical data. Even if such a light source existed, insufficient personnel would impede the collection of an adequate number of samples. Alternatively, a softmax activation function could enable continuous mapping by the model.

## Authors

Jingwen (Steven) Shi: Model Building & Training, Data Collection

Desmond Wang: UI Implementation & Testing

Hongsheng Zhong: Idea Provider, Data Collection

Hilda Chen: Project Testing & Debug, Data Collection
