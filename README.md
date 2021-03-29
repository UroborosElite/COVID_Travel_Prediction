# COVID_Travel_Prediction

### Group 7 Final Project for Columbia U Bootcamp

## Team Members

#### Caroline Leon
* Github Repository
* Machine Learning (collaborative effort)
* Database Creation (collaborative effort)

#### Amirah Daniels
* Machine Learning (collaborative effort)
* Database Creation (collaborative effort)

# Topic:
Is the US on track to meet President Biden's projected vaccine rollout to all adults in the US by end of May 2021?

## Why Did We Select This Topic?
We wanted to investigate if our personal interest in being vaccinated against COVID and returning to some form of daily life before COVID, including vacations and social gatherings, would translate to a high number of vaccinated individuals eager to do the same. We are also interested in following developing new surrounding the vaccine and speculating whether governments and companies will begin to require it of patrons or employees.

## What Questions Do You Hope to Answer With The Data?
* If the US is not likely to meet President Biden's anticipated vaccination date for all Americans, when can this be estimated?
* How are neighboring countries fairing in their efforts to vaccinate their populace?

## Data Sources:

[Our World in Data](https://ourworldindata.org/coronavirus "Our World in Data Coronavirus")

Our World in Data monitors data that is relevant to the global community, whether it is COVID statistics, literacy percentages, or a myriad of other information. Our World in Data collates this information making it readily accessible to anyone who may want or need it.

[Open Source Covid Data Updated Daily](https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv "Open Source Covid Data")

This is the GitHub repository where the data collected by Our World in Data lives. Some of these datasets are updated daily, as is with the COVID vaccination dataset.

[CDC was a main source of the data collated by Our World in Data](https://covid.cdc.gov/covid-data-tracker/#vaccinations "CDC COVID Data")

The Centers for Disease Control and Prevention is part of the United States Department of Health and Human Services. It safeguards the US from health and safety threats - both foregin and homegrown.

## Technologies Used
* Python - Flask app
* Jupyter Notebook
* HTML - jinja2 and Javascript

#### Data Cleaning and Analysis
Pandas will be used to clean and explore the data.

#### Database Storage
Postgres is the database we intend to use, integrating Flask as a means to query the data.

#### Machine Learning Model
SciKitLearn is the ML library we will be using to create a classifier. We will be modeling our data using a linear regression model with weighted biases favoring more recent data, using all available vaccination data of all locations worldwide, starting in December 2020.

#### Dashboard
In addition to using a Flask template, we will also integrate D3.js and plotly for a functioning dashboard. It will be hosted on Heroku.

# Analysis and Challenges

## Results, Challenges and Difficulties Encountered

## What are some conclusions you can draw about the outcomes?
* Based on our analysis the United States trajectory is not on trend to have everyone in the US vaccinated by the end of May.
* Based on the data we have compiled and reviewed, we are projecting completion will be October.

## How do we compare to other nations?
* We are doing exponentially better than the European Union and Germany who just initiated another lockdown due to COVID.

* We are underperforming in our vaccine rollout when compared to some of the less populous nations such as Israel.

## What are some limitations of this dataset?

### Differences in General Population:
* Variances in populations of nations may make this data seem biased in favor of smaller, less populous nations. This is due to the fact that less populous nations’ vaccination percentages would rise at a faster rate than densely populated nations.

### Access to Vaccine:
* Some nations have limited access to vaccine supplies for various reasons. An example of this is the European Union now prioritizing its members, meaning UK and by extension Canada will have less access to EU vaccine supply.

### Government Management of Vaccine Distribution:
* Israel has been referred to as executing a successful vaccine rollout. As evidenced in our analysis, the US is not on track to meet its own timetable.

* The differences between these two populations is vast - over 330 Million in USA to Israel’s approximately 9 million. However, a review of Israel’s best practices may prove beneficial to larger nations.

### Vaccine Supply:
* A sudden influx of vaccine supply due to increases in production, another manufacturer gaining emergency approval would skew the current data.

### Choice:
* This data does not factor the political undercurrent of COVID and its vaccine. At this time vaccination is recommended, not required as it is in the USA with MMR (Measles, Mumps, Rubella). But if more businesses, institutions, or even the government start to require the vaccine then this data will experience a positive correlation as a result.

## What are some other possible tables and/or graphs that we could create?

* An analysis of what steps Israel's Ministry of Health - widely regarded a having managed a successful vaccine rollout -  undertook in the management of their vaccine rollout, that could be emulated by a larger nation.
