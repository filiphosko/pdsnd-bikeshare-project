import streamlit as st
import time
import pandas as pd
import altair as alt
import plotly.express as px
from constants import *


def main():
    st.title("Bikeshare dataset: insights")
    st.markdown("Hope you'll enjoy going through all these visualizations 😎")

    # Filter for cities
    cities = list(CITY_DATA.keys())

    city = st.selectbox(
        label="Choose your city", options=cities, format_func=format_label
    )

    # Load the CSV data and create additional columns
    df = prepare_data(city)

    # Create visualizations for 'general overview' stats
    st.markdown("### Raw data for {} bike trips".format(city.title()))
    number_of_rows = st.number_input(
        label="Please select the number of rows you'd like to see",
        min_value=5,
        max_value=len(df.index),
        value=5,
        step=5,
    )
    st.write(df.iloc[0:number_of_rows])

    missing_values = df.isnull().sum().where(lambda x: x > 0).dropna()

    if not missing_values.empty:
        st.write(
            "### Missing values per column",
            missing_values.sort_values(ascending=False).rename(
                "Number of missing values"
            ),
        )

    # Visualize data about trips before month/day filters are applied
    trip_duration_per_month = df[["Trip Duration", "Month"]].groupby("Month").sum()

    trip_duration_per_month_df = trip_duration_per_month.reset_index()

    trip_duration_per_month_df["Trip Duration"] = pd.Series(
        map(
            lambda x: round(x / (3600 * 24), 2),
            trip_duration_per_month_df["Trip Duration"],
        )
    )

    st.markdown("### Total monthly trip duration")

    trip_duration_per_month_chart = (
        alt.Chart(trip_duration_per_month_df)
        .mark_bar()
        .encode(
            x=alt.X("Month:O", title="Month number"),
            y=alt.Y("Trip Duration:Q", title="Trip Duration (days)"),
        )
    )

    st.altair_chart(trip_duration_per_month_chart, use_container_width=True)

    if "Generation" in df.columns:
        trip_duration_per_generation = (
            df[["Trip Duration", "Generation"]].groupby("Generation").sum()
        )

        trip_duration_per_generation_df = trip_duration_per_generation.reset_index()

        st.markdown("### Total trip duration per generation")

        trip_duration_per_generation_chart = px.pie(
            trip_duration_per_generation_df, values="Trip Duration", names="Generation"
        )

        st.plotly_chart(trip_duration_per_generation_chart, use_container_width=True)

        trip_count_per_generation = df["Generation"].value_counts()
        trip_count_per_generation_df = trip_count_per_generation.reset_index()

        st.markdown("### Number of trips per generation")

        trip_count_per_generation_chart = (
            alt.Chart(
                trip_count_per_generation_df.rename(
                    columns={"index": "Generation", "Generation": "Number of trips"}
                )
            )
            .mark_bar()
            .encode(x=alt.X("Generation:O", sort="y"), y=alt.Y("Number of trips:Q"),)
        )

        st.altair_chart(trip_count_per_generation_chart, use_container_width=True)

    # Create and apply month/day filters
    st.markdown("## Month/day filters")

    months = st.multiselect(
        label="Choose a month (if left unselected, it will get all months)",
        options=MONTHS,
        default=MONTHS,
        format_func=format_label,
    )

    days = st.multiselect(
        label="Choose a day (if left unselected, it will get all days)",
        options=DAYS,
        default=DAYS,
        format_func=format_label,
    )

    # Filter by month if applicable
    if months and len(months) != len(MONTHS):
        month_numbers = map(lambda x: MONTHS.index(x) + 1, months)

        df = df[df["Month"].isin(month_numbers)]

    # Filter by day of week if applicable
    if days and len(days) != len(DAYS):
        day_numbers = map(lambda x: DAYS.index(x) + 1, days)

        df = df[df["Day of Week"].isin(day_numbers)]

    # Most common dates and times
    st.markdown("### Most frequent times of travel")

    # Most common month
    st.markdown(
        "* The most common month is: {}".format(
            MONTHS[df["Month"].value_counts().idxmax() - 1].title()
        )
    )

    # Most common day of week
    st.markdown(
        "* The most common day of week is: {}".format(
            DAYS[df["Day of Week"].value_counts().idxmax() - 1].title()
        )
    )

    # Most common start hour
    st.markdown(
        "* The most common start hour is: {}".format(
            df["Start Hour"].value_counts().idxmax()
        )
    )

    # Trip duration stats
    st.markdown("### Trip duration")

    st.markdown(
        "* The total travel time is: {} hours".format(
            round(df["Trip Duration"].sum() / 3600, 2)
        )
    )

    st.markdown(
        "* The average (mean) travel time is: {} minutes".format(
            round(df["Trip Duration"].mean() / 60, 2)
        )
    )

    # Most frequent start stations chart
    start_station_counts = df["Start Station"].value_counts()
    most_frequent_start_stations = start_station_counts.head()

    most_frequent_start_stations_df = (
        most_frequent_start_stations.to_frame().reset_index()
    )

    most_frequent_start_stations_chart_data = most_frequent_start_stations_df.rename(
        columns={"index": "Start Station", "Start Station": "Number of Trips"}
    )

    st.markdown("### Most commonly used start stations")

    most_frequent_start_stations_chart = (
        alt.Chart(most_frequent_start_stations_chart_data)
        .mark_bar()
        .encode(x="Number of Trips", y=alt.Y("Start Station", sort="-x"))
        .properties(width="container", height=200)
    )

    st.altair_chart(most_frequent_start_stations_chart, use_container_width=True)

    # Most frequent end stations chart
    start_station_counts = df["End Station"].value_counts()
    most_frequent_start_stations = start_station_counts.head()

    most_frequent_start_stations_df = (
        most_frequent_start_stations.to_frame().reset_index()
    )

    most_frequent_start_stations_chart_data = most_frequent_start_stations_df.rename(
        columns={"index": "End Station", "End Station": "Number of Trips"}
    )

    st.markdown("### Most commonly used end stations")

    most_frequent_start_stations_chart = (
        alt.Chart(most_frequent_start_stations_chart_data)
        .mark_bar()
        .encode(x="Number of Trips", y=alt.Y("End Station", sort="-x"))
        .properties(width="container", height=200)
    )

    st.altair_chart(most_frequent_start_stations_chart, use_container_width=True)

    st.markdown("### Most common combination of start and end stations")

    st.write(
        df.groupby(["Start Station", "End Station"])
        .size()
        .sort_values(ascending=False)
        .head()
        .to_frame()
        .reset_index()
        .rename(columns={0: "Number of Trips"})
    )

    # User stats (by Gender and Birth Year only if applicable)
    st.write("### Count of users per user type", df["User Type"].value_counts())

    if "Gender" in df.columns:
        st.write("### Count of users per gender", df["Gender"].value_counts())

    if "Birth Year" in df.columns:
        st.markdown("### User stats by birth")

        st.markdown(
            "* The earliest year of birth is: {}".format(int(df["Birth Year"].min()))
        )

        st.markdown(
            "* The most recent year of birth is: {}".format(int(df["Birth Year"].min()))
        )

        st.markdown(
            "* The most common year of birth is: {}".format(
                int(df["Birth Year"].value_counts().idxmax())
            )
        )


def load_data(city):
    try:
        df = pd.read_csv(DATA_DIR + "/" + CITY_DATA[city.lower()])

        return df
    except FileNotFoundError as e:
        st.error("The CSV file for the city you selected is not available.")


def create_additional_columns(df):
    # From Start Time
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Month"] = df["Start Time"].dt.month
    df["Day of Week"] = df["Start Time"].dt.dayofweek
    df["Start Hour"] = df["Start Time"].dt.hour

    if "Birth Year" in df.columns:
        generations = list()
        # Adds a new computed column (note: probably not very efficient and can be optimized?)
        for index, birth_year in df["Birth Year"].iteritems():
            for generation in GENERATIONS:
                years, generation_name = generation
                min_year, max_year = years

                if max_year and min_year:
                    if birth_year >= min_year and birth_year <= max_year:
                        generations.append((index, generation_name))
                elif not min_year:
                    if birth_year <= max_year:
                        generations.append((index, generation_name))
                else:
                    if birth_year >= min_year:
                        generations.append((index, generation_name))

        df["Generation"] = pd.Series(
            data=map(lambda x: x[1], generations),
            index=map(lambda x: x[0], generations),
        )

    return df


@st.cache
def prepare_data(city):
    df = load_data(city)
    df = create_additional_columns(df)

    return df


def format_label(item):
    return item.title()


if __name__ == "__main__":
    main()
