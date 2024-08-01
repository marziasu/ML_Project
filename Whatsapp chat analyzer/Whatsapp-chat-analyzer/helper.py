from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

extractor= URLExtract()
wc=WordCloud(width=800, height=400,font_path='kalpurush.ttf')


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df= df[df['user']==selected_user]
    # 1. fetch total number of messages
    num_msg= df.shape[0]

    # 2. fetch total number of words
    words=[]
    for message in df['message']:
        words.extend( message.split() )

    # 3. fetch number of media message
    num_media_msg=df[df['message']=='<Media omitted>\n'].shape[0]

    # 4. fetch number of links shared
    links=[]
    for msg in df['message']:
        links.extend( extractor.find_urls(msg) )   
    
    return num_msg,len(words), num_media_msg, len(links)

    
def most_active_user(df):
    x= df['user'].value_counts().head()
    new_df=round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x, new_df

def create_wordcloud(selected_user, df):
    if selected_user!= 'Overall':
        df= df[df['user']==selected_user]

    f=open('banglish stopwords.txt','r', encoding='utf-8')
    stop_words=f.read()

    temp= df[df['user']!='group notification']
    temp= temp[temp['message']!= '<Media omitted>\n' ]
    temp= temp[ temp['message']!='Missed video call\n']
    temp= temp[ temp['message']!='Missed voice call\n']
    temp= temp[ temp['message']!='null\n']
    def remove_stop_words(messages):
        y=[]
        for word in messages.lower().split():    
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message']=temp['message'].apply(remove_stop_words)
    wc_df= wc.generate(temp['message'].str.cat(sep=' '))

    return wc_df

def most_common_word(selected_user, df):
    f=open('banglish stopwords.txt','r', encoding='utf-8')
    stop_words=f.read()

    temp= df[df['user']!='group notification']
    temp= temp[temp['message']!= '<Media omitted>\n' ]
    temp= temp[ temp['message']!='Missed video call\n']
    temp= temp[ temp['message']!='Missed voice call\n']
    temp= temp[ temp['message']!='null\n']
    words=[]
    for msg in temp['message']:
        for word in msg.lower().split():    
            if word not in stop_words:
                words.append(word)

    common_word_df= pd.DataFrame( Counter(words).most_common(20) )
    return common_word_df

def monthly_timeline(selected_user, df):
    if selected_user!= 'Overall':
        df= df[df['user']==selected_user]

    timeline= df.groupby(['year', 'month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]) )
    timeline['time']=time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user!= 'Overall':
        df= df[df['user']==selected_user]
    daily_timeline= df.groupby( df['date'] ).count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    busy_day=df['day_name'].value_counts()

    return busy_day

def month_activity_map(selected_user, df):
    busy_month=df['month'].value_counts()

    return busy_month

def activity_heatmap(selected_user, df):
    user_heatmap= df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
