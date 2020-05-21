# Bikeshare project for Udacity's Programming for Data Science with Python
Created on May 21, 2020

## What's this repository about?
The purpose is to showcase the final Python project of this Nanodegree that focuses mostly on Pythons's libraries that are frequently used in the data science domain (here it's especially Pandas).

Except Pandas I also used the Streamlit framework for data visualization https://www.streamlit.io/. With it I was able to put together a basic Python app with charts and filtering based on select boxes - from the UX standpoint I liked it much more than just having the user to interact with the shell environment 😉

## So we can look at some charts? That's exciting!
Yep, I can feel your excitement. The app was built to visualize data provided by the US bike sharing provider Motivate https://www.motivateco.com. It was tested using a small subset of data for three cities: Chicago, New York and Washington.

The dataset contained these columns:

Start Time, End Time, Trip Duration (in seconds), Start Station, End Station, User Type, Gender (only for Chicago and New York), Birth Year (only for Chicago and New York)

As you can see there's plenty of information to look into 😎 So let's dive in!

## Awesome, can't wait. But how can I run this stuff?
No worries, it's pretty easy. You just have to install the Python libraries that are the dependencies for this project - you can see them at the top of `bikeshare.py`. After you'll have them installed in your Python environment, just run `streamlit run bikeshare.py` and you should be good to go!

## Inspiration aka resources
I had to read a bunch of articles, go through documentation and sometimes wander into coding oriented forums to put this all together since I never worked with Streamlit before (with Pandas too, and Python in general). These are the resources that helped the most:

Streamlit docs
https://docs.streamlit.io/en/latest/api.html

Cool guide into Streamlit with examples
https://analyticsindiamag.com/a-beginners-guide-to-streamlit-convert-python-code-into-an-app/

Another cool article about Streamlit (with examples)
https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83

Plotly knows charts (I used the Pie)
https://plotly.com/python/pie-charts/

Filtering a Pandas DataFrame (very handy)
https://www.listendata.com/2019/07/how-to-filter-pandas-dataframe.html