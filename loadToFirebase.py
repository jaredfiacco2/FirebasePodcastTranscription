import firebase_admin
from firebase_admin import credentials, firestore
from pandasDataFrames import refresh_XmlToPkl_All, refresh_FirebaseToPkl_All, refresh_FirebaseToPkl_Transcript, podcasts_XmlToFireBase_WhereMissing, podcasts_WhereTranscriptMissing
from firebaseAddPodcastTranscripts import transcribeNewPodcasts

#firebase setup
cred = credentials.Certificate("darknetdiaries-firebase-adminsdk-cmlo5-0476cd885a.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()

#Pull Current XML --> Transform into json --> Pass df back --> Save pkl copy
FreeFeedURL = "https://darknetdiaries.com/feedfree.xml"
df_xml_channel, df_xml_podcast = refresh_XmlToPkl_All(FreeFeedURL)

#Pull Current FireStore --> Pass df back --> Save pkl copy
df_firestore_channel, df_firestore_podcasts, df_firestore_transcript = refresh_FirebaseToPkl_All(store)

#Identify New Podcasts, add them to Firestore if exists
df_missing_podcasts = podcasts_XmlToFireBase_WhereMissing( df_xml_podcast, df_firestore_podcasts, FreeFeedURL, store)
if not df_missing_podcasts.empty:
    doc_ref_item = store.collection(u'item')
    podcast_item= df_missing_podcasts.to_dict(orient='records')
    list(map(lambda x: doc_ref_item.add(x), podcast_item))

#Identify Untranscribed Podcasts, transcribe them, add them to Firestore if exists
df_missing_podcasts = podcasts_WhereTranscriptMissing(store, 1)
if len(df_missing_podcasts.index) > 2:
    transcribeNewPodcasts(store)
refresh_FirebaseToPkl_Transcript(store)

#Done!
print('Complete!')


# #Pull Local Pickles --> Pass df back
# from pandasDataFrames import pklToDataFrame 
# df_xml_channel, df_xml_podcast, df_firestore_channel, df_firestore_podcasts, df_firestore_transcript = pklToDataFrame()

# # Truncate top 500 in collection before filling it 
#from truncateFirebase import delete_collection
# delete_collection(doc_ref_channel, 500)
# delete_collection(doc_ref_item, 500)