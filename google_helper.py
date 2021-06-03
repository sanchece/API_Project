
from google.cloud import language_v1
from statistics import mean
def google_sentiment_analysis(tweet):
    text=tweet
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment

def get_focus_sentiment(sentiments):
    # currently working on better algorithm to extract focus sentiment from extracted tweets
    focus_sentiment=mean(sentiments)
    return focus_sentiment