# Udacity Self-Driving Car Engineer Nanodegree - Behavioral Cloning Project
The objective of this project is to develop a Deep Neural Network which can drive a simulated vehicle in a simlated environment. The simulated environment is built on the Unity engine and consits of a single vehicle in a small world with a single track loop as shown below:

![Simulator Screenshot](/img/simulator_screen.png)

The simulator can be run in two modes, "Training Mode" and "Autonomous Mode". In Training Mode, the vehicle can be driven by the developer and first person images from the vehicle can be captured as well as the steering angle, brake, throttle, and speed of the vehicle. An example image is shown below:

![Image from vehicle](/img/img_from_vehicle.jpg)

In Autonomous Mode, live images can be feed to a trained model which generates a steering angle, which is then fed to the vehicle.

By manually driving the vehicle in Training Mode and using the images from the vehicle as features, with the associated steering angles as labels, I was able to develop a Deep Neural Network to control the steering of the vehicle as it drove around the track.

## Network Architecture

The network architecture that I used was inspired by a paper titled [End to End Learning for Self-Driving Cars](http://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf). In that paper, they present the following figure which depicts the architecture that they used to map images to steering commands:

![Network Architecture](/img/network_architecture.png)

This model consists of data normalization, followed by 3 5x5 convolutional layers, followed by 2 3x3 convolutional layers, followed by 3 fully connected layers, followed by the output layer. The only modification that I made to this architecture was the addition of a 2-Dimensional max-pooling layer after each convolutional layer to further reduce the number of model parameters and help reduce overfitting.

The non-linear mechanisms that are utilized in the model are stacked convolutional layers, ReLU activation, and max-pooling.

## Training Data

To generate training data, first the simulator was run in Training Mode while I drove the vehicle around the track for about 4 laps. However, based on this data alone, the model did not learn how to recover the vehicle if it ever veered off course. To teach the model how to recover the vehicle, I recorded two laps of recovering the vehicle from veering to the right, followed by two laps of recovering the vehicle from veering to the left. After collecting this data, I found that there were many more data points from the vehicle driving down the center of the track compared to recovering from a veering to the left or right. To balance the data, I included two copies of each veering recovery data point.

After training the model using this data, I found that the model was able to drive the vehicle through almost all of the loop. The only place that the model had an issue was the sole right turn on the course. To remedy this, I collected more data of manual driving on that turn as well as recovering from a veering to the left on that turn. Additionally, I included multiple copies of these data points in the training data.

## Fitting the model to the data

To optimize the fit of the model to the data, I used an Adam Optimizer with a mean-squared-error loss metric. 

## Validation and Test

To determine when the optimization was overfitting the model, I used a random selection of the data points as a validation set. Furthermore, after optimizing the fit of the model on the validation set, I ran the simulator in Autonomous Mode to test if the model was able to generate steering angles which would keep the vehicle on the track as it drove around the loop.
