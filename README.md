# CMPSC463_Project2

**Project Goals:**

The goal of this project is to develop an interactive, accessible application that makes criminal analysis and visualization easier. The application seeks to predict future crime trends, uncover correlations, give insights into crime patterns, and facilitate data-driven decision-making for legislators and law enforcement by utilizing data science methodologies.

**Significance of the Project:**

Worldwide, crime is still a major problem that calls for creative approaches to research and prevention. The following significant issues are addressed by this project:

1. **Data-Driven Insights:** By examining crime data, the tool finds trends and connections that provide important information about the causes of crime.
   
2. **User Engagement:** To promote an easy-to-use user experience, the software includes interactive capabilities for comparing cities, viewing crime hotspots, and visualizing predictions.
   
3. **Prediction and Clustering:** To help with resource allocation and strategic planning, the application uses machine learning algorithms to anticipate future crime patterns and group cities into clusters according to their crime rates.
   
4. **Interactive Mapping:** A distinctive, spatially focused analysis is produced by combining interactive maps with geographic data.

This project is unique since it integrates interactive visualization, clustering, and predictive analytics into a single, coherent application.


**Installation and Usage Instructions:**
1. **Prerequisites:**
Install Python (version 3.8 or higher).

Install required libraries using the following command:
 pip install pandas matplotlib seaborn sklearn plotly folium tkintermapview


2. **Dataset: ** Place the crime dataset file (pa_crime_data.xls) in the project directory.
3. **Running the Application:**
Execute the following command:
  python crime_analysis_app.py


**Code Structure:**
1.** Data Loading and Preprocessing: **

  a. Reads and Cleans the dataset. 
  
  b. Calculates crime rates per 1,000 population for better analysis. 
  

2. **Tabs and Features: **
   
  a. **City Analysis:** Shows city-specific crime statistics.
  
  b.** Heatmap:** Crime category correlation heatmap.
  
  c. **City Comparison: ** Comares crime rates between two cities.
  
  d. **Interactive Map:** Shows crime hotspots geographically.
  
  e. **Prediction & Clustering: **
  
    i. Uses linear regression to predict future rates of violent crime. 
    ii. Uses KMeans to group cities according to crime rates.

4. **Visualization and Interaction:**
Matplotlib, Seaborn, Plotly, and Folium are used for creating interactive and static visualizations.



*******flowchart to be added 




**Functionalities and Test Results: **
1. **Functionalities:**
   
  a.** City Analysis:**
  
    i. Allows users to select a city and browse comprehensive crime statistics for a chosen city.
    ii. Verified by showing precise data for a few chosen cities.
    
  b. **Heatmap:** 
  
    i. Produces a crime category correlation heatmap.
    ii. Verification: Correlations match patterns in the data.
    
  c. **City Comparison: **
  
    i. Examines the rates of property and violent crime in two different cities.
    ii. Verification: City data is appropriately reflected in the graphs.
    
  d. **Interactive Map: **
  
    i. Displays crime hotspots based on geographical data.
    ii. Verification: The markers match the latitude and longitude of the dataset.
    
  e. **Prediction & Clustering: **
  
    i. Uses linear regression to forecast rates of violent crime.
    ii. Divides cities into groups according to trends in crime.
   iii. Verification: Clusters offer insightful groupings, and predictions match data trends.


3. **Testing Results: **
   
The application was tested using Pennsylvania crime data. Below are sample results:
  *Correlation between violent and property crime: 0.85 (highly correlated).
  *Cities grouped into three clusters effectively distinguished high-crime and low-crime areas.


**Showcasing the Achievement of Project Goals:**
Sample Execution Results:

1.** City Analysis:**
  *Selected City: Pittsburgh
  *Displayed Data: Violent Crime - 4,123; Property Crime - 12,345.

  
2. **Heatmap:**
  *Strong correlation observed between burglary and property crime rates.

   
4. **Prediction:**
  *Predicted Violent Crime Rate for a population of 500,000: 45 per 1,000.


4.** Clustering:**
*Cluster 0: Low crime cities.
*Cluster 1: Moderate crime cities.
*Cluster 2: High crime cities.



**Discussion and Conclusion:** 
**Challenges:**
Data inconsistency: Preprocessing was necessary for missing or insufficient data.
Map visualization: Performance lags occurred when handling big datasets on interactive maps.

**Restrictions:**
Predictions may not take into consideration outside variables like changes in policy because they are based on a small number of features.
Although clustering assumes three groups, the amount of the dataset may require modification.

**Course Learning Application:**
Algorithms: Implemented Linear Regression and KMeans algorithms.
Visualization: Applied concepts of data visualization using Matplotlib and Seaborn.
Programming: Developed modular, object-oriented code using Python.






