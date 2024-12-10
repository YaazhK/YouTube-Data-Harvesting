import streamlit as st
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from datetime import datetime

api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyArPRfj8d8ah5Rh9BAYIR1okOSUZtHRpc8"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

def channel_data(ch_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=ch_id
        )
    response1 = request.execute()
    try:
        ch_data={
        "channel_id": ch_id,
        "channel_name":response1['items'][0]['snippet'].get('title','No Title'),
        "channel_description":response1['items'][0]['snippet'].get('description', 'NA'),
        "channel_published_at":response1['items'][0]['snippet'].get('publishedAt', 0),
        "channel_playlist_id":response1['items'][0]['contentDetails']['relatedPlaylists'].get('uploads', 0),
        "channel_subscription":response1['items'][0]['statistics'].get('subscriberCount', 0),
        "channel_views":response1['items'][0]['statistics'].get('viewCount', 0),
        }
        return ch_data
    except Exception as e:
        return "Error in API request. Please try again later."

def playlist_data(pl_id):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId= pl_id,
        maxResults=10
        )
    response2 = request.execute()

    vi_id= [item['contentDetails']['videoId'] for item in response2['items']]
    return vi_id

def video_data(vd_id):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id= vd_id
        )
    response3 = request.execute()
    vd_data={
        "video_id": vd_id,
        "video_name":response3['items'][0]['snippet'].get('title', 'No Title'),
        "video_description":response3['items'][0]['snippet'].get('description', 'No Description'),
        "video_published_at":response3['items'][0]['snippet'].get('publishedAt', 'N/A'),
        "video_duration_sec":response3['items'][0]['contentDetails'].get('duration', 'N/A'),
        "video_caption_status":response3['items'][0]['contentDetails'].get('caption', 'false'),
        "view_count":response3['items'][0]['statistics'].get('viewCount', 0),
        "like_count":response3['items'][0]['statistics'].get('likeCount', 0),
        "favorite_count":response3['items'][0]['statistics'].get('favoriteCount', 0),
        "comment_count":response3['items'][0]['statistics'].get('commentCount', 0),
        }
           
    return vd_data

def get_comment_ids(vd_id):
    comment_ids = []
    next_page_token = None

    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=vd_id,
                pageToken=next_page_token
                )
            response4 = request.execute()

            for item in response4['items']:
                if len(comment_ids)>=10:
                    break
                comment_ids.append(item['id'])

            next_page_token = response4.get('nextPageToken')
            
            if not next_page_token:
                break
    
    except HttpError as e:
        error_content = eval(e.content.decode("utf-8"))
        reason = error_content['error']['errors'][0].get('reason')
        if reason == 'commentsDisabled':
            return[]
        else:
            raise

    return comment_ids

def comment_data(cm_id):
    request = youtube.comments().list(
        part="snippet",
        id=cm_id
         )
    response5 = request.execute()

    cm_data={
        "comment_id": cm_id,
        "comment_author_name":response5['items'][0]['snippet'].get('authorDisplayName','NA'),
        "comment_text":response5['items'][0]['snippet'].get('textOriginal','NA'),
        "comment_published_at":response5['items'][0]['snippet'].get('publishedAt','NA'),
        }
           
    return cm_data

def page1():
    st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")
    st.write("An overview of key details about a YouTube channel, including  video performance, and audience insights, all in one place!")

    title = st.text_input("Enter a YouTube Channel ID")
    if title:
        intro = channel_data(title)
        if len(intro)<=30:
                st.subheader("Channel Name")
                st.write(intro["channel_name"])
                
                st.subheader("Channel Description")
                st.write(intro["channel_description"])

                st.subheader("Channel Views")
                st.write(intro["channel_views"])

                st.subheader("Channel Subscriptions")
                st.write(intro["channel_subscription"])

                st.subheader("Channel Published At")
                pb_at = datetime.strptime(intro["channel_published_at"], '%Y-%m-%dT%H:%M:%SZ')
                pub_at = pb_at.strftime('%d-%m-%Y %H:%M:%S')
                st.write(pub_at)
            
        elif intro=="Error in API request. Please try again later.":
            st.info("No data found for the provided Channel ID. Please check and try again.")
    else:
        pass

def page2():
    from mysql import connector
    connection=connector.connect(
        host="localhost",
        user="root",
        password="Yaazh@#2808MySQL",
        database="CA_P1"
    )
    cursor=connection.cursor()
    query="use CA_P1"
    cursor.execute(query)

    cursor.execute("TRUNCATE TABLE channel_info")
    cursor.execute("TRUNCATE TABLE video_info")
    cursor.execute("TRUNCATE TABLE comment_info")

    query="""
            create table if not exists channel_info
            (
            channel_id varchar(255) not null, 
            channel_name varchar(255) not null, 
            channel_description text, channel_published_at datetime,  
            channel_playlist_id varchar(255),
            channel_subscription int, channel_views int
            )"""
    cursor.execute(query)

    query="""
            create table if not exists video_info
            (
            video_id varchar(255) not null,video_name varchar(255) not null, video_description text, 
            video_published_at datetime, video_duration_sec float, video_caption_status boolean,
            view_count int, like_count int, favorite_count int, comment_count int, channel_id varchar(255)
            )
            """
    cursor.execute(query)

    query="""
            create table if not exists comment_info
            (
            comment_id varchar(255) not null, comment_author_name varchar(255), 
            comment_text text, comment_published_at datetime, video_id varchar(255)
            )
            """
    cursor.execute(query)

    connection.commit()
    
    import pandas as pd

    channel_df = pd.DataFrame()
    video_df = pd.DataFrame()
    comment_df = pd.DataFrame()

    channel_ids=['UCqM-RLkwAtT9pIU3-1zWdUw','UCi8cCe02oSGS21lHrAcjogA',
                'UC-VPf3yXgkbjH6PFKQBblYg','UC2Oq9PykS2GxW_ko2f-1PMA',
                'UCbjJZdJbaxGVW88CispTk8g','UCClfsa2ZA60lfFBSEgs2_Lg',
                'UCBriTgjiwqKKcfjOYuzO_bA','UC4f-ZK1IHG8MGZ8ch8Wp_IA',
                'UCrJNwpevlqZLVO1LW2Mo-Ag','UCcM-gKMDCINDxI4faMiVCGw',
                ]

    for ch_id in channel_ids:
        channel_info = channel_data(ch_id)
        channel_df = pd.concat([channel_df, pd.DataFrame([channel_info])])
        channel_df['channel_published_at'] = pd.to_datetime(channel_df['channel_published_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')

        playlist_id = channel_info['channel_playlist_id']
        video_ids = playlist_data(playlist_id)
        for vi_id in video_ids:
            video_info = video_data(vi_id)
            video_info['channel_id'] = ch_id
            video_df = pd.concat([video_df, pd.DataFrame([video_info])])
            video_df['video_published_at'] = pd.to_datetime(video_df['video_published_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
            
            pd.set_option('future.no_silent_downcasting', True)
            video_df['video_caption_status'] = video_df['video_caption_status'].replace({'false': 0, 'true': 1}).fillna(0).astype(int)
            
            import re
            def convert_to_seconds(duration_series):
                def parse_duration(duration):
                    if pd.isna(duration):
                        return '0'
                    
                    if not isinstance(duration, str):
                        if isinstance(duration, (int, float)):
                            return str(int(duration))
                        return '0'
                    
                    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
                    if not match:
                    # If the input is already in seconds (no PT format)
                        try:
                            return str(int(float(duration)))
                        except (ValueError, TypeError):
                            return '0'
                    
                    hours = int(match.group(1) or 0)
                    minutes = int(match.group(2) or 0)
                    seconds = int(match.group(3) or 0)
                
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    return str(total_seconds)

                result = duration_series.apply(parse_duration)
                return result
        
            video_df['video_duration_sec'] = convert_to_seconds(video_df['video_duration_sec'])

            comment_ids = get_comment_ids(vi_id)
            for cm_id in comment_ids:
                comment_info = comment_data(cm_id)
                comment_info['video_id'] = vi_id
                comment_df = pd.concat([comment_df, pd.DataFrame([comment_info])])
                comment_df['comment_published_at'] = pd.to_datetime(comment_df['comment_published_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')

    channel_df.reset_index(drop=True, inplace=True)
    video_df.reset_index(drop=True, inplace=True)
    comment_df.reset_index(drop=True, inplace=True)

    df1= channel_df
    query="insert into channel_info values(%s,%s,%s,%s,%s,%s,%s)"
    data= [tuple(data) for data in df1.values]
    cursor.executemany(query,data)

    df2= video_df
    query="insert into video_info values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data=[tuple(data) for data in df2.values]
    cursor.executemany(query,data)

    df3= comment_df
    query="insert into comment_info values(%s,%s,%s,%s,%s)"
    data=[tuple(data) for data in df3.values]
    cursor.executemany(query,data)

    st.write("Explore YouTube data through key questions provided in the dropdown below to analyze channel stats, video performance, and audience insights!")

    option = st.selectbox(
        "Select your query from the dropdown:",
        ("",
        "What are the names of all the videos and their corresponding channels?",
        "Which channels have the most number of videos, and how many videos do they have?", 
        "What are the top 10 most viewed videos and their respective channels?",
        "How many comments were made on each video, and what are their corresponding video names?",
        "Which videos have the highest number of likes, and what are their corresponding channel names?",
        "What is the total number of likes for each video, and what are their corresponding video names?", 
        "What is the total number of views for each channel, and what are their corresponding channel names?",
        "What are the names of all the channels that have published videos in the year 2022?",
        "What is the average duration of all videos in each channel, and what are their corresponding channel names?", 
        "Which videos have the highest number of comments, and what are their corresponding channel names?"),
    )

    st.write("You selected:", option)
    if option:

        if option=="What are the names of all the videos and their corresponding channels?":
            try:
                cursor = connection.cursor(buffered=True)
                query_0="""
                        select distinct video_info.video_name,channel_info.channel_name from video_info inner join
                        channel_info on video_info.channel_id=channel_info.channel_id
                        """
                cursor.execute(query_0)
                st.write(f"Your answer is:")
                for data in cursor:
                    st.write(f"Video Name: {data[0]}")
                    st.write(f"Video is from the Channel: {data[1]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="Which channels have the most number of videos, and how many videos do they have?":
            try:
                cursor = connection.cursor(buffered=True)
                query_1="""
                        select distinct channel_info.channel_name, count(video_info.video_name) as video_count from video_info 
                        inner join channel_info on video_info.channel_id = channel_info.channel_id 
                        group by channel_info.channel_name order by video_count desc
                        """
                cursor.execute(query_1)
                st.write(f"Your answer is:")
                for data in cursor:
                    st.write(f"Channel having most number of videos: {data[0]}")
                    st.write(f"The number of videos is: {data[1]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="What are the top 10 most viewed videos and their respective channels?":
            try:
                cursor = connection.cursor(buffered=True)
                query_2= """
                        select distinct video_info.video_name,channel_info.channel_name,video_info.view_count from video_info 
                        inner join channel_info on video_info.channel_id = channel_info.channel_id 
                        order by video_info.view_count desc limit 10
                        """
                cursor.execute(query_2)
                st.write(f"Your answer is:")
                st.write(f"Top 10 most viewed videos:\n")
                for data in cursor:
                    st.write(f"Video Name: {data[0]}")
                    st.write(f"Channel Name: {data[1]}")
                    st.write(f"View Count: {data[2]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="How many comments were made on each video, and what are their corresponding video names?":
            try:
                cursor = connection.cursor(buffered=True)
                query_3="select distinct video_name,comment_count from video_info"
                cursor.execute(query_3)
                st.write(f"Your answer is:")
                st.write(f"Number of comments for each video of the channel:\n")
                for data in cursor:
                    st.write(f"Video Name: {data[0]}")
                    st.write(f"Comment Count for the video: {data[1]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="Which videos have the highest number of likes, and what are their corresponding channel names?":
            try:
                cursor = connection.cursor(buffered=True)
                query_4="""
                        select distinct video_info.video_name, channel_info.channel_name, video_info.like_count 
                        from video_info inner join channel_info on video_info.channel_id = channel_info.channel_id
                        order by video_info.like_count desc limit 10
                        """
                cursor.execute(query_4)
                st.write(f"Your answer is:")
                st.write("Top 10 videos with the highest number of Likes and their Channels:\n")
                for data in cursor:
                    st.write(f"Video Name: {data[0]}")
                    st.write(f"Channel Name: {data[1]}")
                    st.write(f"Likes: {data[2]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="What is the total number of likes for each video, and what are their corresponding video names?":
            try:
                cursor = connection.cursor(buffered=True)
                query_5="select distinct video_name, like_count from video_info"
                cursor.execute(query_5)
                st.write(f"Your answer is:")
                st.write(f"Number of likes for each video of the channel:")
                for data in cursor:
                    st.write(f"Video Name: {data[0]}")
                    st.write(f"Like Count for the video: {data[1]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="What is the total number of views for each channel, and what are their corresponding channel names?":
            try:
                cursor = connection.cursor(buffered=True)
                query_6="select distinct channel_name,channel_views from channel_info"
                cursor.execute(query_6)
                st.write(f"Your answer is:")
                for data in cursor:
                    st.write(f"Channel Name: {data[0]}")
                    st.write(f"View Count for the channel: {data[1]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="What are the names of all the channels that have published videos in the year 2022?":
            try:
                cursor = connection.cursor(buffered=True)
                query_7 = """
                    select distinct channel_info.channel_name from video_info inner join channel_info 
                    on video_info.channel_id = channel_info.channel_id where year(video_info.video_published_at) = 2022
                    """
                cursor.execute(query_7)
                st.write(f"Your answer is:")
                st.write("Name of Channels that published videos in the year 2022:\n")
                for data in cursor:
                    st.write(f"Channel Name: {data[0]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="What is the average duration of all videos in each channel, and what are their corresponding channel names?":
            try:
                cursor = connection.cursor(buffered=True)
                query_8 = """
                        select distinct channel_info.channel_name, avg(video_info.video_duration_sec) as avg_video_duration_sec 
                        from video_info inner join channel_info on video_info.channel_id = channel_info.channel_id 
                        group by channel_info.channel_name
                        """
                cursor.execute(query_8)
                st.write(f"Your answer is:")
                st.write("Average Video Duration for Each Channel:\n")
                for data in cursor:
                    st.write(f"Channel Name: {data[0]}")
                    st.write(f"Average Duration (seconds): {data[1]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        elif option=="Which videos have the highest number of comments, and what are their corresponding channel names?":
            try:
                cursor = connection.cursor(buffered=True)
                query_9 = """
                        select distinct video_info.video_name, channel_info.channel_name, video_info.comment_count 
                        from video_info inner join channel_info on video_info.channel_id = channel_info.channel_id 
                        order by video_info.comment_count desc limit 5
                        """
                cursor.execute(query_9)
                st.write(f"Your answer is:")
                st.write("Top 5 Videos with the Highest Number of Comments:\n")
                for data in cursor:
                    st.write(f"Video Name: {data[0]}")
                    st.write(f"Channel Name: {data[1]}")
                    st.write(f"Number of Comments: {data[2]}")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.write("No data found.")
    else:
        pass
    
    cursor.close()
    connection.close()

pages = ["About", "Query"]
pg = st.sidebar.radio("", pages)

if pg == "About":
    page1()
elif pg == "Query":
    page2()