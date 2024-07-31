import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file= st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    byte_data= uploaded_file.getvalue()
    data=byte_data.decode('utf-8')
    df=preprocessor.preprocessor(data)

    user_list= df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user= st.sidebar.selectbox("Show analysis wrt.", user_list)

    if st.sidebar.button('Show analysis'):
        # Statistics
        num_msg, num_words,num_media, num_links= helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4= st.columns(4)
        with col1:
            st.subheader("Total Messages")
            st.title(num_msg)
        with col2:
            st.subheader("Total Word")
            st.title(num_words)
        with col3:
            st.subheader("Total Media Shared")
            st.title(num_media)
        with col4:
            st.subheader("Total Links Shared")
            st.title(num_links)
        
        # monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user, df)
        fig, ax=plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title('Daily Timeline')
        daily_timeline=helper.daily_timeline(selected_user, df)
        fig, ax= plt.subplots()
        ax.plot( daily_timeline['date'], daily_timeline['message'] )
        plt.xticks(rotation='vertical' )
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2= st.columns(2)
        with col1:
            st.header('Most busy day')
            busy_day= helper.week_activity_map(selected_user, df)
            fig, ax= plt.subplots()
            ax.bar(busy_day.index, busy_day.values )
            plt.xticks(rotation='vertical' )

            st.pyplot(fig)
        with col2:
            st.header('Most busy month')
            busy_month= helper.month_activity_map(selected_user, df)
            fig, ax= plt.subplots()
            ax.bar(busy_month.index, busy_month.values , color='orange')
            plt.xticks(rotation='vertical' )

            st.pyplot(fig)

        # acitvity heatmap
        st.header('Weekly Activity Map')
        user_heatmap= helper.activity_heatmap(selected_user, df)
        fig, ax= plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the most active user in the group (Group level)
        if selected_user=='Overall':
            st.title('Most Active Users')
            x,new_df = helper.most_active_user(df)
            fig, ax= plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        
        # WordCloud
        st.title("WordCloud")
        wc_df= helper.create_wordcloud(selected_user, df)
        fig, ax= plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)

        # most common word
        st.title('MOst Common Word')
        common_word_df= helper.most_common_word(selected_user, df)
        fig, ax= plt.subplots()
        ax.barh(common_word_df[0], common_word_df[1])
        st.pyplot(fig)