# Commentary

## Table of Contents
1. [Logistics](#logistics) (start here!)
2. [About](#about)
2. [Setup Instructions](#instructions)
3. [Interaction](#interaction)
4. [Requirements](#requirements)
4. [Data: Source, Pre-processing, etc.](#data)

## Logistics

*Name:* Danny Vilela

*NetID:* dov205

## About

This project serves as an interactive approach to analyzing Reddit comment data gathered over a two-day period. Despite the seemingly short amount of time, comments across ~30 subreddits generated over half a gigabyte of data. Reddit is home to many, many more subreddits — many of which are much more active than our queried subreddits.

This dataset allows us to understand commentator behavior and analyze the differences (and similarities!) between thematically-distant but behaviorally-similar subreddits.

## Instructions

Building this project is relatively simple. Here's the setup required:

1. After cloning locally, `cd` into the `data` folder. Assuming this project is in the root directory `~`, it'll look like:

		cd ~/final_project/dov205/data

2. You should see many different `.csv` files of the form `comments_*.csv`. Feel free to see my reasoning behind the data processing task [below](#data). These files are essentially split versions of the master comments dataset, so to join them we simply run:

		cat comments_*.csv > comments.csv

You should have a large (~657 MB) dataset that we'll be using for the remaining project. Halfway done!

### Environment

When installing dependencies, I make relatively basic assumptions that the user has [miniconda](http://conda.pydata.org/miniconda.html) – a leaner alternative to Python's *Anaconda* package manager – installed. To make things as smooth as possible, I suggest creating a new conda environment (note, the syntax differences between setting up an environment for `conda` is similar to `pip`). The required commands are as follow:

```bash
# Set up working environment called 'reddit'
conda create --name reddit python=3 jupyter ipython matplotlib pandas numpy

# Activate reddit environment
# Windows: activate reddit
source activate reddit
```

This keeps your (the grader) package management state isolated from this project's and ensures we don't worry about dependency hell :)

**Once you're done grading, feel free to use the following commands to clean up:**

```bash
# Exit conda environment
source deactivate reddit

# Delete conda environment
conda remove --name reddit --all
```

We're done setting things up! What a relief.

## Interaction

The top-level `commentary.py` serves as our program's driver. After my own data analysis and visualization on the Reddit comments dataset, program control state is handed to the user via interactive prompts.

The interactive component is designed to (ideally) be fairly self-explanatory, however, the general idea is that we repeat a loop (until our user has had enough) that cycles through:

1. **Selecting what variables/features our user is interested in exploring/analyzing.** This allows us to isolate the most relevant parts of the problem and, along with reducing the computational overhead of moving data around, can give us insight as to what the user is expecting to explore.

2. **Performing transformations, aggregations, and summarizations on our data.** *TODO*

3. **Visualizing or otherwise communicating to the analysis driver the results of their analysis.** *TODO*

## Requirements

The [final project instructions](https://docs.google.com/document/d/1y-bkl-7pmlv1KN6yaMCInSWyoeINH39ZWzlDjT0cvnU/edit#) list a few requirements for our project that I thought may prove useful to list here, as well as where I fulfilled those requirements:

1. **Loading a non-trivial dataset into pandas objects (DataFrame and Series)** Yes! Please see the [data preprocessing](#data) work I've done, as well as the `load_reddit_data()` data ingestion method in `commentary.py`.

2. **Perform some kind of meaningful analysis of the data using pandas and/or NumPy computational and data analysis tools.** TODO

3. **Display the results of the analysis using matplotlib.** TODO

4. **Allow the user to interactively control the analysis and display of the data.**

5. **The project must include a user guide that describes how to install, configure, and run the program.** Yes! Please see the above [installation instructions](#instructions) which takes care of installation, data and environment configuration, and running the program `commentary.py`.

6. **The final project source code, datasets, and documentation must be uploaded to the final_project repository on GitHub in the same manner as the assignments (fork the repository and send a pull request). The NetID used for the directory should be correspond to one of the students in the team for that project.** Yes! The one by one: 

	- Source code is housed in `commentary.py` and the `Plotter` class directory. 
	- Datasets are under the project's `data` directory. Again, please see the [next section](#data) to learn more about data sourcing, preparation, and processing.
	- Documentation takes the form of this `README` and the inline code comments used to clarify what any particular code block is doing.
	- I'm a team of one, so that takes care of the NetID situation :)

## Data

[Dataset source – Linan Qiu](https://github.com/linanqiu/reddit-dataset)

### Data preprocessing

After cloning Linan Qiu's Reddit dataset source, we have a directory `data` with multiple CSVs. Each CSV corresponds to a category and its specific subreddit (e.g. `gaming_pokemon.csv`, `lifestyle_drunk.csv`, etc.), and each row contains features relating to a top-level thread or thread comment within that subreddit.

When I first attempted to read in the dataset, there was an obvious discrepancy: rows representing comments were in the same files as rows representing thread posts, which made `pandas.read_csv()` upset (and, more importantly, would impact the interpretability of the dataset).

To preserve the most of our original dataset and focus our analysis, I've chosen to only analyze comments, not comments. From the original README, Linan Qiu noted that comment-level posts would have 11 features, whereas thread-level posts (from both the documentation and my exploration of the data) had anywhere between 11 and 13 features.

Our preprocessing goal was two-fold: join all CSVs into a `master` CSV and keep rows whose feature count is 11. With some trial, error, and research into the appropriate command-line tools I came up with the following command to be run from the `data` directory:

```bash
cd ~/path/to/data
cat *.csv > master.csv && awk -F , 'NF==11' < master.csv > comments.csv
```

Broken down: we concatenate all CSV files into a single file `master.csv`. Next, we utilize the command-line tool `awk` to take care of our data preprocessing. In order to isolate comments, we define the regular expression that separates each field (here, a comma `,`) and set our evaluation condition to whether a row has exactly 11 fields. If so, we redirect those rows into `comments.csv`.

This gives us a reasonably clean, large (~657 MB) dataset for analyzing with pandas.

**However**, GitHub has a strict limit on files above 100 MB. To get under/around this limitation, I have to split the files into 80 MB fragments and commit them that way. I do so with the following command:

	split -b 80m comments.csv comments_
	
Decomposed, this command splits `comments.csv` into 80 MB files, prefixed by `comments_`. This gives us a directory with `comments.csv` and `comments_aa`, `comments_ab`, etc. In order to make the filenames a bit nicer, I rename with the following:

	for i in comments_??; do mv "$i" "$i.csv"; done

This gives us `comments_aa.csv`, `comments_ab.csv`, etc. This helps when we want to re-join all the files together with part of our initial processing command:

	cat comments_??.csv > comments.csv
