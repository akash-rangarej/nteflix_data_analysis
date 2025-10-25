import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #E50914;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 2rem;
        color: #E50914;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #E50914;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #E50914;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv('netflix1.csv')
    data = df.copy()
    data.drop_duplicates(inplace=True)
    
    # Data preprocessing
    data['date_added'] = pd.to_datetime(data['date_added'])
    data['year_added'] = data['date_added'].dt.year
    data['month_added'] = data['date_added'].dt.month
    data['genres'] = data['listed_in'].apply(lambda x: x.split(","))
    
    return data

data = load_data()

# Sidebar for filters and navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.title("🎬 Netflix Analytics")

analysis_option = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["📊 Overview", "🎭 Content Analysis", "📈 Trends Over Time", "👥 Directors & Creators", "🔍 Word Cloud Analysis"]
)

# Overview Section
if analysis_option == "📊 Overview":
    st.markdown('<h1 class="main-header">Netflix Data Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_content = len(data)
        st.metric("Total Content", f"{total_content:,}")
    
    with col2:
        movies_count = len(data[data['type'] == 'Movie'])
        st.metric("Movies", f"{movies_count:,}")
    
    with col3:
        tv_shows_count = len(data[data['type'] == 'TV Show'])
        st.metric("TV Shows", f"{tv_shows_count:,}")
    
    with col4:
        latest_year = data['year_added'].max()
        st.metric("Latest Year", latest_year)
    
    # Content distribution with Plotly
    st.markdown('<h2 class="section-header">Content Distribution</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive pie chart
        type_counts = data['type'].value_counts()
        fig_pie = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Content Type Distribution",
            color=type_counts.index,
            color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Rating distribution
        rating_counts = data['rating'].value_counts().head(10)
        fig_rating = px.bar(
            x=rating_counts.values,
            y=rating_counts.index,
            orientation='h',
            title="Top 10 Content Ratings",
            color=rating_counts.values,
            color_continuous_scale='Reds'
        )
        fig_rating.update_layout(xaxis_title="Count", yaxis_title="Rating")
        st.plotly_chart(fig_rating, use_container_width=True)

# Content Analysis Section
elif analysis_option == "🎭 Content Analysis":
    st.markdown('<h1 class="main-header">Content & Genre Analysis</h1>', unsafe_allow_html=True)
    
    # Genre analysis
    st.markdown('<h2 class="section-header">Genre Analysis</h2>', unsafe_allow_html=True)
    
    # Interactive genre selection
    all_genres = sum(data['genres'], [])
    genre_counts = pd.Series(all_genres).value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        top_n = st.slider("Select number of top genres to display:", 5, 20, 10)
        
        top_genres = genre_counts.head(top_n)
        fig_genres = px.bar(
            x=top_genres.values,
            y=top_genres.index,
            orientation='h',
            title=f"Top {top_n} Genres on Netflix",
            color=top_genres.values,
            color_continuous_scale='Viridis'
        )
        fig_genres.update_layout(xaxis_title="Count", yaxis_title="Genre")
        st.plotly_chart(fig_genres, use_container_width=True)
    
    with col2:
        st.markdown("### Genre Insights")
        st.write(f"**Total unique genres:** {len(genre_counts)}")
        st.write(f"**Most popular genre:** {genre_counts.index[0]} ({genre_counts.iloc[0]} titles)")
        st.write(f"**Average titles per genre:** {round(genre_counts.mean(), 1)}")

# Trends Over Time Section
elif analysis_option == "📈 Trends Over Time":
    st.markdown('<h1 class="main-header">Content Trends Over Time</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Yearly trend
        yearly_trend = data['year_added'].value_counts().sort_index()
        fig_yearly = px.line(
            x=yearly_trend.index,
            y=yearly_trend.values,
            title="Content Added by Year",
            markers=True
        )
        fig_yearly.update_layout(xaxis_title="Year", yaxis_title="Number of Titles Added")
        fig_yearly.update_traces(line=dict(color='#E50914', width=3))
        st.plotly_chart(fig_yearly, use_container_width=True)
    
    with col2:
        # Monthly distribution
        monthly_trend = data['month_added'].value_counts().sort_index()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        fig_monthly = px.bar(
            x=months,
            y=monthly_trend.values,
            title="Content Added by Month",
            color=monthly_trend.values,
            color_continuous_scale='Bluered'
        )
        fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Number of Titles Added")
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Interactive time series by type
    st.markdown('<h3 class="section-header">Content Growth by Type</h3>', unsafe_allow_html=True)
    
    yearly_by_type = data.groupby(['year_added', 'type']).size().reset_index(name='count')
    fig_trend_type = px.area(
        yearly_by_type,
        x='year_added',
        y='count',
        color='type',
        title="Content Growth by Type Over Time",
        color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'}
    )
    st.plotly_chart(fig_trend_type, use_container_width=True)

# Directors & Creators Section
elif analysis_option == "👥 Directors & Creators":
    st.markdown('<h1 class="main-header">Directors & Content Creators</h1>', unsafe_allow_html=True)
    
    # Top directors
    director_counts = data['director'].value_counts().head(15)
    director_counts = director_counts[director_counts.index != 'Unknown']
    
    fig_directors = px.bar(
        x=director_counts.values,
        y=director_counts.index,
        orientation='h',
        title="Top Directors on Netflix",
        color=director_counts.values,
        color_continuous_scale='Hot'
    )
    fig_directors.update_layout(xaxis_title="Number of Titles", yaxis_title="Director")
    st.plotly_chart(fig_directors, use_container_width=True)
    
    # Country analysis
    st.markdown('<h3 class="section-header">Content by Country</h3>', unsafe_allow_html=True)
    
    country_data = data['country'].value_counts().head(15)
    fig_country = px.treemap(
        names=country_data.index,
        parents=[''] * len(country_data),
        values=country_data.values,
        title="Content Distribution by Country",
        color=country_data.values,
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_country, use_container_width=True)

# Word Cloud Analysis Section
elif analysis_option == "🔍 Word Cloud Analysis":
    st.markdown('<h1 class="main-header">Title Analysis - Word Clouds</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Movie Titles Word Cloud")
        movie_titles = data[data['type'] == 'Movie']['title'].dropna()
        
        if len(movie_titles) > 0:
            wordcloud_movie = WordCloud(
                width=800,
                height=400,
                background_color='black',
                colormap='Reds',
                max_words=100
            ).generate(' '.join(movie_titles))
            
            fig_movie, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud_movie, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_movie)
    
    with col2:
        st.markdown("### TV Show Titles Word Cloud")
        tv_titles = data[data['type'] == 'TV Show']['title'].dropna()
        
        if len(tv_titles) > 0:
            wordcloud_tv = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap='Blues',
                max_words=100
            ).generate(' '.join(tv_titles))
            
            fig_tv, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud_tv, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_tv)
    
    # Additional insights
    st.markdown("### Title Length Analysis")
    data['title_length'] = data['title'].str.len()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_length_movie = px.histogram(
            data[data['type'] == 'Movie'],
            x='title_length',
            title="Movie Title Length Distribution",
            color_discrete_sequence=['#E50914']
        )
        st.plotly_chart(fig_length_movie, use_container_width=True)
    
    with col2:
        fig_length_tv = px.histogram(
            data[data['type'] == 'TV Show'],
            x='title_length',
            title="TV Show Title Length Distribution",
            color_discrete_sequence=['#221F1F']
        )
        st.plotly_chart(fig_length_tv, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Netflix Data Analysis Dashboard | Created with Streamlit</div>",
    unsafe_allow_html=True
)