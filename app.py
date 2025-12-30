import streamlit as st
import os
from googleapiclient.discovery import build
from Senti import extract_video_id, analyze_sentiment, bar_chart, plot_sentiment
from YoutubeCommentScrapper import save_video_comments_to_csv, get_channel_info, get_channel_id, get_video_stats

st.set_page_config(page_title='YouTube Comment Lens', page_icon='LOGO.png', initial_sidebar_state='auto')

# API Configuration
try:
    DEVELOPER_KEY = st.secrets["general"]["API_KEY"]
except (FileNotFoundError, KeyError):
    st.error("API Key not found. Please configure .streamlit/secrets.toml")
    st.stop()

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Initialize API Client
@st.cache_resource
def get_youtube_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

youtube = get_youtube_service()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.sidebar.title("Sentimental Analysis")
st.sidebar.header("Enter YouTube Link")
youtube_link = st.sidebar.text_input("Link")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    
    if video_id:
        st.sidebar.write("The video ID is:", video_id)
        
        # Helper function to get channel ID safely
        channel_id = get_channel_id(youtube, video_id)
        
        if not channel_id:
            st.error("Could not retrieve video information. Please check the link.")
        else:
            # Save comments to data directory
            csv_file = save_video_comments_to_csv(youtube, video_id, output_dir='data')
            
            if csv_file and os.path.exists(csv_file):
                st.sidebar.success("Comments saved!")
                st.sidebar.download_button(
                    label="Download Comments", 
                    data=open(csv_file, 'rb').read(), 
                    file_name=os.path.basename(csv_file), 
                    mime="text/csv"
                )
                
                # Fetch Channel Info
                channel_info = get_channel_info(youtube, channel_id)
                
                if channel_info:
                    col1, col2 = st.columns(2)

                    with col1:
                        channel_logo_url = channel_info.get('channel_logo_url')
                        if channel_logo_url:
                            st.image(channel_logo_url, width=250)

                    with col2:
                        channel_title = channel_info.get('channel_title')
                        st.markdown(f"## {channel_title}")
                        st.caption("YouTube Channel Name")

                    st.markdown("---")
                    
                    col3, col4, col5 = st.columns(3)
                    
                    with col3:
                        st.metric("Total Videos", channel_info.get('video_count', 'N/A'))

                    with col4:
                        created_date = channel_info.get('channel_created_date', '')[:10]
                        st.metric("Channel Created", created_date)

                    with col5:
                        st.metric("Subscriber Count", channel_info.get('subscriber_count', 'N/A'))
                        
                    st.markdown("---")

                    # Fetch Video Stats
                    stats = get_video_stats(youtube, video_id)
                    if stats:
                        st.markdown("### Video Information")
                        col6, col7, col8 = st.columns(3)
                        
                        with col6:
                            st.metric("Total Views", stats.get("viewCount", 'N/A'))

                        with col7:
                            st.metric("Like Count", stats.get("likeCount", 'N/A'))

                        with col8:
                            st.metric("Comment Count", stats.get("commentCount", 'N/A'))
                        
                        st.markdown("---")
                        
                        # Embed Video
                        # Layout columns to center the video
                        col_left, col_center, col_right = st.columns([1, 8, 1])
                        with col_center:
                            st.video(data=youtube_link)
                
                # Sentiment Analysis
                if csv_file:
                    results = analyze_sentiment(csv_file)
                    
                    st.markdown("### Sentiment Analysis Results")
                    col9, col10, col11 = st.columns(3)
                    
                    with col9:
                        st.metric("Positive Comments", results['num_positive'])

                    with col10:
                        st.metric("Negative Comments", results['num_negative'])

                    with col11:
                        st.metric("Neutral Comments", results['num_neutral'])
                    
                    # Charts
                    st.markdown("#### Visualizations")
                    bar_chart(csv_file)
                    plot_sentiment(csv_file)
                    
                    # Channel Description
                    st.markdown("### Channel Description")
                    st.write(channel_info.get('channel_description', 'No description available.'))
            else:
                 st.error("Failed to fetch comments or save data.")

    else:
        st.error("Invalid YouTube link")
