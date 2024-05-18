# Gold

![logo](https://github.com/Shigerman/gold/raw/master/gold.jpg)

The script receives the current price of a 10-gram gold bar from the bank site
and compares it to the purchase price in 2018.

The price difference is expressed in roubles and percent
and also with the help of a line graph.

The data for building the graph is taken from the csv file,
where price/date are saved every time the script is run.


***********


## Instruments used:

```
    Python, Requests, Pandas, Matplotlib, Poetry
```

## How to run the script:

Clone the repository.

Install the dependencies:

```
    poetry install
```

If running under WSL, make sure that some kind of X window server is
running, for example VcXsrv with the 'Disable access control' option.

Run the tests:
```
    poetry run pytest
```

Run the script:

```
    poetry run python gold.py
```

The application will output the gold bar price difference (in rubles)
to the terminal. A line graph will be also displayed, if window subsystem
is available.
