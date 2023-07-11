import streamlit as st
from streamlit_space import space

import pandas as pd
import numpy as np
import datetime

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
 
st.set_option('deprecation.showPyplotGlobalUse', False)

# Plotting default parameters:
plt.rcParams['axes.axisbelow'] = True    #Grid below plots
plt.rcParams['figure.figsize'] = (7.5,5) #Default figure size

with st.sidebar:
    st.markdown("Author: **:blue[Group 9]**")
    st.write("Date: ", datetime.date(2023, 7, 11))
    st.text("Description: Interactive Web Application \n for Python Project 2.")

st.title("Fast Food Analysis")
'''
We analyze the `fastfood` dataset provided at [Kaggle](https://www.kaggle.com/datasets/ulrikthygepedersen/fastfood-nutrition).
'''

with st.expander("About the `fastfood` dataset"):
        '''
        ## About the `fastfood` dataset

        This is a fast food nutrition dataset, which provides a comprehensive breakdown of the nutritional content of various 
        fast food products from popular fast food chains.

        Fast food is known for its convenience and affordability, but it is also infamous for its high-calorie, high-fat, 
        and high-sugar content. This dataset aims to shed light on the nutritional value of these fast food products, helping 
        consumers make more informed decisions about their food choices.

        This dataset provides the information on calories, fat, carbohydrates, protein, and other key nutrients. 
        By analyzing this dataset, we can gain a better understanding of the nutritional impact of fast food consumption 
        and work towards creating healthier food options in the fast food industry.

        The variables present in the dataset: 

        | **Variable name** | **Description**                      | **Data type** |
        | ----------------- | ------------------------------------ | ------------- |
        |  restaurant       | Name of restaurant                   | text          |
        |  item             | Name of item                         | text          |
        |  calories         | Total calories (cal)                 | numeric       |
        |  cal_fat          | Calories from fat (cal)              | numeric       |
        |  total_fat        | Total fat (g)                        | numeric       |
        |  sat_fat          | Saturated fat (g)                    | numeric       |
        |  trans_fat        | Trans fat (g)                        | numeric       |
        |  cholesterol      | Cholesterol (mg)                     | numeric       |
        |  sodium           | Sodium (mg)                          | numeric       |
        |  total_carb       | Total carbonhydrates                 | numeric       |
        |  fiber            | Fibers                               | numeric       |
        |  sugar            | Sugar (g)                            | numeric       |
        |  protein          | Protein                              | numeric       |
        |  vit_a            | Vitamin A                            | numeric       |
        |  vit_c            | Vitamin C                            | numeric       |
        |  calcium          | Calcium                              | numeric       |
        |  salad            | Inidicate if the item is salad or not| text          |
        '''

@st.cache_data
def import_and_clean(dat):
        _df = pd.read_csv(dat)
        #_df.fillna(value={
        #       'fiber'   : _df['fiber'].mean(),
        #       'protein' : _df['protein'].mean(),
        #       'vit_a'   : _df['vit_a'].mean(),
        #       'vit_c'   : _df['vit_c'].mean(),
        #       'calcium' : _df['calcium'].mean()},
        #       inplace=True
        #)
        _df.fillna(value={x : _df[x].mean() for x in _df.select_dtypes(include='number').columns})
        return _df

df = import_and_clean('fastfood.csv')
df

_labels = {'restaurant': 'Restaurant', 
           'item': 'Item', 
           'calories': 'Calories', 
           'cal_fat': 'Calories from fat', 
           'total_fat': 'Total fat', 
           'sat_fat': 'Saturated fat', 
           'trans_fat': 'Trans fat', 
           'cholesterol': 'Cholesterol', 
           'sodium': 'Sodium', 
           'total_carb': 'Total carbohydrate', 
           'fiber': 'Fiber', 
           'sugar': 'Sugar', 
           'protein': 'Protein',
           'vit_a': 'Vitamin A', 
           'vit_c': 'Vitamin C', 
           'calcium': 'Calcium'
          }

def show(fig):
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

'''
## Item count by restaurants
'''

_df = df['restaurant'].value_counts().sort_values()
restaurants = _df.index

cols = st.columns(2)
with cols[0]:
        fig1a = px.bar(_df, x = _df.index, y =_df.values, text_auto=True, title="In frequency", labels=_labels)
        show(fig1a)
with cols[1]:
        fig1b = px.pie(_df, values="count", names=_df.index, hole=0.4, title="In percentage", labels=_labels)
        show(fig1b)

'''
## Relationship between nutritions
'''

_df = df.drop(['salad','restaurant','item'], axis = 1)
_df.rename(columns=_labels, inplace=True)

sns.heatmap(_df.corr(), fmt = '.2f', annot=True, cmap="BuGn")
plt.title('Correlation between nutritions')
st.pyplot()

with st.expander("Correlation analysis"):
        '''
        If we define a correlation greater than 0.7 to be considered a "strong" correlation, then we can see which variables are strongly correlated to each others.

        - **Calories** are strongly correlated to saturated fat, cholesterol, sodium, carbs, and protein
        - **Total fat** is strongly correlated to saturated fat, cholesterol, and protein
        - **Cholesterol** is strongly correlated to calories, saturated fat, and protein
        - **Sodium** is strongly correlated to calories and protein
        - **Carbohydrates** are strongly correlated to calories
        - **Protein** is strongly correlated to calories and cholesterol

        Besides, we can deduce some interesting facts:

        - Calories are affected by many types of nutrition.
        - Comparing to saturated fat, trans fat has weaker correlation to other nutrition, means that it cause less harm.
        - Fats create the most energy, then the protein, sodium and cholesterol.
        - Carbs and fiber have a good correlation, because nutritious carbohydrate foods provide a rich source of fiber, since fiber itself is a form of carbohydrate.
        - Calcium also has a fair correlation with carbs and fibers.
        '''

'''
## Effects of fat, carbohydate and protein on calories
'''

col1, col2 = st.columns([1,3])

with col1:
        space(lines=10)
        _x = st.radio( "Choose a category:",
            ('total_fat', 'total_carb', 'protein'))

with col2:
        fig2a = px.scatter(df, x=_x, y="calories", color="restaurant",
                        labels=_labels, 
                        size="calories", 
                        opacity=0.5,
                        title = "%s to calories relationship" % _labels[_x], 
                        trendline='ols', 
                        trendline_scope="overall")
        show(fig2a)

fig2b = px.scatter(df, x=_x, y="calories", 
               labels=_labels, 
               color="restaurant", 
               opacity=0.5, 
               facet_col="restaurant",
               facet_col_wrap=3, 
               trendline='ols')
show(fig2b)

'''
## Average nutrition by restaurants
'''

_df = df.drop(['item', 'salad'], axis=1).groupby('restaurant').mean()
#_df = df.drop(['restaurant', 'item', 'salad'], axis=1)
col1, col2 = st.columns([1,3])

with col1:
        _x = st.radio( "Choose a category:", _df.columns)

with col2:
        #fig = px.histogram(df, x='restaurant', y=_x, histfunc='avg', text_auto='.2f')
        fig3 = px.bar(_df, x=_df.index, y=_df[_x], color='calories', text_auto='.2f', labels=_labels)
        show(fig3)

'''
## Analysis of calorie content
'''

tabs = st.tabs(["Box plot", "Histogram", "Custom histogram"])

with tabs[0]: 
        fig4a = px.box(df, x='restaurant', y='calories', labels=_labels, color='restaurant')
        fig4a.update_layout(showlegend=False)
        show(fig4a)

with tabs[1]: 
        col1, col2 = st.columns([1,3])

        with col1:
                st.write(df['calories'].describe())

        with col2:
                fig4a = px.histogram(df, x='calories', color='restaurant', opacity=0.5, 
                                   marginal='box', 
                                   labels={'calories': 'Calories'}, 
                                   title='Fastfood Calorie Histogram')
                show(fig4a)

        fig4b = px.histogram(df, x='calories', color='restaurant', 
                       facet_col="restaurant",
                       facet_col_wrap=3)
        show(fig4b)

with tabs[2]:
        options = st.multiselect( 'Choose a restaurant:', restaurants)
        cal_range = st.slider("Choose a range for calories", 
                    int(df['calories'].min()), int(df['calories'].max()), (20, 2000)
                    )
        st.write("Calorie range:", cal_range)

        fig4a = px.histogram(df[df['restaurant'].isin(options) & (df['calories'] >= cal_range[0]) & (df['calories'] <= cal_range[1])], 
                             x='calories', color='restaurant', opacity=0.5, 
                             marginal='box', 
                             labels={'calories': 'Calories'}, 
                             title='Fastfood Calorie Histogram')
        show(fig4a)
'''
### Top 10 meals with the highest and lowest calories in all restaurants
'''

tabs = st.tabs(["Top 10 highest", "Top 10 lowest"])

with tabs[0]:
        fig5 = px.bar(df.nlargest(10, 'calories'), y='item', x='calories', text_auto=True, labels=_labels, color='restaurant', 
                     title='Top 10 meals with highest calories')
        fig5.update_layout(yaxis = {"categoryorder":"total ascending"})
        show(fig5)

with tabs[1]:
        fig5 = px.bar(df.nsmallest(10, 'calories'), y='item', x='calories', text_auto=True, labels=_labels, color='restaurant', 
                     title='Top 10 meals with lowest calories')
        fig5.update_layout(yaxis = {"categoryorder":"total descending"})
        show(fig5)