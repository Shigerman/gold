# Gold

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

Run the tests:
```
    poetry run pytest
```

Run the script:

```
    poetry run python gold.py
```

First the command line will display
the gold bar price difference expressed in roubles and percent.

Then you will see a line graph of the gold bar price difference.
