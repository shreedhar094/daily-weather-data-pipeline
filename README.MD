
DAILY WEATHER DATA PIPELINE

A Python-based data pipeline that collects current weather information for Bengaluru, Mumbai, and Delhi using WeatherAPI and stores it in a SQLite database. It includes duplicate prevention, request retries, error logging, and scheduled execution using Windows Task Scheduler.

PROJECT OVERVIEW

The pipeline performs the following steps.

1. Fetches current weather data from WeatherAPI.
2. Extracts observation time, temperature, humidity, feels-like temperature, and wind speed.
3. Stores weather data in a SQLite database.
4. Prevents duplicate records using a unique index on city and observation time.
5. Logs successful operations, skipped duplicates, and failures.
6. Is configured to run daily through Windows Task Scheduler.

TECHNOLOGIES USED

- Python
- WeatherAPI
- Requests
- SQLite
- Python Logging
- Windows Task Scheduler
- Git and GitHub

PROJECT STRUCTURE

daily_weather_pipeline
    main.py
    check_data.py
    requirements.txt
    .gitignore
    README.md

The weather.db database and pipeline.log file are generated when the pipeline runs. They are excluded from Git through .gitignore.

DATA COLLECTED

For each city, the pipeline stores:

- City
- Observation time
- Temperature in Celsius
- Relative humidity
- Feels-like temperature in Celsius
- Wind speed in kilometres per hour

SETUP AND INSTALLATION

Step 1: Clone the repository

Replace the URL with your GitHub repository URL.

    git clone YOUR_GITHUB_REPOSITORY_URL
    cd daily_weather_pipeline

Step 2: Create and activate a virtual environment

    python -m venv venv
    venv\Scripts\Activate.ps1

If PowerShell blocks script execution, run:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Then activate the environment again.

Step 3: Install dependencies

    pip install -r requirements.txt

Step 4: Configure the WeatherAPI key

Create an API key at https://www.weatherapi.com/

Set it as an environment variable in PowerShell:

    $env:WEATHER_API_KEY = "YOUR_API_KEY"

The application reads the key from the WEATHER_API_KEY environment variable. Never upload your API key to GitHub or hardcode it in the source code.

Step 5: Run the pipeline

    python main.py

The pipeline fetches current weather data for Bengaluru, Mumbai, and Delhi and stores new observations in weather.db.

Step 6: View stored records

    python check_data.py

This displays the records stored in the SQLite database.

DATABASE AND DUPLICATE PREVENTION

The pipeline stores records in a SQLite table named weather.

A unique index is created on the combination of city and time. Data is inserted using SQLite INSERT OR IGNORE.

If a record with the same city and observation time already exists, the database ignores the duplicate instead of inserting it again.

ERROR HANDLING AND LOGGING

The pipeline includes:

1. Up to three attempts for failed WeatherAPI requests.
2. A request timeout.
3. Error handling for API and database operations.
4. Execution logging in pipeline.log.
5. A summary of successfully processed cities and failed cities.

To view the latest log entries, run:

    Get-Content pipeline.log -Tail 15

SCHEDULED EXECUTION

The pipeline is configured in Windows Task Scheduler to run daily at 10:38 PM.

The task runs main.py using the project's Python interpreter and project directory.

One automatic scheduled execution was successfully tested. Further daily executions have not yet been verified.

The computer must be on and awake at the scheduled time. With the current Task Scheduler setting, the Windows user must also be logged in.

The pipeline can also be run manually at any time using:

    python main.py

KEY LEARNING OUTCOMES

1. Calling REST APIs using Python.
2. Extracting and handling JSON response data.
3. Storing structured data in a relational database.
4. Preventing duplicate records using database constraints.
5. Handling API failures with retry logic.
6. Logging pipeline execution and errors.
7. Scheduling a Python script using Windows Task Scheduler.

FUTURE IMPROVEMENTS

1. Migrate from SQLite to PostgreSQL.
2. Use Apache Airflow for workflow orchestration.
3. Add automated data-quality checks.
4. Add notifications for failed pipeline runs.
5. Deploy the pipeline to a cloud environment.

AUTHOR

Shreedhar Ganiger

B.Tech, Computer Science and Engineering, Data Analytics