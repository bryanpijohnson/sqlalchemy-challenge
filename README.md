# Bryan Johnson's GWU Module 10 SQLAlchemy Assignment READ ME File

## The files for this assignment can be found at the following repo:
https://github.com/bryanpijohnson/sqlalchemy-challenge

## Within the repo link, you will find the following folders and files to be reviewed and graded:

- **README.md** - that is this file. :)
- **SurfsUp** - this is the folder where the following files/folders live
    - **Resources** - this folder holds the sqlite and CSV files to create the database in Python
    - **app.py** - this is the Python file where the Climate App can be found
    - **climate_starter.ipynb** - this is the Jupyter Notebook file where the initial station and measurement analysis is done

# ANALYSIS

## Climate Analysis

After importing the correct libraries, building the engine to the database, and reflecting/creating the classes for the tables, I was able to find the *most_recent_date* in the measurement data, then used the datetime module to find the date one year prior.

I then used both of those dates to filter the measurement data and turn that into a DataFrame. Plotting it gave the plot shown below:

![Daily Precipitation Over the last Year of Data Collection](SurfsUp/Images/precipitation.png)


## Station Analysis

After finding out that there are exactly 9 stations in the data set (both in the stations table and in the measurements table), I wrote a query to find the most active station, by counting the number of times each station had in the measurements table. That station is USC00519281.

I then found all of the temperature data for that station in the most recent complete year, turned that result into a pandas DataFrame, and then plotted the frequencies of the temperatures in the histogram below:

![Temperature Frequency for Most Active Station Over the Last Year of Data Collection](SurfsUp/Images/temp_freq.png)

# CLIMATE APP

After importing the dependencies and setting up the database, I set up a section of code that I knew would be reused a few times for multiple routes, so I set them ahead of the routing portion.

Then I worked on the Static Routes, which was very straightforward. While working on the dynamic routes, I realized that my code for the "*../start*" and "*../start/end*" routes were very similar. I looked into to see if it was possible to combine routes and saw that it was. I then started working on combining the code so they would work on the same lines of code.

One of the things I really enjoy is UI/UX work. In this example, I knew that I wanted the user to get a valuable error on a few occasions. Here are those occasions:
- **When the start date occurred after the end date** - Since the code is very specific in how it filters, the start date should always come before the end date
- **When the start date occurs after the last date in the dataset or when the end date occurs before the first date in the dataset** - The user doesn't know *a priori* what dates are available to search for. Therefore, a helpful error should be shown when this happens.
- **When the start date or end date aren't even dates** - I added a portion at the beginning of this route to check to make sure that they were actually dates in the ISO format and to show an error if they weren't.

## Static Routes

There following references (within the app) are as follows:
- **/api/v1.0/precipitation** -- the date and amount of precipitation each day for the last year of collection
- **/api/v1.0/stations** -- the list of all the stations, by code and name
- **/api/v1.0/tobs** -- the list of temperature readings for the most active station (USC00519281) in the last year of data collection

## Dynamic Routes
- **/api/v1.0/start** -- replace 'start' with a date (YYYY-MM-DD) to see the minimum, maximum, and average temperature after that start date.
- **/api/v1.0/start/end** -- replace 'start' and 'end' with dates (YYYY-MM-DD) to see the minimum, maximum, and average temperature between those dates, inclusive

## Secret Route
- **/api/v1.0/secret** -- if you dare

---
If you have any questions, please feel free to contact me.