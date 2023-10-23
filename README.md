# Covid19-Visualisation
#### available @ [https://covid19-visualisation.onrender.com/](https://covid19-visualisation.onrender.com/)

## Background
In December 2019, a number of cases that pointed to a potential respiratory disease were reported in Wuhan, China. The World Health Organisation (WHO) made the first announcement of a novel coronavirus SARS-CoV-2 in January 2020 and 2 months later, a pandemic was declared. The COVID-19 pandemic has had a significant global impact, with more than 535M (+198k) cases and 6.31M (+463) deaths worldwide.

Since then, COVID-19 data has been made available in numerous APIs, for everyone to access and inform themselves. This repository accesses the [Disease.sh](https://github.com/disease-sh/API) open API and provides visualisations for global statistics, along with a guide to interpret them.

## Data Collection 
In short, Disease.sh allows for data collection from multiple sources in a single API. 

For this project, 3 API calls were made:
- Global statistics: [https://disease.sh/v3/covid-19/all](https://disease.sh/v3/covid-19/all)
- Countries (cases,deaths,etc): [https://disease.sh/v3/covid-19/countries](https://disease.sh/v3/covid-19/countries)
- Countries Vaccine Coverage: [https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=1&fullData=false](https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=1&fullData=false)

Plus the data for all states from The Covid Tracking Project:
- States (cases,deaths,etc): [https://covidtracking.com/data/download](https://covidtracking.com/data/download)


## Dashboard Deployment 
The deployment of the dash app is made with [Heroku](http://heroku.com). 

## Running the App Localy
1. Clone the repository.
2. Make sure to create a virtual environment or add into your current environment the libraries in the "requirements.txt".
3. Open a terminal or shell in the /path/to/dash_app/ 
4. Run the following command "python app.py"
5. Open the default local host (http://127.0.0.1:8050/ 895) in your browser
