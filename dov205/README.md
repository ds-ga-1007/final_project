## Commentary

### Important notes:

Fork: https://github.com/dataframing/reddit-dataset
Source: https://github.com/linanqiu/reddit-dataset

### Data preprocessing

In directory with all CSV files:

  $ cat *.csv > master.csv && awk -F , 'NF==11' < master.csv > comments.csv

Broken down: we concatenatve all CSV files into a single file "master.csv".
Next, we utilize the command-line tool awk to take care of our data preprocessing.
Our reddit data contains both comments (which are in response to either
another comment or the original post) and original posts. This presents a
problem: comments contain 11 fields, whereas original posts contain 13.
In order to limit the scope of our analysis on strictly comments, we utilize
awk in order to omit particular rows that contain more than 11 instances of our
defined comma delimiter, ','. With master.csv as input, we output the lines
that do not get filtered by awk into 'comments.csv'.
