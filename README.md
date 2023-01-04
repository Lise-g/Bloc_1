# Bloc_1
**Kayak project for certification**

The project aims at collecting some data in order to create an application that will recommend where people should plan their next holidays.
We focus on the top 35 cities to visit in France.

> Video link of the project : 👉  👈

Contact : Lise Gnos  
email : lise.gnos@gmail.com

## First step :  

Get weather data, build a score for each destination and plot a map with the best destinations.  

> Notebook : 'kayak_project/apis.ipynb'  
> Output of the notebook : 'kayak_project/cities_weather_score.csv'

## Second step :  

Scrape hotels' info for each destination from booking.com  
A scrapy project was created in order to do that.

> Scrapy spider : 'kayak_project/projets_scrapy/booking/spiders/booking_spider5.py'  
> Output of the spider : 'kayak_project/projets_scrapy/booking/hotels_complete5.json'

## Third step :  

Gathering all the information and plotting the best hotels for a destination.  

> Notebook : 'kayak_project/hotels.ipynb'

In this notebook I make the join between the 2 files : 'cities_weather_score.csv' and 'hotels_complete5.json'

> Output of the notebook : 'kayak_project/database_kayak_project.csv'

## Fourth step :

Store all the information in a data lake : a bucket was created and the 'database_kayak_project.csv' file was stored in it.

> URL of the csv file : https://bucket-kayak-project.s3.eu-west-3.amazonaws.com/database_kayak_project.csv

## Fifth step :  

Extract, transform and load cleaned data from the datalake to a data warehouse using Amazon RDS.  

> Endpoint of the RDS instance : database-kayak.cmhaagxswhbn.eu-west-3.rds.amazonaws.com

> Notebook that served to put the 'database_kayak_project.csv' file to the database : 'kayak_project/database.ipynb'

pgAdmin was used to connect to the database.


