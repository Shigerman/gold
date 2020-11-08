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
    Python, Requests, Pandas, Matplotlib
```

## How to run the script:

Clone the repository.

Create the virtual environment:

```
    python3 -m venv .venv
```

Activate the virtual environment:

```
    for Windows: .venv\Scripts\activate
```
```
    for Mac or Linux: . .venv/bin/activate
```

Install the dependencies:

```
    pip install -r requirements.txt
```

Run the tests:
```
    pytest test_gold.py
```

Run the script:

```
    python3 gold.py
```

First you will see a line graph of the gold bar price difference.

After closing the graph, the command line will display
the gold bar price difference expressed in roubles and percent.
