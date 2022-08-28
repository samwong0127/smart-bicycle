# Development of A Smart Bicycle
*My Final Year Project*

The Interdepartmental Final Year Project is a collaborative capstone project completed by students from departments of the Faculty of Engineering at Hong Kong Polytechnic University. The project typically includes several faculty areas such as Electrical Engineering and Computing, where students contribute to the project with their own areas of expertise. I had the honor to participate in the *Development of A Smart Bicycle* led by ISE and won the Creative Project Award. 

*Development of A Smart Bicycle* aims to develop a smart bicycle to improve people's riding experience by applying the cutting-edge technologies. The smart bicycle can enhance user experience by providing posture suggestion and tail light automation for traffic safety. Our smart bicycles are targeted at citizens, so the ideal outcome is that users can review their trip with a smartphone app where all suggestions, records, etc. are saved instead of the bicycle. In the project, I am responsible for developing the prototype of Cycling Patten Recognition with motion sensors and Machine Learning. Through this project, I have enhanced my interpersonal skills and technical skills in data analytics and the application of ML models in real life. Finally, a branch of Cycling Pattern Recognition: Turning Tendency Prediction model (which predicts future turning tendency) is developed and implemented on bicycles. 

This repo concludes my method of doing so and it may help others to do research.

## Notes
- All Python files are compatible with Python 2.7
- All Python files are compatible with Python 3.7 except Raspberry-Pi/taillightControl.py because of coding. Therefore, The whole system needs to be ran in Python 2.7
- Raspberry-Pi/requirements.txt is only a recommended installation list.


## Real-time processing pipeline
The real-time processing pipeline reads data from IMU sensor and pedal force sensors. After that, it combines and transforms them into a desired format and then passes it into the loaded models. The models do predictions and control the LED tailight. Finally, the predicted results and processed data are saved into a dataframe. A CSV file containing recorded data will be saved with current date if any exception happens.

## IMU sensor (Inertial Measurement Unit sensor)
...

## LED tail light and Arduino
LED tail light is an important feature in my part of the project. Turning Tendency Prediction can predict turning tendency with trained model with 98.7% accuracy. The prediction results (0 and 1) should be visualized for pedestrians and other riders.
...

## Raspberry Pi
...

## System diagram
[Picture here]

## File structure

To run the whole system
```bash
python Raspberry-Pi/main.py
```


