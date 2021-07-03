import matplotlib.pyplot as pyplot
import nltk
import pandas
import re
from textblob import TextBlob
from wordcloud import WordCloud

class Analyzer:
    """
    This class offers different possibilities for data processing and analysis.
    """

    def clean_line_feeds(self, text):
        text = text.replace("\n", " ");
        return text
    
    def clean_text_for_sentiment(self, text):
        """This function uses regular expresions to remove hashtags, links, @ mentions and 'RT '..."""

        text = re.sub(r'#[A-Za-z0-9]+', "", text);
        text = re.sub(r'@[A-Za-z0-9_:]+', "", text);
        text = re.sub(r'http[a-zA-Z0-9://\\._@]*', "", text);
        text = re.sub(r'^RT[\s]+', "", text);
        text = re.sub(r'[\'‘’\"\[\](){}]', "", text);

        return text;
    
    def clean_text_for_tagcloud(self, text):
        """This function uses regular expresions to remove hashtags, links, 'RT '..., and any non word character.
        But keeps @ mentions ().
        Also converts the whole text to lower case and uses nltk.corpus to remove stop_words.
        """
        text = re.sub(r'#[A-Za-z0-9ñÑáéíóúÁÉÍÓÚ]+', "", text);
        text = re.sub(r'http[a-zA-Z0-9://._@]*', "", text);
        text = re.sub(r'^RT[\s]+', "", text);
        text = re.sub(r'\W', " ", text);
        text = re.sub(r'[\s]+', " ", text);
        text = text.lower();

        return text;

    def tweets_dataframe(self, tweets_list):
        """
        This function returns a Dataframe from the given tweets list.
        Also creates a CSV file.
        """
        tw_dataframe = pandas.DataFrame(data=[tweet.id for tweet in tweets_list], columns=["ID"]);

        tw_dataframe["AUTHOR"] = [tweet.author.screen_name for tweet in tweets_list];
        tw_dataframe["TEXT"] = [self.clean_line_feeds(tweet.full_text) for tweet in tweets_list];
        tw_dataframe["DATE"] = [str(tweet.created_at) for tweet in tweets_list];
        tw_dataframe["LIKES"] = [tweet.favorite_count for tweet in tweets_list];
        tw_dataframe["RTS"] = [tweet.retweet_count for tweet in tweets_list];
        tw_dataframe["HTS"] = [tweet.entities["hashtags"] for tweet in tweets_list];
        #tw_dataframe["URL"] = [tweet.entities["urls"] for tweet in tweets_list];

        tw_dataframe["POLARITY"] = [self.tweets_polarity(text) for text in tw_dataframe["TEXT"]];
        tw_dataframe["SENT_LABEL"] = [self.tweets_sentiment(polarity) for polarity in tw_dataframe["POLARITY"]];

        tw_dataframe.to_csv("saved_csv/tw_dataframe.csv");
        return tw_dataframe;
    
    def tweets_polarity(self, tweet):
        """
        This function sets a polarity index for each tweet.
        """
        sent_analysis = TextBlob(self.clean_text_for_sentiment(tweet));

        if tweet != "":
            if sent_analysis.detect_language() == "es":
                result = sent_analysis.translate(from_lang="es", to="en").sentiment.polarity;
        
        return result;
    
    def tweets_sentiment(self, tweet_polarity):
        """
        This function sets a positive-negative label for each tweet_polarity.

        polarity > 1 --> positive / polarity == 0 --> neutral / polarity < 0 = negative
        """

        if tweet_polarity > 0:
            return "positive";
        elif tweet_polarity == 0:
            return "neutral";
        else:
            return "negative";

    
    def likes_retweets_timeline(self, dataframe):
        """
        This function displays a historical timeline for the number of likes and Retweets --> To jpg file.
        """
        dataframe = dataframe.sort_values(by=["DATE"], ascending=True);

        # For this plot i just ignore the hours, min, sec.
        x = [date.split(" ")[0] for date in dataframe["DATE"]];

        pyplot.figure(figsize=(13, 5));
        pyplot.plot(x, dataframe["LIKES"], label="Likes");
        pyplot.plot(x, dataframe["RTS"], label="RTs");

        pyplot.legend();
        pyplot.xlabel("Date");
        pyplot.ylabel("Nº of likes / RTs");
        pyplot.title("Historical timeline for Likes and RTs");
        pyplot.savefig("saved_figs/timeline_likes_retweets.jpg");
        pyplot.show();
    
    def tweets_timeline(self, dataframe):
        """
        This function displays a historical timeline for the number of tweets + retweets --> To jpg file.
        """

        # For this plot i just ignore the hours, min, sec.
        x = [date.split(" ")[0] for date in dataframe["DATE"]];

        df_dates = pandas.DataFrame(data=x, columns=["Date"]);
        df_plot_dates_tweets = df_dates["Date"].value_counts().to_csv("saved_csv/tweets_timeline.csv");

        df_plot_dates_tweets = pandas.read_csv("saved_csv/tweets_timeline.csv");
        df_plot_dates_tweets.columns = ["Date", "Tweets"];
        df_plot_dates_tweets = df_plot_dates_tweets.sort_values(by=["Date"], ascending=True);

        pyplot.figure(figsize=(13, 5));
        pyplot.plot(df_plot_dates_tweets["Date"], df_plot_dates_tweets["Tweets"]);
        pyplot.xlabel("Date");
        pyplot.ylabel("Nº of Tweets/RTs");
        pyplot.title("Historical timeline for Nº of tweets");
        pyplot.savefig("saved_figs/timeline_tweets.jpg");
        pyplot.show();

    def hashtag_cloud(self):
        """
        This function collects hashtags from each tweet of the tw_dataframe.csv file, created by tweets_dataframe() function.
        Then creates a dataframe ranking most repeated hashtags --> To csv file.
        Returns a hashtag cloud --> To jpg file.
        """
        tw_dataframe = pandas.read_csv("saved_csv/tw_dataframe.csv", index_col=False);

        hashtags_series = tw_dataframe["HTS"];

        split_object_list = [];

        for object in hashtags_series:
            split_object = object.split();
            for data in split_object:
                data = data.replace("'", "").replace("\"", "").replace("[", "").replace("]", "").replace("}", "").replace("{", "").replace(":", "").replace(",", "");
                split_object_list.append(data);

        hashtag_list = [];
        positions = range(0, len(split_object_list));
        for position in positions:
            if split_object_list[position] == "text":
                hashtag_list.append(split_object_list[position + 1]);

        df_hashtags = pandas.DataFrame(data=hashtag_list, columns=["hashtags_count"]);
        most_repeated_hashtags = df_hashtags["hashtags_count"].value_counts();
        most_repeated_hashtags.to_csv("saved_csv/most_repeated_hashtags.csv");

        hashtag_string = "";
        for hashtag in hashtag_list:
            hashtag_string += hashtag + " ";

        wordcloud = WordCloud(width=1024, height=800, colormap="Blues", min_font_size=14).generate(hashtag_string)
        pyplot.figure(figsize=(8, 5), facecolor=None);
        pyplot.imshow(wordcloud);
        pyplot.axis("off");
        pyplot.title("Hashtags Cloud");
        pyplot.savefig("saved_figs/hashtags_cloud.jpg");
        pyplot.show();

    def keywords_cloud(self):
        """
        This function creates a wordcloud from the texts contained in tw_dataframe.csv file, created by tweets_dataframe() function.
        Uses stopwords to remove irrelevant words.
        Returns a keyword cloud --> To jpg file.
        """
        tw_dataframe = pandas.read_csv("saved_csv/tw_dataframe.csv", index_col=False);

        keywords_string = "";

        for text in tw_dataframe["TEXT"]:
            keywords_string += self.clean_text_for_tagcloud(text) + " ";

        wordcloud = WordCloud(width=1024, height=800, max_words=100, colormap="Blues", min_font_size=14);
        wordcloud.stopwords = nltk.corpus.stopwords.words("spanish");
        wordcloud.generate(keywords_string);
        
        pyplot.figure(figsize=(8, 5), facecolor=None);
        pyplot.imshow(wordcloud);
        pyplot.axis("off");
        pyplot.title("keywords Cloud");
        pyplot.savefig("saved_figs/keywords_cloud.jpg");
        pyplot.show();

    def sentiment_plot(self):
        """
        This function creates a piechart from SENT_LABEL column contained in tw_dataframe.csv file.
        """
        tw_dataframe = pandas.read_csv("saved_csv/tw_dataframe.csv", index_col=False);

        sent_label_series = tw_dataframe["SENT_LABEL"].value_counts();
        sent_label_series.to_csv("saved_csv/overall_sentiment.csv", index_label="NAME_LABELS");

        overall_sent_df = pandas.read_csv("saved_csv/overall_sentiment.csv");

        overall_sent_df["PERCENT"] = [round(data * 100 / overall_sent_df["SENT_LABEL"].values.sum(), 1) for data in overall_sent_df["SENT_LABEL"]]

        labels = overall_sent_df["NAME_LABELS"].values;

        pyplot.pie(overall_sent_df["PERCENT"].values, autopct="%1.1f%%", labels=labels);
        pyplot.title("Overall Sentiment");
        pyplot.savefig("saved_figs/overall_sentiment.jpg");
        pyplot.show()

        overall_sent_df.to_csv("saved_csv/overall_sentiment.csv");
