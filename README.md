# CaliCast
This project is a weather data dashboard that integrates real-time, historical weather data and a machine learning model for weather predictions with a cloud database. The goal is to enhance our software engineering skills by working with Shiny for Python, data visualization, and cloud database management.

The dashboard provides visual insights into various weather parameters across multiple Californian cities. Users can interact with different graphs to explore temperature trends, wind speed and direction, humidity levels, and cloud cover.


## Cloud Database
Database Used:
The project utilizes Google Cloud Firestore for storing and retrieving weather data. Firestore is a NoSQL cloud database that supports real-time updates and seamless integration with web applications.

## Cloud Database

### Database Used

The project utilizes Google Cloud Firestore for storing and retrieving weather data. Firestore is a NoSQL cloud database that supports real-time updates and seamless integration with web applications.

Database Structure:
* historical_weather_data
* location_id
* current_weather_data
## Development Environment
Tools Used:
* Google Cloud Firestore (for database)
* Shiny for Python (for building the web app)
* GitHub Actions (for automating data updates)
* VS Code (for development)
* Python 3.x

## Programming Language & Libraries:
* Python
* shiny (web app framework)
* pandas (data manipulation)
* plotnine (ggplot-style visualization)
* matplotlib (additional plotting)
* numpy (numerical computations)
* google.cloud.firestore (database integration)
* XGBoostRegressor (future 12h weather predictions)

## Useful Websites
* Shiny for Python Documentation
* Google Cloud Firestore Docs
* Plotnine Documentation
* Matplotlib Documentation
* NOAA Weather API

## Future Work
* Improve UI/UX: Enhance the design with better color schemes and animations.
* More Graphs: Add visualizations for precipitation, UV index, and air quality.
* Additional ML models to predict more long term weather patterns.
