# :bike: green-mapper :metro:

This project optimises transport routes in London. The route can be optimised based on quickest time, shortest distance, or lowest emissions. Python and R versions of the source code are provided (both currently under development).

## Table of Contents
- [Set up](#1-set-up)
- [Launch app](#2-launch)

## 1. Set up

To use this project, please provide a TFL API access key id pair (can be requested [here](https://api-portal.tfl.gov.uk/signup)). These should be in a `.txt` file that looks like below:
```
app_id: <id here>
app_key: <key here>
```

Once you have cloned the repository, to launch the model using python, please install conda (or your preferred alternative) and run the following command in your terminal:
```
conda env create -f environment.yml
conda activate green-mapper
```

## 2. Launch

Once the [`params.yml`](params.yml) file is up to date with credentials file path, url parameters and base map parameters, the application can be launched by simply running [`launch.py`](launch.py) using the following code:
```
python launch.py
```

This should lead to the following output in the terminal:
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'launch'
 * Debug mode: on
```

Just copy and paste the url Dash is running on into a browser of your choice and the app will launch. Once you have put in your desired journey and selected a route, it should look like this:
![An image showing a screengrab of the Green Mapper App. On the LHS are boxes to input a start and end point with a button to get routes and drop down menu to select a route. In the middle is the interactive map with route plotted, and on the RHS are key details about the journey such as simple instructions and total journey time.](img/Screenshot%202024-03-12%20at%2019.29.20.png)