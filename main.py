from class_analyzer import Analyzer
from class_streamer import Streamer

keyword_to_find = input("Introduzca una palabra, hashtag o frase: ");

my_streamer = Streamer();
tweets_list = my_streamer.find_keyword(keyword_to_find);

my_analyzer = Analyzer();
tw_dataframe = my_analyzer.tweets_dataframe(tweets_list);
my_analyzer.tweets_timeline(tw_dataframe);
my_analyzer.likes_retweets_timeline(tw_dataframe);
my_analyzer.hashtag_cloud();
my_analyzer.keywords_cloud();
my_analyzer.sentiment_plot();