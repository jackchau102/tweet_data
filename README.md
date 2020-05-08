![Twitter data generated so far using Kepler.gl](/usatwitter.png)

<h1>How to set up and run the scraper from your local machine</h1>

<h2>Setting up an anaconda environment</h2>

1. Install anaconda using the following link: "https://docs.anaconda.com/anaconda/install/"

2. Create an environment from the .yml file (note: this is only applicable for Mac OS). If you are using a different OS, manually install the dependencies needed for the python script

```conda env create --file twitter_env.yml```

3. Activate the environment

```source activate twitter_env```

<h2>Running the bash script</h2>

The bash script runs and logs error to an error.txt file. This is to help with debugging when needed.

To run the bash script, follow these steps: 

1. Grant permission for machine to read and execute the bash script. In the local directory terminal: 

```chmod r+x call_and_log```

2. Run the bash script

```./call_and_log```

<h2> A few notes on the CSV file produced </h2>

1. The output does not include column names. The column names are in the following order:

<ul>
    <li>User ID</li>
    <li>User tweet</li>
    <li>Tweet creation time</li>
    <li>Latitude</li>
    <li>Longitude</li>
</ul>

2. Currently, it is best to set up the scraper on a virtual machine to save space on your local machine. To do this, create a VM and clone the files onto that machine.

3. To keep the script running, consider using nohup

```
nohup ./call_and_log //run the bash script in the background
cat nohup.out //print out to shell console the result of the bash script
``` 

4. nohup will keep the script running on your VM even after you exit