import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
# đọc dữ liệu 
movies_data = pd.read_csv('https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv')
movies_data.dropna()



# sidebar
st.sidebar.write('Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range')
score = st.sidebar.slider('Choose a value:', min_value=1.00, max_value=10.00, value=(1.00, 10.00))

st.sidebar.write('Select your preferred genre(s) and year to view the movies released that year and on that genre')
genre= st.sidebar.multiselect('Choose Genre:', movies_data['genre'].unique(), default=['Action'])
year= st.sidebar.selectbox('Choose a Year',movies_data['year'].unique() )

# Các tiêu đề
st.title('Interactive Dashboard')
st.header('Interact with this dashboard using the widgets on the sidebar')


# Chia trang thành hai cột bằng phương thức st.columns()
col1, col2 = st.columns(2)
# Viết tiêu đề trên mỗi cột
with col1:
    st.write('#### Interact with this dashboard using the widgets on the sidebar')
    selected_columns = movies_data[movies_data['genre'].isin(genre) & (movies_data['year']== year)]

    selected_columns.reset_index(drop=True, inplace=True)
    st.table(selected_columns[['name','genre','year']])
    

with col2:
    st.write('#### Lists of movies filtered by year and Genre')
    score_info = (movies_data['score'].between(*score))
    rating_count_year = movies_data[score_info].groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'genre', y = 'score')
    figpx.update_layout(
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'))
    st.plotly_chart(figpx)

st.write("""Average Movie Budget, Grouped by Genre""")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

fig = plt.figure(figsize = (19, 10))
plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing the Average Budget of Movies in Each Genre')
st.pyplot(fig)