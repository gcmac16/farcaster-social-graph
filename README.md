CLI for downloading the farcaster social graph and rendering it using networkx. 

### Getting Started
To get started make a virtual environment by running:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Next, make an env file called `.env`; in this you'll need to put your farcsater custody account seedphrase in a variable called `FARCASTER_MNEMONIC` like:
```
FARCASTER_MNEMONIC="word1 word2 word3 ...."
```

To test whether everything is working you can run in test mode:
```
python cli.py --test
```

If successful, the message "Passed Healthcheck" should be printed to the console.

### Building the graph
To kick off the program, simply run
```
python cli.py
```

The basic loop of the program is:
1. Iterate over all farcaster ids
2. Get all the users that FID is following
3. Write the data to a file (by default `.farcaster_graph.txt` but you can set this via `--output_file_path` CLI arg)

On subsequent runs, the script will pick up from the last FID you pulled by parsing the output of the file.

### TODO
- write code to build follower graph given the following data we have here
- write code to integrate with networkx

*Inpsired by a Balajis bounty on FC*
