# RushHour

Written and tested with python 2.7

## Running

the main script to run is located in src/main/python/RushHour.py. The solver can be started from your console:

```
python src/main/python/RushHour.py
```

## File format

A level file exists of a variable number of rows and columns. Each row does need to have the same number of characters.
an empty space is marked with a lowercase `_`. a car is marked with a letter of choice, as long as each car has a unique
letter. The letter of the starting car is fixed, it is the letter `R`. The finish of the level can be added by a pound sign `#` at the end of a row. The starting car needs to be on
the same row as the finish.

Sample level files can be found in src/resources/level*

