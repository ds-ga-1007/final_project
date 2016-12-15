# nn-python
Neural Network implementation in Python

### Background

There are three main mathematical computations utilized in this package that the models are built on.

Imputation is the process of replacing missing values in a dataset.
Mean imputation replaces the missing values within a feature with the arithmetic mean of the existing values.
Median imputation replaces the missing values within a feature with the median of the existing values.
For a more detailed description of imputation, see https://en.wikipedia.org/wiki/Imputation_(statistics)

Neural Networks are a mathematical representation of a computation graph.
There are many different optional structures, training algorithms, and other options available within this package
accessible through NeuralNetworkLearner.
For a more detailed description of Neural Network models and training algorithms,
see https://en.wikipedia.org/wiki/Artificial_neural_network

An Autoencoder is an application of a Neural Network to perform dimensionality reduction that can preserve
large amounts of the true underlying variations within a dataset with a very small encoding dimension.
Compared to linear dimensionality reduction algorithms like PCA, autoencoders can represent many dimensions
of variation within a low number of encoded dimensions, such as maintaining upwards of 99% data variation
from a high dimensional dataset in as little as 2 or 3 dimensions due to the non-linearity of a Neural Network.
A brief summary of an autoencoder is a neural network that has a narrow hidden layer, and with inputs and outputs
both equal to the dataset features to be autoencoded.
For a more detailed description of autoencoders, see https://en.wikipedia.org/wiki/Autoencoder


### System and Dependencies

Only tested on Linux.  Windows and OS/X are not supported.

Requires Python 3, and the following packages to work:

* numpy
* pandas
* tabview
* matplotlib

NOTE: this code will **not** work on Python 2.

### Usage for `demo.py`

`demo.py` is an interactive interface in console for mining the latent features in a dataset, and visualizing them in 2D or 3D.

#### Sample walkthrough

One can run the script by following the steps below:

1. Execute the script:

    ```
    $ python demo.py
    ```
    
    The script prompt is pretty self-descriptive.  However we still provide an end-to-end walkthrough for visualizing the abalone dataset.
    
2. You will see a prompt for the path to the dataset, which **MUST** be a CSV file.  After entering the path to the dataset (`dataset/abalone.data` in our case), it will request the separator character (comma in our case, and you can safely leave it blank), whether or not there is a header in the first line (`'N'` in our case), and which column the target variable is in (type -1 for the rightmost column).  The session should look as follows before actual preprocessing of the feature set and the label set:

    ```
    Enter the filename you want to load the dataset from:
    dataset/abalone.data
    Enter the separator for the CSV file [default ","]:

    Is there a header in the first line? [Y/N]
    n
    Column names not available in header.
    Please specify the indices for target column separated by comma.
    Negative indices indicate columns starting from the right.
    Enter a blank line to indicate that there is no target variable.
    -1
    ```
    
3. It will present a menu, on which you can specify various transformations and build a pipeline of transformations, preview the result of the pipeline, etc.  In abalone dataset, you may wish to normalize the numeric columns to values between -1 and 1, then dummy out the categorical values in the first column.

  NOTE: the order of the menu will change between execution.

  For normalizing all numeric columns, type `n` to enter the normalization step, then choose `-` to normalize the values into somewhere between -1 and 1, and select `a` to apply this for all numeric columns.  The session should probably look like this:

    ```
    Preprocessing feature set
    Data preprocessing:
    i - impute missing values in numeric columns
    p - preview result
    x - quit and terminate
    a - add null indicator variables
    n - normalize columns
    u - undo last transformation
    d - delete values
    1 - dummy out (one-hot encode) categorical variables
    v - view pipeline
    q - quit and proceed to next step
    s - view/edit schema
    n
    Choose the normalization method:
    1 - linearly normalizing to 0..1
    n - subtracting the mean and dividing by standard deviation
    0 - subtracting the mean
    - - linearly normalizing to -1..1
    -
    a - all numeric columns
    s - only some of the columns
    a
    ```
    
  For one-hot encoding the categorical columns, just type `1` in the `Data preprocessing` menu.

    ```
    Data preprocessing:
    i - impute missing values in numeric columns
    p - preview result
    x - quit and terminate
    a - add null indicator variables
    n - normalize columns
    u - undo last transformation
    d - delete values
    1 - dummy out (one-hot encode) categorical variables
    v - view pipeline
    q - quit and proceed to next step
    s - view/edit schema
    1
    Dummying out every categorical variables (null values are encoded as all zeroes)
    ```

  Select `v` in the data preprocessing menu to view current pipeline of transformations, whose operations would be sequentially applied to the dataset:

    ```
    Data preprocessing:
    i - impute missing values in numeric columns
    p - preview result
    x - quit and terminate
    a - add null indicator variables
    n - normalize columns
    u - undo last transformation
    d - delete values
    1 - dummy out (one-hot encode) categorical variables
    v - view pipeline
    q - quit and proceed to next step
    s - view/edit schema
    v
    Current pipeline:
    Normalize by linearly normalizing to -1..1 for all columns
    Dummy out categorical values
    ```
    
  Select `p` to preview the result of transformation in an interactive interface.  The program would show a table and you can navigate in the cells.

  When done, enter `q` to commit the changes and proceed to transform the label set.
  
    ```
    Data preprocessing:
    i - impute missing values in numeric columns
    p - preview result
    x - quit and terminate
    a - add null indicator variables
    n - normalize columns
    u - undo last transformation
    d - delete values
    1 - dummy out (one-hot encode) categorical variables
    v - view pipeline
    q - quit and proceed to next step
    s - view/edit schema
    q
    ```
  
  In our case we do not need to transform the label set, so we directly choose q:
  
    ```
    Preprocessing label set
    Data preprocessing:
    i - impute missing values in numeric columns
    p - preview result
    x - quit and terminate
    a - add null indicator variables
    n - normalize columns
    u - undo last transformation
    d - delete values
    1 - dummy out (one-hot encode) categorical variables
    v - view pipeline
    q - quit and proceed to next step
    s - view/edit schema
    q
    Visualizing the dataset on 2D and 3D spaces...
    ```
    
4. After the autoencoding finishes, the program shows a window containing the visualization and projection of the dataset in 2D and 3D graphs, then terminates.  Usually, you are able to observe a perfectly straight line.

#### Documentation

`demo.py` only supports reading, preprocessing, and visualizing datasets in CSV format.

##### Startup

Upon execution it will request a path to the dataset, the separator character, whether it contains the list of column names on the first line, and whether there are any target variables.

###### Target variable specification

Target variable columns can be specified by indices.  If the indices are negative, say `-n`, then it represents the rightmost n-th column.

Target variable columns can also be specified by names, but only if the column names are available in the CSV file.  If they don't have a name, `demo.py` will assign the n-th column with the default name `col<n-1>`.  For instance, the first column would be given the name `col0`.  You can change the name later in data preprocessing step, but it won't have any effect on visualization results.

If there is no target variable, you will only need to preprocess one dataset.  Otherwise, you will have to preprocess two datasets: a *feature* set and a *label* set.  Data preprocessing is done interactively by a menu.

##### Main menu

The main menu provides the following functionalities:

* `p`: Preview the result of preprocessing.  An interactive table will be shown and you can check the result with it.
* `v`: View the current pipeline of transformations.  Data preprocessing is done by applying transformations sequentially in the pipeline.
* `u`: Undo last transformation, in case of you made something wrong.  You can undo as many steps as you want until the pipeline becomes empty.
* `s`: View or edit schema.  A *schema* describes whether each column is categorical or numeric.  By default, `demo.py` treats any columns with non-numeric values (such as "?", "A", etc.) categorical, and numeric otherwise.  Selecting this option gives you a series of sub-options:
  * `c`: Rename columns.
  * `g`: Guess schema.  If you select this option, the program would check each column whether a majority of the values there are numeric: if so, then sets the column type to be numeric, deleting any non-numeric values in the process.  This is useful when a small portion of the column is populated by "unknown identifiers" such as "?", "-", etc.
  * `s`: Display current schema.  Make sure you check the schema before visualization, as the default schema and/or schema guessing would not always do what you exactly want.
  * `d`: Drop columns.
  * `m`: Change column type to either numeric or categorical by your own.
* `d`: Delete values.  You can delete the following values for either all the columns, or some of the columns (and you'll have to specify the name of those columns by your own):
  * `n`: All negative values.  Useful in datasets where negative values make no sense or indicates unknownness.
  * `0`: All zeroes.
  * `x`: All values equal to some value.  You will be asked what value it is, and whether it is numeric or categorical.
  * `?`: All question marks ("?"), dashes ("-"), whitespaces, and "N/A" or "NA" in uppercase or lowercase.  This should cover most cases of unknown value indication.  Though for numeric values, it is often more straightforward to simply force that column to be numeric (by editing the schema and changing the column type).
* `a`: Add null indicator variables.  You will be asked whether a null indicator variable should be added for each numeric column, or each of the columns you specified.  A new column would be added for each column with null values, with 1 showing that the corresponding value is missing, or 0 otherwise.  Usually categorical columns does not need null indicator variables.
* `n`: Normalize columns.  You will be asked whether you want to normalize all numeric columns, or you want to specify some of the columns for normalization.  It gives you four options for normalization:
  * `0`: Shift the mean to 0.
  * `n`: Shift the mean to 0 and rescale the values to make the variance 1.
  * `1`: Linearly normalize all values to those between 0 and 1.
  * `-`: As above, but to those between -1 and 1.
* `1` (not the lowercase `l`): Dummy out each categorical variable into n indicator variables, where n is the number of different values in that column.  The program will automatically apply this transformation to all categorical columns.
* `i`: Impute the empty values.  You can choose to impute all the columns or some of the columns (whose names should be specified) by
  * `0`: all zeros
  * `m`: the median of each column
  * `a`: the average of each column
* `q`: Quit and proceed with this pipeline.  Upon selection, you should have transformed every categorical value to numeric, and there should not be any missing values, otherwise the program would ask you to deal with them by either dummy out the categorical values, or impute the null values.
* `x`: Quit and say goodbye.

##### Visualization

After preprocessing the dataset, or feature set and label set, the program will autoencode the data, and visualize every data point by their latent 2D and 3D representations in a 2D and 3D plot.  Usually you can find something interesting.

### Writing code within this framework

Please consult `User_Guide_Code.ipynb` for details and demonstration.

### Acknowledgements

The abalone dataset, arrhythmia dataset, and IRIS dataset comes from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml).

The MNIST dataset is publicly available in [LISA-lab](http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz) in Pickle format.  We wrapped it up in an HDF5 file.
