# Development of A Smart Bicycle
*My Final Year Project*

The Interdepartmental Final Year Project is a collaborative capstone project completed by students from departments of the Faculty of Engineering at Hong Kong Polytechnic University. The project typically includes several faculty areas such as Electrical Engineering and Computing, where students contribute to the project with their own areas of expertise. I had the honor to participate in the *Development of A Smart Bicycle* led by ISE and won the Creative Project Award. 

*Development of A Smart Bicycle* aims to develop a smart bicycle to improve people's riding experience by applying the cutting-edge technologies. In the project, I am responsible for developing the prototype of Cycling Patten Recognition with motion sensors and Machine Learning. Through this project, I have enhanced my interpersonal skills and technical skills in data analytics and the application of ML models in real-time environment.

This repo concludes my method of doing so and it may help others to do research.

## Notes
- All Python files are compatible with Python 2.7
- All Python files are compatible with Python 3.7 except Raspberry-Pi/taillightControl.py because of coding. Therefore, The whole system needs to be ran in Python 2.7
- Raspberry-Pi/requirements.txt is only a recommended installation list.


## Real-time processing pipeline
The real-time processing pipeline reads data from IMU sensor and pedal force sensors. After that, it combines and transforms them into a desired format and then passes it into the loaded models. The models do predictions and control the LED tailight. Finally, the predicted results and processed data are saved into a dataframe. A CSV file containing recorded data will be saved with current date if any exception happens.

## IMU sensor (Inertial Measurement Unit sensor)
...

## LED taillight and Arduino
...

## System diagram
[Picture here]

## File structure

To run the whole system
```bash
python Raspberry-Pi/main.py
```


