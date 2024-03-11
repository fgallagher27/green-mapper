# :bike: green-mapper :metro:

This project optimises transport routes in London. The route can be optimised based on quickest time, shortest distance, or lowest emissions. Python and R versions of the source code are provided (both currently under development).

## Table of Contents
- [Set up](#1-set-up)
    - [Python](#python-set-up)
    - [R](#r-set-up)
    - [Building the London transport system map](#building-the-london-transport-system-map)

## 1. Set up

To use this project, please provide a TFL API access key id pair (can be requested [here](https://api-portal.tfl.gov.uk/signup)). These should be in a `.txt` file that looks like below:
```
app_id: <id here>
app_key: <key here>
```

### Python set up
To python source code is in the [Python](Python) folder. Once you have cloned the repository, to launch the model using python, please install conda (or your preferred alternative) and run the following command in your terminal:
```
conda env create -f environment.yml
conda activate green-mapper
```


### R set up

TBC

### Building the London transport system map

A map of the london transport system map is built as part of this project. This is a one time exercise that is computationally expensive. Detailed instructions can be found in [`map_data.yml`](map_data.yml).