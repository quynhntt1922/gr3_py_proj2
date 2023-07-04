import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
 
st.set_option('deprecation.showPyplotGlobalUse', False)

with st.expander("About the dataset"):
        '''
        ## About the dataset

        This is a fast food nutrition dataset, which provides a comprehensive breakdown of the nutritional content of various fast food products from popular fast food chains.

        Fast food is known for its convenience and affordability, but it is also infamous for its high-calorie, high-fat, and high-sugar content. This dataset aims to shed light on the nutritional value of these fast food products, helping consumers make more informed decisions about their food choices.

        This dataset provides the information on calories, fat, carbohydrates, protein, and other key nutrients. By analyzing this dataset, we can gain a better understanding of the nutritional impact of fast food consumption and work towards creating healthier food options in the fast food industry.

        The dataset is provided at [Kaggle](https://www.kaggle.com/datasets/ulrikthygepedersen/fastfood-nutrition).

        The variables present in the dataset: 

        | **Variable name** | **Description**                      |
        | ----------------- | ------------------------------------ |
        |  restaurant       | Name of restaurant                   |
        |  item             | Name of item                         |
        |  calories         | Total calories (cal)                 |
        |  cal_fat          | Calories from fat (cal)              |
        |  total_fat        | Total fat (g)                        |
        |  sat_fat          | Saturated fat (g)                    |
        |  trans_fat        | Trans fat (g)                        |
        |  cholesterol      | Cholesterol (mg)                     |
        |  sodium           | Sodium (mg)                          |
        |  total_carb       | Total carbonhydrates                 |
        |  fiber            | Fibers                               |
        |  sugar            | Sugar (g)                            |
        |  protein          | Protein                              |
        |  vit_a            | Vitamin A                            |
        |  vit_c            | Vitamin C                            |
        |  calcium          | Calcium                              |
        |  salad            | Inidicate if the item is salad or not|
        '''


with st.expander("Dataset"):
        '''
        ## Dataset
        '''

        with st.echo():
                df = pd.read_csv('fastfood.csv')
                df

        # Plotting default parameters:
        plt.rcParams['axes.axisbelow'] = True    #Grid below plots
        plt.rcParams['figure.figsize'] = (7.5,5) #Default figure size

with st.expander("Tidy the dataset"):
        '''
        ## Tidy the dataset
        '''

        with st.echo():
                def missings(df):
                    nan_count = df.isna().sum().sort_values(ascending= False)
                    nan_perc = (nan_count / df.shape[0]) * 100
                    _table = pd.concat([nan_count,nan_perc],axis = 1).reset_index()
                    _table.rename(columns = {0 : 'NA Count' , 1:'NA Percentage'}, inplace=True)
                    return _table

                missings(df)

        st.write(missings(df))

        '''
        - There is 1 item (0.19%) which we do not know the protein content
        - There are 12 items (2.33%) which we do not know the fiber content
        - There are 214 items (41.55%) which we do not know the vitamin A content
        - There are 210 items (40.78%) which we do not know the vitamin C content
        - There are 210 items (40.78%) which we do not know the calcium content

        There were too many (~ 40%) missing values in some columns, we would not drop the rows with missing values. 
        We instead fill them with the average value of the its corresponding column:
        '''

        with st.echo():
                df.fillna(value={
                       'fiber' : df['fiber'].mean(),
                       'protein' : df['protein'].mean(),
                       'vit_a' : df['vit_a'].mean(),
                       'vit_c' : df['vit_c'].mean(),
                       'calcium' : df['calcium'].mean()},
                       inplace=True
                )

'''
## Analyzing and visualizing the dataset

### Item count by restaurants
'''

cols = st.columns(2)

with cols[0]:
        _df = df['restaurant'].value_counts().sort_values()
        ax = sns.barplot(x=_df.index, y=_df.values)
        plt.xticks(rotation='vertical')
        plt.bar_label(ax.containers[0], padding=3)
        plt.ylim(top=1.1*max(_df))
        plt.xlabel('')
        plt.ylabel('Count')
        plt.title('Item Count by Restaurant')

        st.pyplot()

with cols[1]:
        _df.plot.pie(y = 'item', autopct='%1.0f%%', legend=None)
        plt.ylabel('')
        plt.title('Item Share by Restaurant (in Dataset)')

        st.pyplot()

'''
### Relationship between nutritions
'''

with st.echo():
        sns.heatmap(df.drop(['salad','restaurant','item'], axis = 1).corr(), fmt = '.2f', annot=True, cmap="BuGn")
        plt.title('Correlation between Nutritions')
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
### Effects of fat, carbohydate and protein on calories
'''

cols = st.columns(3)

with cols[0]:
        sns.regplot(x='total_fat', y='calories', data=df, fit_reg=True, scatter_kws=dict(alpha=.5))
        plt.xlabel('Total fat')
        plt.ylabel('Calories')
        plt.title('Total Fat to Calories Relationship') 
        st.pyplot()

with cols[1]:
        sns.regplot(x='total_carb', y='calories', data=df, fit_reg=True, scatter_kws=dict(alpha=.5))
        plt.xlabel('Total carbohydrate')
        plt.ylabel('Calories')
        plt.title('Total Carbohydrate to Calories Relationship') 
        st.pyplot()

with cols[2]:
        sns.regplot(x='protein', y='calories', data=df, fit_reg=True, scatter_kws=dict(alpha=.5))
        plt.xlabel('Protein')
        plt.ylabel('Calories')
        plt.title('Protein to Calories Relationship') 
        st.pyplot()

'''
### Average nutrition by restaurants
'''

_df = df.drop(['item', 'salad'], axis=1).groupby('restaurant').mean()

cols = st.columns(2)

with cols[0]:
        ax = pd.concat([_df['calories'], _df['cal_fat']], axis=1).plot.bar(width=0.8, cmap="Set3")
        plt.legend(['Calories', 'Calories from fat'])
        for x in ax.containers:
            plt.bar_label(x, padding=3, fmt='%.2f', size=8)
        plt.ylim(top=1.1*max(_df['calories']))
        plt.xlabel('')
        plt.title('Average Calorie by Restaurant')
        st.pyplot()

        ax = pd.concat([_df['total_fat'], _df['sat_fat'], _df['trans_fat']], axis=1).plot.bar(width=0.9, cmap="Set3")
        plt.legend(['Total fat', 'Saturated fat', 'Trans fat'])
        for x in ax.containers:
            plt.bar_label(x, padding=3, fmt='%.2f', size=8)
        plt.ylim(top=1.1*max(_df['total_fat']))
        plt.xlabel('')
        plt.title('Average Fat by Restaurant')
        st.pyplot()

        d = _df['protein'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Protein')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))
        st.pyplot()

        d = _df['cholesterol'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Cholesterol')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))
        st.pyplot()

with cols[1]:
        d = _df['sodium'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Sodium')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))
        st.pyplot()

        d = _df['sugar'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Sugar')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))
        st.pyplot()

        d = _df['fiber'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Fiber Content')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))
        st.pyplot()

        ax = pd.concat([_df['vit_a'], _df['vit_c']], axis=1).plot.bar(width=0.9, cmap="Set3")
        plt.legend(['Vitamin A', 'Vitamin C'])
        for x in ax.containers:
            plt.bar_label(x, padding=3, fmt='%.2f', size=8)
        plt.ylim(top=1.1*max(_df['vit_c']))
        plt.xlabel('')
        plt.title('Average Vitamin by Restaurant')
        st.pyplot()

d = _df['calcium'].sort_values()
ax = sns.barplot(x=d.index, y=d.values)
plt.xticks(rotation='vertical')
plt.xlabel('Restaurants')
plt.ylabel('Average Calcium Content')
plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
plt.ylim(top=1.1*max(d))
st.pyplot()

'''
### Analysis of calorie content
'''

sns.boxplot(x='restaurant', y='calories', data=df)
plt.xticks(rotation='vertical')
plt.xlabel('Restaurant')
plt.ylabel('Calories')
plt.title('Fastfood Calorie Box Plot')
st.pyplot()

'''
### Distribution of calories in all items
'''

with st.echo():
        df['calories'].describe()
st.write(df['calories'].describe())

sns.histplot(x='calories', data=df, kde=True)
#kde=True: compute a kernel density estimate to smooth the distribution
plt.xlabel('Calories')
plt.title('Fastfood Calorie Histogram')
st.pyplot()

'''
### Top 10 meals with the highest and lowest calories in all restaurants
'''

cols = st.columns(2)

with cols[0]:
        _df = df[['item', 'calories']].sort_values('calories', ascending=False).iloc[:10]
        ax = _df.plot.barh(x='item', y='calories', ylabel='', title='Top 10 Meals with Highest Calories')
        plt.bar_label(ax.containers[0], padding=3)
        plt.xlim(right=1.1*max(_df['calories']))
        st.pyplot()

with cols[1]:
        _df = df[['item', 'calories']].sort_values('calories', ascending=True).iloc[:10]
        ax = _df.plot.barh(x='item', y='calories', ylabel='', title='Top 10 Meals with Lowest Calories')
        plt.bar_label(ax.containers[0], padding=3)
        plt.xlim(right=1.1*max(_df['calories']))
        st.pyplot()