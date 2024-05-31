import googleapiclient.discovery
import pymongo
import psycopg2
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image



#API Key connection 

api_service_name = "youtube"
api_version = "v3"

api_key = "AIzaSyD4mx1WEjal93AwxSOjyXUwOenrA_8d6KE"

youtube = googleapiclient.discovery.build( api_service_name, api_version, developerKey=api_key)



#Channel Information 

def channel_Data(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    data = {
        'channel_name':response['items'][0]['snippet']['title'],
        'channel_des':response['items'][0]['snippet']['description'],
        'channel_pat':response['items'][0]['snippet']['publishedAt'],
        'channel_pid':response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        'channel_sub':response['items'][0]['statistics']['subscriberCount'],
        'channel_vc':response['items'][0]['statistics']['videoCount'],
        'channel_vic':response['items'][0]['statistics']['viewCount'],
        'channel_id':response['items'][0]['id']
    }
    return data


#Get video ids

def get_videos_ids(channel_id):
    video_ids=[]
    request = youtube.channels().list(
                id=channel_id,
                part='contentDetails'
            ) 
    response = request.execute()

    Playlist_Id= response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token=None

    while True:

        request1 = youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=Playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_token)
        response1 = request1.execute()

        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')

        if next_page_token is None:
                    break
    return video_ids



#Video Information
def get_video_info(video_ids):
    video_data=[]
    for video_id in video_ids:
        request=youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id 
        )
        response=request.execute()

        for item in response["items"]:
                data=dict(Channel_Name=item['snippet']['channelTitle'],
                        Channel_id=item['snippet']['channelId'],
                        Video_Id=item['id'],
                        Title=item['snippet']['title'],
                        Tags=item['snippet'].get('tags'),
                        Thumbnail=item['snippet']['thumbnails']['default']['url'],
                        Description=item['snippet'].get('description'),
                        Published_Date=item['snippet']['publishedAt'],
                        Duration=item['contentDetails']['duration'],
                        Views=item['statistics'].get('viewCount'),
                        Likes=item['statistics'].get('likeCount'),
                        Comments=item['statistics'].get('commentCount'),
                        Favourite_Count=item['statistics']['favoriteCount'],
                        Definition=item['contentDetails']['definition'],
                        Caption_status=item['contentDetails']['caption']
                        )
                video_data.append(data)
    return video_data  
        


#Comment Information
def get_comment_info(video_ids):
    Comment_data=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            response=request.execute()

            for item in response['items']:
                data=dict(Comment_Id=item['snippet']['topLevelComment']['id'],
                        Video_Id=item['snippet']['topLevelComment']['snippet']['videoId'],
                        Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        Comment_Published=item['snippet']['topLevelComment']['snippet']['publishedAt'])
                
                Comment_data.append(data)
                
    except:
        pass
    return Comment_data  





#Playlist Information
def get_playlist_info(channel_id):
        next_page_token=None
        Playlist_data=[]
        while True:
                request=youtube.playlists().list(
                        part='snippet,contentDetails',
                        channelId=channel_id,
                        maxResults=50,
                        pageToken=next_page_token
                        )
                response=request.execute()

                for item in response['items']:
                        data=dict(Playlist_Id=item['id'],
                                Title=item['snippet']['title'],
                                Channel_Id=item['snippet']['channelId'],
                                Channel_Name=item['snippet']['channelTitle'],
                                Published_At=item['snippet']['publishedAt'],
                                Video_Count=item['contentDetails']['itemCount'])
                        Playlist_data.append(data)
        
                next_page_token=response.get('nextPageToken')
                if next_page_token is None:
                        break
        return Playlist_data
    


#upload mongoDB

client=pymongo.MongoClient("mongodb+srv://rsaakash2000:akashof10th@cluster0.1hsfxn2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client["Youtube_data"]



def channel_details(channel_id):
    ch_details=channel_Data(channel_id)
    pl_Details=get_playlist_info(channel_id)
    vi_ids=get_videos_ids(channel_id)
    vi_details=get_video_info(vi_ids)
    com_details=get_comment_info(vi_ids)

    coll1=db["channel_details"]
    coll1.insert_one({"channel_information":ch_details,
                    "playlist_information":pl_Details,
                    "video_information":vi_details,
                    "comment_information":com_details})

    return "upload completed successfully" 


#table creation for channels,playlists,videos,comments

def channels_table(channel_name_single):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rsaakash",
                        database="youtube_data",
                        port="5432")
    cursor=mydb.cursor()


    
    create_query='''create table if not exists channels(channel_name varchar(100),
                                                    channel_id varchar(80) primary key,
                                                    channel_sub bigint,
                                                    channel_vic bigint,
                                                    channel_vc int,
                                                    channel_des text,
                                                    channel_pid varchar(80))'''
    cursor.execute(create_query)
    mydb.commit()

    


    single_channel_detail=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({"channel_information.channel_name":channel_name_single},{"_id":0}):
        single_channel_detail.append(ch_data["channel_information"])
        
    df_single_channel_detail=pd.DataFrame(single_channel_detail)    


    for index,row in df_single_channel_detail.iterrows():
        insert_query='''insert into channels(channel_name,
                                            channel_id,
                                            channel_sub,
                                            channel_vic,
                                            channel_vc,
                                            channel_des,
                                            channel_pid)
                                            
                                            values(%s,%s,%s,%s,%s,%s,%s)'''
        values=(row['channel_name'],
                row['channel_id'],
                row['channel_sub'],
                row['channel_vic'],
                row['channel_vc'],
                row['channel_des'],
                row['channel_pid'])
        
        try:
             
            cursor.execute(insert_query,values)
            mydb.commit()

        except:

            news= f"Your Provided Channel Name {channel_name_single} Already Exists"

            return news

        




def playlist_table(channel_name_single):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rsaakash",
                        database="youtube_data",
                        port="5432")
    cursor=mydb.cursor()

    

    create_query='''create table if not exists playlists(Playlist_Id varchar(100) primary key,
                                                        Title varchar(100),
                                                        Channel_Id varchar(100),
                                                        Channel_Name varchar(100),
                                                        Published_At timestamp,
                                                        Video_Count int)'''

    cursor.execute(create_query)
    mydb.commit()


    single_playlist_details=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({"channel_information.channel_name":channel_name_single},{"_id":0}):
        single_playlist_details.append(ch_data["playlist_information"]) 

    df_single_playlist_details= pd.DataFrame(single_playlist_details[0])


    for index,row in df_single_playlist_details.iterrows():
        insert_query='''insert into playlists(Playlist_Id,
                                              Title,
                                              Channel_Id,
                                              Channel_Name,
                                              Published_At,
                                              Video_Count)
                                              values(%s,%s,%s,%s,%s,%s)'''
        values=(row['Playlist_Id'],
                row['Title'],
                row['Channel_Id'],
                row['Channel_Name'],
                row['Published_At'],
                row['Video_Count'])
        
        
        cursor.execute(insert_query,values)
        mydb.commit()



def videos_table(channel_name_single):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rsaakash",
                        database="youtube_data",
                        port="5432")
    cursor=mydb.cursor()

    

    create_query='''create table if not exists videos(Channel_Name varchar(100),
                                                    Channel_id varchar(100),
                                                    Video_Id varchar(30) primary key,
                                                    Title varchar(100),
                                                    Tags text,
                                                    Thumbnail varchar(200),
                                                    Description text,
                                                    Published_Date timestamp,
                                                    Duration interval,
                                                    Views bigint,
                                                    Likes bigint,
                                                    Comments int,
                                                    Favourite_Count int,
                                                    Definition varchar(10),
                                                    Caption_status varchar(50))'''

    cursor.execute(create_query)
    mydb.commit()


    single_videos_details=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({"channel_information.channel_name":channel_name_single},{"_id":0}):
        single_videos_details.append(ch_data["video_information"])

    df_single_videos_details= pd.DataFrame(single_videos_details[0])



    for index,row in df_single_videos_details.iterrows():
        insert_query='''insert into videos(Channel_Name,
                                                Channel_id,
                                                Video_Id,
                                                Title,
                                                Tags,
                                                Thumbnail,
                                                Description,
                                                Published_Date,
                                                Duration,
                                                Views,
                                                Likes,
                                                Comments,
                                                Favourite_Count,
                                                Definition,
                                                Caption_status
                                                )

                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        
        values=(row['Channel_Name'],
        row['Channel_id'],
        row['Video_Id'],
        row['Title'],
        row['Tags'],
        row['Thumbnail'],
        row['Description'],
        row['Published_Date'],
        row['Duration'],
        row['Views'],
        row['Likes'],
        row['Comments'],
        row['Favourite_Count'],
        row['Definition'],
        row['Caption_status'])
        
        
        cursor.execute(insert_query,values)
        mydb.commit()




def comments_table(channel_name_single):
        mydb=psycopg2.connect(host="localhost",
                                user="postgres",
                                password="rsaakash",
                                database="youtube_data",
                                port="5432")
        cursor=mydb.cursor()


        create_query='''create table if not exists comments(Comment_Id varchar(100) primary key,
                                                                Video_Id varchar(50),
                                                                Comment_Text text,
                                                                Comment_Author varchar(150),
                                                                Comment_Published timestamp)'''

        cursor.execute(create_query)
        mydb.commit()

        single_comments_details=[]
        db=client["Youtube_data"]
        coll1=db["channel_details"]
        for ch_data in coll1.find({"channel_information.channel_name":channel_name_single},{"_id":0}):
                single_comments_details.append(ch_data["comment_information"])
        
        df_single_comments_details= pd.DataFrame(single_comments_details[0])


        for index,row in df_single_comments_details.iterrows():
                insert_query='''insert into comments(Comment_Id,
                                                        Video_Id,
                                                        Comment_Text,
                                                        Comment_Author,
                                                        Comment_Published
                                                        )
                                                values(%s,%s,%s,%s,%s)'''
        
        
                values=(row['Comment_Id'],
                        row['Video_Id'],
                        row['Comment_Text'],
                        row['Comment_Author'],
                        row['Comment_Published']
                        )
                cursor.execute(insert_query,values)
                mydb.commit()
    


def tables(single_channel):

    news= channels_table(single_channel)
    if news:
        return news
    
    else:

        playlist_table(single_channel)
        videos_table(single_channel)
        comments_table(single_channel)

        return "Tables Created Successfully"



def show_channels_table():
    ch_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data['channel_information'])
    df=st.dataframe(ch_list) 

    return df  





def show_playlists_table():
    pl_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
        for i in range(len(pl_data['playlist_information'])):
            pl_list.append(pl_data['playlist_information'][i])
    df1=st.dataframe(pl_list)

    return df1





def show_videos_table():
    vi_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for vi_data in coll1.find({},{"_id":0,"video_information":1}):
        for i in range(len(vi_data['video_information'])):
            vi_list.append(vi_data['video_information'][i])
    df2=st.dataframe(vi_list) 

    return df2





def show_comments_table():
    com_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for com_data in coll1.find({},{"_id":0,"comment_information":1}):
           for i in range(len(com_data['comment_information'])):
               com_list.append(com_data['comment_information'][i])
    df3=st.dataframe(com_list)

    return df3



#streamlit 


st.set_page_config(layout="wide")
st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")

# Apply custom CSS for sidebar and other components
st.markdown(
    """
    <style>
    /* Sidebar */
    [data-testid="stSidebar"]{
        background-color: #ffffff; /* White sidebar background */
        color: white;
    }
    
    /* Label */
    div[data-testid="stTextInput"]>label {
        color: #000000 !important; /* Custom color for the label */
    }

    /* Main content */
    .stApp {
        background-color: #C0C0C0!important; /* Silver background color */
        color: #333333; /* Dark Gray text color */
    }
    
    /* Headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #000000; /* Black header color */
    }

    .stRadio>label {
    color: #000000 !important; /* Custom color for radio button header */
    }
    
    .stSelectbox>label {
    color: #000000 !important; /* Custom color for selectbox header */
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3498DB; /* Light Blue button color */
        color: white; /* White button text color */
    }

    /* Label for "CHANNELS" */
    #channels_label {
        color: #000000 !important; /* Custom color for the label */
    }

    /* Label for "PLAYLISTS" */
    #playlists_label {
        color: #000000 !important; /* Custom color for the label */
    }

    /* Label for "VIDEOS" */
    #videos_label {
        color: #000000 !important; /* Custom color for the label */
    }

    /* Label for "COMMENTS" */
    #comments_label {
        color: #000000 !important; /* Custom color for the label */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar configuration
with st.sidebar:
    st.sidebar.image('image.png', use_column_width=True)
    selected = option_menu("Skills Takeaway From This Project",
                        ["Python Scripting","Data Collection",'MongoDB',"API Integration","Data Management using SQL"],
                        icons=["code","database","database","plug","filetype-sql"],
                        menu_icon="menu-up",
                        orientation="vertical")

# Main content configuration
channel_id = st.text_input("Enter the channel ID")

# Define coll1 outside the sidebar block
db = client["Youtube_data"]
coll1 = db["channel_details"]

if st.button("Collect and Store Data"):
    ch_ids = []
    for ch_data in coll1.find({}, {"_id": 0, "channel_information": 1}):
        ch_ids.append(ch_data['channel_information']["channel_id"])
    if channel_id in ch_ids:
        st.warning("Channel details of the given channel ID already exist.")
    else:
        insert = channel_details(channel_id)
        st.success("Channel details successfully stored.")

All_channels = [ch_data["channel_information"]["channel_name"] for ch_data in coll1.find({}, {"_id": 0, "channel_information": 1})]
unique_channel = st.selectbox("Select the channel", All_channels)

if st.button("Migrate to SQL"):
    Table = tables(unique_channel)
    st.success("Migration to SQL completed successfully.")

show_table = st.radio("Select the table for view", ("CHANNELS", "PLAYLISTS", "VIDEOS", "COMMENTS"))
if show_table == "CHANNELS":
    st.markdown('<label id="channels_label">CHANNELS</label>', unsafe_allow_html=True)
    show_channels_table()
elif show_table == "PLAYLISTS":
    st.markdown('<label id="playlists_label">PLAYLISTS</label>', unsafe_allow_html=True)
    show_playlists_table()
elif show_table == "VIDEOS":
    st.markdown('<label id="videos_label">VIDEOS</label>', unsafe_allow_html=True)
    show_videos_table()
elif show_table == "COMMENTS":
    st.markdown('<label id="comments_label">COMMENTS</label>', unsafe_allow_html=True)
    show_comments_table()

#SQL Connection:

mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rsaakash",
                        database="youtube_data",
                        port="5432")
cursor=mydb.cursor()

question=st.selectbox("Select your question",("1. What are the names of all the videos and their corresponding channels?",
                                              "2. Which channels have the most number of videos, and how many videos do they have",
                                              "3. What are the top 10 most viewed videos and their respective channels?",
                                              "4. How many comments were made on each video, and what are their corresponding video names?",
                                              "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                                              "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                              "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                                              "8. What are the names of all the channels that have published videos in the year 2022?",
                                              "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                              "10. Which videos have the highest number of comments, and what are their corresponding channel names?"))

if question=="1. What are the names of all the videos and their corresponding channels?":
    query1='''select title as videos,channel_name as channelname 
              from videos'''
    cursor.execute(query1)
    mydb.commit()
    t1=cursor.fetchall()
    df=pd.DataFrame(t1,columns=["video title","channel name"])
    st.write(df)

elif question=="2. Which channels have the most number of videos, and how many videos do they have":
    query2='''select channel_name as channelname,channel_vic as no_videos
              from channels
              order by channel_vic desc'''
    cursor.execute(query2)
    mydb.commit()
    t2=cursor.fetchall()
    df2=pd.DataFrame(t2,columns=["channel name","No of videos"])
    st.write(df2)

elif question=="3. What are the top 10 most viewed videos and their respective channels?":
    query3='''select views as views,channel_name as channelname,title as videotitle 
              from videos
              where views is not null 
              order by views desc limit 10'''
    cursor.execute(query3)
    mydb.commit()
    t3=cursor.fetchall()
    df3=pd.DataFrame(t3,columns=["views","channel name","videotitle"])
    st.write(df3)

elif question=="4. How many comments were made on each video, and what are their corresponding video names?":
    query4='''select comments as no_comments,title as videotitle
              from videos
              where comments is not null '''
    cursor.execute(query4)
    mydb.commit()
    t4=cursor.fetchall()
    df4=pd.DataFrame(t4,columns=["no of comments","videotitle"])
    st.write(df4)

elif question=="5. Which videos have the highest number of likes, and what are their corresponding channel names?":
    query5='''select title as videotitle,channel_name as channelname,likes as likecount
              from videos
              where likes is not null
              order by likes desc'''
    cursor.execute(query5)
    mydb.commit()
    t5=cursor.fetchall()
    df5=pd.DataFrame(t5,columns=["video title","channel name","like count"])
    st.write(df5)

elif question=="6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
    query6='''select likes as likecount 
              from videos'''
    cursor.execute(query6)
    mydb.commit()
    t6=cursor.fetchall()
    df6=pd.DataFrame(t6,columns=["like count"])
    st.write(df6)
    

elif question=="7. What is the total number of views for each channel, and what are their corresponding channel names?":
    query7='''select channel_name as channelname, channel_vic as totalviews
              from channels'''
    cursor.execute(query7)
    mydb.commit()
    t7=cursor.fetchall()
    df7=pd.DataFrame(t7,columns=["channelname","totalviews"])
    st.write(df7)

elif question=="8. What are the names of all the channels that have published videos in the year 2022?":
    query8='''select title as video_title, published_date as publisheddate,channel_name as channelname
              from videos
              where extract(year from published_date)=2022'''
    cursor.execute(query8)
    mydb.commit()
    t8=cursor.fetchall()
    df8=pd.DataFrame(t8,columns=["videotitle","published_date","channelname"])
    st.write(df8)

elif question=="9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    query9='''select channel_name as channelname,AVG(duration) as averageduration
              from videos
              group by channel_name'''
    cursor.execute(query9)
    mydb.commit()
    t9=cursor.fetchall()
    df9=pd.DataFrame(t9,columns=["channelname","averageduration"])

    T9=[]
    for index,row in df9.iterrows():
        channel_title=row["channelname"]
        average_duration=row["averageduration"]
        average_duration_str=str(average_duration)
        T9.append(dict(channeltitle=channel_title,avgduration=average_duration_str))
    df1=pd.DataFrame(T9)
    st.write(df1)


elif question=="10. Which videos have the highest number of comments, and what are their corresponding channel names?":
    query10='''select title as videotitle,channel_name as channelname,comments as comments
               from videos
               where comments is not null 
               order by comments desc'''
    cursor.execute(query10)
    mydb.commit()
    t10=cursor.fetchall()
    df10=pd.DataFrame(t10,columns=["video title","channel name","comments"])
    st.write(df10)
