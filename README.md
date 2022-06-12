# Zillow Home Value Estimator - Regression Project

## Project Discription

### Project Goals

### Busines Goals
- Construct an ML Regression model that predict property tax assessed values ('taxvaluedollarcnt') of Single Family Properties using attributes of the properties.

- Find the key drivers of property value for single family properties. Some questions that come to mind are: Why do some properties have a much higher value than others when they are located so close to each other? Why are some properties valued so differently from others when they have nearly the same physical attributes but only differ in location? Is having 1 bathroom worse than having 2 bedrooms?

- Deliver a report that the data science team can read through and replicate, understand what steps were taken, why and what the outcome was.

- Make recommendations on what works or doesn't work in prediction these homes' values.

### Audience
- A group of managers at Zillow
- Data science team collegues 

### Project Deliverables
- Github repo with a complete readme.md, a final report (.ipynb), acquire & prepare Modules (.py) (which are in wrangle.py), other supplemental artifacts created while working on the project (e.g. exploratory/modeling notebook(s))

- A live 5 minute presentation on the notebook Report


### Data Dictionary:

### Initial Hypotheses
- **Hypothesis 1**
- alpha = .05
$H_0$: There is no significant difference in property tax assessed values for different lot sizes
$H_a$: There is a significant difference in property tax assessed values for different lot sizes
Outcome: I rejected the Null Hypothesis; there is a difference in the property tax assessed values for different lot sizes

- **Hypothesis 2**
- alpha = .05
$H_0$: Having 1 bathroom is not worse than having 2 bedrooms
$H_a$: Having 1 bathroom is significantly worse than having 2 bedrooms
Outcome: I rejected the Null Hypothesis; there is a signifcant difference between 1 bathroom and 2 bedrooms

### Executive Summary
- Key Findings
- Recommendations
- Next Steps


## Project Reproduction
[ ] Read the README.md file
[ ] User needs to have their own env.py file with 'user' for username, 'host', and 'password' formated like this (db, user, host, passwor) to access Codeup database 
[ ] Download the wrangle.py file into working directory for acquire and prepare functions 
[ ] Then run final_report jupyter notebook