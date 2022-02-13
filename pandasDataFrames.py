import json, requests, xmltodict, pandas as pd

def refresh_XmlToPkl_Channel(FreeFeedURL):
    #Pull XML --> Transform into json --> 
    response = requests.get(FreeFeedURL)
    json_data = json.loads(json.dumps(xmltodict.parse(response.content)))
    #Save Channel list as xml_channel.pkl
    df_channel = pd.json_normalize(json_data["rss"]["channel"]).drop(['item', ], axis=1)
    df_channel = pd.DataFrame(df_channel.to_dict(orient='records'))
    df_channel.to_pickle("pkl/xml_channel.pkl")
    return df_channel

def refresh_XmlToPkl_Podcast(FreeFeedURL):
    #Pull XML --> Transform into json --> 
    response = requests.get(FreeFeedURL)
    json_data = json.loads(json.dumps(xmltodict.parse(response.content)))
    #Save podcast list as xml_podcast.pkl
    df_item = pd.json_normalize(json_data["rss"]["channel"], 'item')
    df_item = pd.DataFrame(df_item.to_dict(orient='records'))
    df_item.to_pickle("pkl/xml_podcast.pkl")
    return df_item

def refresh_XmlToPkl_All(FreeFeedURL):
    df_item     = refresh_XmlToPkl_Podcast(FreeFeedURL)
    df_channel  = refresh_XmlToPkl_Channel(FreeFeedURL)
    return df_channel, df_item

def refresh_FirebaseToPkl_Channel(store):
    # Save channel df as a pickle
    channel = store.collection(u'channel').stream()
    channel_df = list(map(lambda x: x.to_dict(), channel))
    cdf = pd.DataFrame(channel_df)
    cdf.to_pickle("pkl/firebase_channel.pkl")
    return cdf

def refresh_FirebaseToPkl_Podcast(store):
    # Save podcast df as a pickle
    podcast_stream = store.collection(u'item').stream()
    podCount = 0
    for podcast in podcast_stream:
        df   = pd.DataFrame([podcast.to_dict()])
        curEpId         = podcast.id
        if podCount == 0:
            # If 1st episode in stream, make dataframe
            pdf = pd.DataFrame(df)
            pdf.insert(0, 'podcastEpisodeId', curEpId)
            podCount += 1
            continue
        # If >0st episode in stream, append to dataframe
        pdf2 = pd.DataFrame(df)
        pdf2.insert(0, 'podcastEpisodeId', curEpId)
        pdf = pdf.append(pdf2, ignore_index=True)
    # podcasts_df = list(map(lambda x: x.to_dict(), podcast_stream))
    # pdf = pd.DataFrame(podcasts_df)
    pdf.to_pickle("pkl/firebase_podcast.pkl")
    return pdf

def refresh_FirebaseToPkl_Transcript(store):
    # Get Episode Transcripts into ONE DATAFRAME from FireStore  
    podcast_stream = store.collection(u'item').stream()
    podCount = 0
    for podcast in podcast_stream:
        curEpId = podcast.id
        transcript_stream = store.collection(u'item').document(curEpId).collection(u'transcript').stream()
        transcript_df = list(map(lambda x: x.to_dict(), transcript_stream))
        if podCount == 0:
            # If 0st episode in stream, make dataframe
            tdf = pd.DataFrame(transcript_df)
            tdf.insert(0, 'podcastEpisodeId', curEpId)
            podCount += 1
            continue
        # If >0st episode in stream, append to dataframe
        tdf2 = pd.DataFrame(transcript_df)
        tdf2.insert(0, 'podcastEpisodeId', curEpId)
        tdf = tdf.append(tdf2, ignore_index=True)
    # Save transcript df as pickle
    tdf.to_pickle("pkl/firebase_transcript.pkl")
    return tdf

def refresh_FirebaseToPkl_All(store):
    cdf = refresh_FirebaseToPkl_Channel(store)
    pdf = refresh_FirebaseToPkl_Podcast(store)
    tdf = refresh_FirebaseToPkl_Transcript(store)
    return cdf, pdf, tdf

def pklToDataFrame():
    df_xml_channel = pd.read_pickle('pkl/xml_channel.pkl')
    df_xml_podcast = pd.read_pickle('pkl/xml_podcast.pkl')
    df_firebase_channel = pd.read_pickle('pkl/firebase_channel.pkl')
    df_firebase_podcast = pd.read_pickle('pkl/firebase_podcast.pkl')
    df_firebase_transcript = pd.read_pickle('pkl/firebase_transcript.pkl')
    return df_xml_channel, df_xml_podcast, df_firebase_channel, df_firebase_podcast, df_firebase_transcript

def podcasts_XmlToFireBase_WhereMissing(xmldf, pdf, FreeFeedURL = None, store = None):
    if FreeFeedURL is not None and store is not None:
        xmldf   = refresh_XmlToPkl_Podcast(FreeFeedURL)
        pdf     = refresh_FirebaseToPkl_Podcast(store)
    else:
        xmldf   = pd.read_pickle('pkl/xml_podcast.pkl')
        pdf     = pd.read_pickle('pkl/firebase_podcast.pkl') 
    cdf = pd.merge(xmldf, pdf['title'], on='title', how="outer", indicator=True).query('_merge=="left_only"').drop(columns=['_merge'])
    return cdf

def podcasts_WhereTranscriptMissing(store, refresh = 1):
    if refresh == 1:    
        pdf = refresh_FirebaseToPkl_Podcast(store)
        tdf = refresh_FirebaseToPkl_Transcript(store)
    else: 
        pdf = pd.read_pickle('pkl/firebase_podcast.pkl')
        tdf = pd.read_pickle('pkl/firebase_transcript.pkl')
    cdf = pd.merge(pdf, tdf['podcastEpisodeId'], on='podcastEpisodeId', how="outer", indicator=True).query('_merge=="left_only"').drop(columns=['_merge'])
    return cdf