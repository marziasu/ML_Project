import re
import pandas as pd

def preprocessor(data):
    pattern=r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[AP]M\s-\s'
    messages=re.split(pattern, data)[1:]
    dates=re.findall(pattern, data)
    df=pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date']= pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ' )
    df.rename(columns={'message_date': 'date_time'}, inplace=True )

        # separate users and message
    users=[]
    messages=[]
    for message in df['user_message']:
        entry= re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])
    df['user']= users
    df['message']= messages
    df.drop(columns=['user_message'], inplace=True )

    # extract days,month,year, time
    df['year']= df['date_time'].dt.year
    df['month']= df['date_time'].dt.month_name()
    df['month_num']=df['date_time'].dt.month
    df['day']= df['date_time'].dt.day
    df['hour']= df['date_time'].dt.hour
    df['minute']= df['date_time'].dt.minute
    df['date']= df['date_time'].dt.date
    df['day_name']= df['date_time'].dt.day_name()

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+'-'+str('00'))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1) )
        else:
            period.append(str(hour)+'-'+str(hour+1) )
    df['period']=period

    return df