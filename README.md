# Beat-the-crowd-umass-model
Scripts for collection ML data and building model
Description as a Tweet:
We've developed a mobile application that leverages machine learning to predict dining common busy-ness and identify student dining habits, for use by students and UMass Dining in minimizing crowds and food waste.

Inspiration:
USDA’s Economic Research Service estimates food waste to be between 30-40 percent of the food supply. By providing our award winning dining program with the ability to identify consumer trends and predict busy-ness, we can begin to reduce excess food waste while saving on costs. For students, the application interface allows users to plan around potential surges in crowds and avoid long lines.

What it does:
Our project consists of a React Native application that interfaces with a Prophet forecasting procedure deployed on a Flask server hosted by Digital Ocean. Users select a dining common in the mobile interface and see the current busy-ness level as well as the forecasted level over the next 24 hours. A Jupyter notebook housing the model implementation allows for more fine-tuned data analysis with trend identification and historical graphs.

How we built it:
As with any AI/ML project, we needed data. Lots of data. Earlier this month, we reverse engineered the official UMass Dining mobile app by intercepting encrypted API traffic using a Man-in-the-Middle HTTPS proxy (mitmproxy). Upon discovering the correct API endpoint, we wrote a script to record the busy-ness level for each dining location every ten minutes into a Postgres database in preparation for the Hackathon.

When the hacking began, we proceeded to train Facebook's open source forecasting procedure called Prophet on the time series data using a Juptyer notebook. We then deployed the trained model on a Flask server. While building the model, we also engineered a React Native app to consume the predictions in a user friendly interface.

Technologies we used:
Javascript
React
SQL
Python
Flask
AI/Machine Learning

Challenges we ran into:
Acquiring the data was fairly tricky. UMass Dining does not provide a documented API for busy-ness levels, leading us to use an HTTPS proxy on the mobile app. Additionally, eduroam prevented us from hosting a proxy on the same network, necessitating a mobile hotspot instead.
None of us had significant prior data science experience going into this project, making simple operations a perpetual journey into documentation and StackOverflow. In addition, we struggled to effectively calibrate the model on different parameters such as performance metrics, weather regressors, holidays, and seasonality.

We encountered a few difficulties in deploying our model on a server. Managing Python dependencies without virtual environments or even a requirements.txt slowed us down considerably, featuring a mind-boggling bug where a dependency's C++ compilation quietly failed due to the server not having enough memory.
Lastly, dealing with time zones, formats, and dates in general was a major headache.

Accomplishments we're proud of:
We are proud of successfully implementing a machine learning model without prior data science experience. In addition, we are pleased with our ability to teach, learn, and debug effectively as team. Lastly, we are excited to work on a project with potential impact on sustainability, campus convenience, and the Princeton Review ranked No. 1 Best Campus Food program!

What we've learned:
- It's possible to discover and intercept mobile API endpoints using an HTTPS proxy
- Today's tooling makes it easy to get up and running with a machine learning model. Understanding and calibrating the model is where data science knowledge and experience is truly required.
- Abstractions and tools generally make developers' lives easier but can be difficult to approach and tend to be harder to troubleshoot when things go wrong.

What's next:
We're interested to see how our model improves as more training data accumulates over time. In addition, we would like to engineer a more robust ML pipeline with features such as distributed computation, automatic deployment, real-time data streaming, quality control, and monitoring. With more time and knowledge, we would have liked to explore industry standard technologies such as Kubernetes and cloud functions that help alleviate some of the challenges we encountered.
Currently, we are missing the infrastructure to deploy our React Native application. Also, we were unable to implement a few desired UI elements and features.

Built with:
- Editors: Visual Studio Code, Sublime Text, Jupyter Notebooks
- Languages: Python, JavaScript, PostgreSQL
- Frameworks: React Native & Expo, Prophet
