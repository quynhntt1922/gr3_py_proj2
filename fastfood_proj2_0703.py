import streamlit as st
import io

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
 
st.set_option('deprecation.showPyplotGlobalUse', False)

'''
# 1. About the dataset

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

'''
# 2. Loading libraries, dataset, and default plotting parameters
'''

'''
## 2.1. Libraries
'''

code = '''
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
'''
st.code(code, language='python')

'''## 2.2. Dataset

We read our dataset by the `read_csv()` method from `pandas`, then assign to the `df` object. Below is what `df` returns:
'''

with st.echo():
        df = pd.read_csv('fastfood.csv')
        df

'''
To view the information about this data frame, we use method `info()`:
'''

code = '''
df.info()
'''
st.code(code, language='python')

buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()

st.text(s)

'''
From the output, we can see that our dataset has 515 observations, with 17 variables as described above. Among these variables, only `restaurant`, `item` and `salad` have the data type of 'object' (non numerical), and the others are numerical: integers or float.

## 2.3. Default plotting parameters
'''

with st.echo():
        plt.rcParams['axes.axisbelow'] = True    #Grid below plots
        plt.rcParams['figure.figsize'] = (7.5,5) #Default figure size

'''
# 3. Tidy the dataset

Not every dataset is clean for analyzing. They may have missing values, or unusual outliers due to sampling issues, typing errors... Therefore, we must first prepare the data to ensure that it is good to analyze. In this project, I will only take care of missing values.

Let us first count how many missing values in each column, and their corresponding percentage:
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
The output shows that:

- There is 1 item (0.19%) which we do not know the protein content
- There are 12 items (2.33%) which we do not know the fiber content
- There are 214 items (41.55%) which we do not know the vitamin A content
- There are 210 items (40.78%) which we do not know the vitamin C content
- There are 210 items (40.78%) which we do not know the calcium content

**Solution**: Since there were too many (~ 40%) missing values in some columns, we would not drop the rows with missing values. We instead fill them with the average value of the its corresponding column. This is done with the following code:
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
The above code filled missing values with its corresponding mean.

# 4. Analyzing and visualizing the dataset

## 4.1. Item count by restaurants

First, let us count how many dishes are there according to each restaurant. Then, we visualize this on a bar chart:
'''

with st.echo():
        _df = df['restaurant'].value_counts().sort_values()
        _df

        ax = sns.barplot(x=_df.index, y=_df.values)
        plt.xticks(rotation='vertical')
        plt.bar_label(ax.containers[0], padding=3)
        plt.ylim(top=1.1*max(_df))
        plt.xlabel('')
        plt.ylabel('Count')
        plt.title('Item Count by Restaurant')

st.pyplot()

'''
This chart illustrates the number of menu items collected in 8 different restaurants in the US. From the chart, the Taco Bell have the most dishes, of 115 dishes, while Chick Fil-A only have 27 items presented in the dataset. This does not conclude that Taco Bell has the most diverse menu, but it may due to the fact that not all restaurant items are accounted into this dataset.

We can also visualize the item count using a pie chart:
'''

with st.echo():
        _df.plot.pie(y = 'item', autopct='%1.0f%%', legend=None)
        plt.ylabel('')
        plt.title('Item Share by Restaurant (in Dataset)')

st.pyplot()

'''
## 4.2. Salad item count

With the same method, we check to see how many items in the dataset is a salad dish:
'''

with st.echo():
        df['salad'].value_counts()

st.write(df['salad'].value_counts())

'''
The output showed that all 515 dishes are not salad, which are expected to be unhealthy and have low fiber content.

## 4.3. Relationship between nutritions

### 4.3.1. Correlation between nutritions

Correlation value is a way to measure how much the two variables change together. The value of correlation is limited between -1 and +1:

- When *negatively correlated*: if one variable is moving in one direction, another is moving in the opposite direction.
- When *positively correlated*: if one variable is moving in one direction, another is also moving in the same direction.
- When *both are not correlated*: if one variable is moving in one direction, another may move in any direction.

The `pandas` package provides the `corr()` method to calculate the correlation between variables, but we first have to drop the categorical variables from the data frame (`restaurant`, `item`, and `salad`). After calculating the correlation, we can use `heatmap()` method from the `seaborn` package to plot the correlation between multiple variables in the dataset:
'''

with st.echo():
        sns.heatmap(df.drop(['salad','restaurant','item'], axis = 1).corr(), fmt = '.2f', annot=True, cmap="BuGn")
        plt.title('Correlation between Nutritions')
st.pyplot()

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

### 4.3.2. Effects of fat, carbohydate and protein on calories

Looking at the scatter plot of fat, carbohydrate and protein to calories, we assume that they all have a linear relationship.
'''

with st.echo():
        sns.regplot(x='total_fat', y='calories', data=df, fit_reg=True, scatter_kws=dict(alpha=.5))
        plt.xlabel('Total fat')
        plt.ylabel('Calories')
        plt.title('Total Fat to Calories Relationship') 

st.pyplot()

with st.echo():
        sns.regplot(x='total_carb', y='calories', data=df, fit_reg=True, scatter_kws=dict(alpha=.5))
        plt.xlabel('Total carbohydrate')
        plt.ylabel('Calories')
        plt.title('Total Carbohydrate to Calories Relationship') 

st.pyplot()

with st.echo():
        sns.regplot(x='protein', y='calories', data=df, fit_reg=True, scatter_kws=dict(alpha=.5))
        plt.xlabel('Protein')
        plt.ylabel('Calories')
        plt.title('Protein to Calories Relationship') 

st.pyplot()

'''
## 4.4. Average nutrition by restaurants

We calculate the average nutrition contents grouped by restaurants, by following steps:

- Drop `item` and `salad` column, keeping only restaurant names and nutrition variables
- Group nutrition by restaurants
- Calculate average value of each column
'''

with st.echo():
        _df = df.drop(['item', 'salad'], axis=1).groupby('restaurant').mean()

'''
We can now visualize them.

### 4.4.1. Average calories by restaurants
'''

with st.echo():
        ax = pd.concat([_df['calories'], _df['cal_fat']], axis=1).plot.bar(width=0.8, cmap="Set3")
        plt.legend(['Calories', 'Calories from fat'])
        for x in ax.containers:
            plt.bar_label(x, padding=3, fmt='%.2f', size=8)
        plt.ylim(top=1.1*max(_df['calories']))
        plt.xlabel('')
        plt.title('Average Calorie by Restaurant')

st.pyplot()

'''
From the above chart, in average:

- A dish in **Chick Fil-A** has the lowest total calories (of 384 cals) and calories from fat (of 145 cals)
- A dish in **McDonalds** has the highest total calories (of 640 cals)
- A dish in **Sonic** has the highest calories from fat (of 338 cals)

This indicates that Chick Fil-A dishes are suitable for those who are in need to cut their calories and lose weight.

### 4.4.2. Average fat by restaurants
'''

with st.echo():
        ax = pd.concat([_df['total_fat'], _df['sat_fat'], _df['trans_fat']], axis=1).plot.bar(width=0.9, cmap="Set3")
        plt.legend(['Total fat', 'Saturated fat', 'Trans fat'])
        for x in ax.containers:
            plt.bar_label(x, padding=3, fmt='%.2f', size=8)
        plt.ylim(top=1.1*max(_df['total_fat']))
        plt.xlabel('')
        plt.title('Average Fat by Restaurant')

st.pyplot()

'''
From the above chart, in average:

- A dish in **Sonic** has the highest amount of total fat, saturated fat and trans fat, which are 37.6 g, 11.4 g and 0.934 g respectively.
- A dish in **Chick Fil-A** also has the lowest amount of total fat, saturated fat and trans fat, which are 16.1 g, 4.11 g, and 0.037g respectively.

Again, Chick Fil-A has a more healthier menu in terms of fat content, while the Sonic dishes seems to be much more greasy.

### 4.4.3. Average protein by restaurants
'''

with st.echo():
        d = _df['protein'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Protein')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))

st.pyplot()

'''
In terms of average protein, **Taco Bell** dishes provide the least protein while **McDonalds**' provide the most.

Paying more attention, we can also see **Chick Fil-A** dishes are the second most protein nutritious. So far, Chick Fil-A dishes are not only low in fat and calories, but also provide us a good amount of protein.

### 4.4.4. Average cholesterol, sodium and sugar by restaurants 
'''

with st.echo():
        d = _df['cholesterol'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Cholesterol')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))

st.pyplot()

'''
From the above bar chart, **McDonalds** dishes are surprisingly high in cholesterol content while **Taco Bell** dishes have the lowest amount. People with heart disease therefore should consider switch their choice of fast food restaurant to Taco Bell.
'''

with st.echo():
        d = _df['sodium'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Sodium')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))

st.pyplot()

'''
**Taco Bell** has the least sodium content in their dishes, while **Arbys** seems to have the saltiest dishes in average.
'''

with st.echo():
        d = _df['sugar'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Sugar')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))

st.pyplot()

'''
Sugar content of dishes in each restaurant clearly varies, with the lowest of **Taco Bell** and **Chick Fil-A** and the highest of **McDonalds** and **Subway**. The highest is tripled the lowest!
'''

with st.echo():
        d = _df['fiber'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Fiber Content')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))

st.pyplot()

'''
In this bar chart, **Subway** and **Taco Bell** dishes have the highest amount of fiber content, which are almost doubled to the rest.
'''

with st.echo():
        ax = pd.concat([_df['vit_a'], _df['vit_c']], axis=1).plot.bar(width=0.9, cmap="Set3")
        plt.legend(['Vitamin A', 'Vitamin C'])
        for x in ax.containers:
            plt.bar_label(x, padding=3, fmt='%.2f', size=8)
        plt.ylim(top=1.1*max(_df['vit_c']))
        plt.xlabel('')
        plt.title('Average Vitamin by Restaurant')

st.pyplot()

'''
In terms of vitamins, **Subway** items are the highest in vitamin C and **McDonalds** items are the highest in vitamin A. On the other hand, **Sonic** dishes are extremely poor in vitamins.
'''

with st.echo():
        d = _df['calcium'].sort_values()
        ax = sns.barplot(x=d.index, y=d.values)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurants')
        plt.ylabel('Average Calcium Content')
        plt.bar_label(ax.containers[0], padding=3, fmt='%.2f')
        plt.ylim(top=1.1*max(d))

st.pyplot()

'''
In terms of calcium content, **Subway** dishes are extremely rich in calcium while **Chick Fil-A** items are relatively poor.

## 4.5. Analysis of calorie content

Since people are mostly interested in calorie content, here we dive deep into many aspects of this variable.

### 4.5.1. Boxplot of calories per restaurant
'''

with st.echo():
        sns.boxplot(x='restaurant', y='calories', data=df)
        plt.xticks(rotation='vertical')
        plt.xlabel('Restaurant')
        plt.ylabel('Calories')
        plt.title('Fastfood Calorie Box Plot')

st.pyplot()

'''
### 4.5.2. Distribution of calories in all items

First, let us have a statistic summary of item calories:
'''

with st.echo():
        df['calories'].describe()

st.write(df['calories'].describe())

'''
Visualize this using a histogram, and overlay a density plot:
'''


with st.echo():
        sns.histplot(x='calories', data=df, kde=True)
        #kde=True: compute a kernel density estimate to smooth the distribution
        plt.xlabel('Calories')
        plt.title('Fastfood Calorie Histogram')

st.pyplot()

'''
From the above table and distribution, we can see that there is a chance of 50% that a dish has the total calories of 490. The item calories are likely to fall between 330 and 690, and the average calorie content is about 531.

### 4.5.3. Top 10 meals with the highest and lowest calories in all restaurants
'''

with st.echo():
        _df = df[['item', 'calories']].sort_values('calories', ascending=False).iloc[:10]
        ax = _df.plot.barh(x='item', y='calories', ylabel='', title='Top 10 Meals with Highest Calories')
        plt.bar_label(ax.containers[0], padding=3)
        plt.xlim(right=1.1*max(_df['calories']))

st.pyplot()

with st.echo():
        _df = df[['item', 'calories']].sort_values('calories', ascending=True).iloc[:10]
        ax = _df.plot.barh(x='item', y='calories', ylabel='', title='Top 10 Meals with Lowest Calories')
        plt.bar_label(ax.containers[0], padding=3)
        plt.xlim(right=1.1*max(_df['calories']))

st.pyplot()