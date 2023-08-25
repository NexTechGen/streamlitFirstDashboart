import streamlit as st
import pandas as pd
import pandas_bokeh
from sklearn.datasets import load_wine
import yfinance as yf

st.set_page_config(layout='wide')

@st.cache_data
def load_data():
    wine = load_wine()
    wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
    wine_df['WineType'] = [wine.target_names[t] for t in wine.target]
    return wine_df

wine_df = load_data()
ingredients = wine_df.drop(columns=['WineType']).columns

avg_wine_df = wine_df.groupby('WineType').mean().reset_index()

# Top section
st.subheader("Rusaid Ahamed :green[1st DataScience Dashboard]")

st.title("Wine Dataset :green[Analysis] :tea: :coffee: :chart: :bar_chart:")
st.markdown("Wine Analysis dashboard let us explore relationship between various **ingredients** used in creation of 3 different types of wine (*Class_0, Class_1 & Class_2*)")

# make sidebar
st.sidebar.markdown('### Scatter Chart: Explore Relationship Between Ingredients :')

# DropDown for change  X and Y
x_axis = st.sidebar.selectbox("X-Axis", ingredients)
y_axis = st.sidebar.selectbox("Y-Axis", ingredients, index=1)


# create checkBox
color_encode = st.sidebar.checkbox(label="Color.Encode by Wine Type")


# multy selecter
st.sidebar.markdown("### Bar Chart: Average Ingredients per Wine Type : ")
bar_multyselect = st.sidebar.multiselect(label='Bar Chart Ingredients', options=ingredients, default=['alcohol', 'malic_acid', 'ash'])


# fit on one row
container = st.container()
chart1, chart2 = container.columns(2)

with chart1:
    if x_axis and y_axis:
        # Scatter Chart
        scater_fig = wine_df.plot_bokeh.scatter(x=x_axis, y=y_axis, category= "WineType" if color_encode else None,
                                                xlabel=x_axis.capitalize(), ylabel=y_axis.capitalize(), title=f"{x_axis.capitalize()} vs {y_axis.capitalize()}",
                                                fontsize_title=25, fontsize_label=12,
                                                figsize=(650, 500), show_figure=False)
        # fit on window Scatter chart
        st.bokeh_chart(scater_fig, use_container_width=True)

with chart2:
    if bar_multyselect:
        st.header("Avg Ingredients")
        st.bar_chart(avg_wine_df, x="WineType", y=bar_multyselect, height=500, use_container_width=True)

