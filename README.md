# ED-Brexit-Twitter-posts-analyzer
Project made for Data Minining (Eksploracja Danych) classes

## Tips
In main directory of this project create a file called _credentials_ that should contain the following keys and tokens in order to contact with Twitter API correctly:  
ACCESS_TOKEN=&lt;your consumer API keys: API key&gt;  
ACCESS_SECRET=&lt;your consumer API keys: API secret key&gt;  
CONSUMER_KEY=&lt;your consumer key&gt;  
CONSUMER_SECRET=&lt;your consumer secret&gt;  
It is important to leave last line (5th counting from 1 onwards) of _credentials_ file empty.

Add two additional directories to the main directory of the projects:
* _logs_ where logs from running _update_db.py_ script will be held
* _backup_ where you should keep your *.jsonl files with data. Name of each data *.jsonl file should have format 'tweets_YYYY_MM_DD' -for instance 'tweets_2019_11_12' 