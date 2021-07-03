## Tweets Analyzer App - Using Matplotlib, Nltk, Pandas, RE, Textblob and Wordcloud.

------------ FEATURES:

* This app asks the user for a word, phrase or hashtag and returns:

- General history of the last 100 tweets.
- Comparative history of Likes and Retweets.
- Cloud of most used hashtags.
- Cloud of most used words.
- General sentiment graph.
- It also saves this information in csv and jpg format.
  
* The first thing you should do is create two folders called: saved_csv and saved_figs. The results will be saved there.

------------ WHY ONLY 100 POST?

The amount of post returned by the app can be modified. But, for this exercise, I thought it best to limit it to 100 posts for the following reasons:

- AVOID THE BAN:

While doing the project, and thinking about the correction, I have executed and made so many requests that Twitter has banned me several times. This means waiting 15 min, in the best of cases, to make requests again. By limiting the amount to 100 posts, I have more chances to test.

- AVOID THE TRANSLATOR'S BAN:

In the same way, an Http 429 (Too Many Requests) error may arise. The reason is, I think, in the requests to translate that I make in the function def tweets_polarity (self, tweet): (line 63 of class_analyzer.py).

If this error comes up, I think the solution is to put a time.sleep as shown below:

def tweets_polarity (self, tweet):
"" "
        This function sets a polarity index for each tweet.
        "" "
        sent_analysis = TextBlob (self.clean_text_for_sentiment (tweet));

        if tweet! = "":
            if sent_analysis.detect_language () == "es":
                result = sent_analysis.translate (from_lang = "es", to = "en"). sentiment.polarity;
-----> time.sleep (5);
        
        return result;

However, this solution does not work once the error has occurred. The reason I don't include the time.sleep directly is that the execution time would be too slow and programming would be very tedious.

------------ USE TIPS:

- WHAT WORD TO LOOK FOR?

When collecting only 100 posts, it would be best to search for a word that is viral enough to collect several days. But, if the word is too viral, the collected posts will be made on the same day and the historical graphics will not look good.

Therefore, the recommendation is to look for a word, hashtag or phrase that is "mildly viral", if you can say so.


####################################### SPANISH ###########################################

------------ CARACTERÍSTICAS:

* Esta app pide al usuario una palabra, frase o hashtag y devuelve:

	- Histórico general de los últimos 100 tweets.
	- Histórico comparado de Likes y Retweets.
	- Nube de hashtags más usados.
	- Nube de palabras más usadas.
	- Gráfico de sentimiento general.
	- Además guarda esta información en formato csv y jpg.
  
* Lo primero que debes hacer es crear dos carpetas llamadas: saved_csv y saved_figs. Allí se guardarán los resultados.

------------ ¿ POR QUÉ SOLO 100 POST?

La cantidad de post que devuelve la app se puede modificar. Pero, para este ejercicio, he creído mejor limitarlo a 100 post por las siguientes razones:

	- EVITAR EL BAN:

	Mientras hacía el proyecto, y pensando en la corrección, he ejecutado y hecho tantas peticiones que Twitter me ha banneado varias veces. Esto supone esperar 15 min, en el mejor de los casos para volver a hacer peticiones. Limitando la cantidad a 100 post tengo más posibilidades de prueba.
	
	- EVITAR EL BAN DEL TRADUCTOR:
		
	De la misma forma, puede surgir un error Http 429 (Too Many Requests). La razón está, creo, en las peticiones para traducir que hago en la función def tweets_polarity(self, tweet): (línea 63 de la class_analyzer.py).
	
	Si surge este error, creo que la solución es poner un time.sleep como se muestra a continuación:
	
	def tweets_polarity(self, tweet):
		"""
        	This function sets a polarity index for each tweet.
        	"""
        	sent_analysis = TextBlob(self.clean_text_for_sentiment(tweet));

        	if tweet != "":
            		if sent_analysis.detect_language() == "es":
                		result = sent_analysis.translate(from_lang="es", to="en").sentiment.polarity;
			----->	time.sleep(5);
        
        		return result;
	
	Sim embargo, esta solución no funciona una vez ya ha saltado el error. La razón por la que no incluyo directamente el time.sleep, es que el tiempo de ejecución sería demasiado lento y programar sería muy tedioso.

------------ CONSEJOS DE USO:

- ¿QUÉ PALABRA BUSCAR?

	Al recoger solo 100 post, lo mejor sería buscar una palabra que sea suficientemente viral como para recoger varios días. Pero, si la palabra es demasiado viral, los post recogidos estarán hechos en el mismo día y los gráficos históricos no quedarán bien.

	Por lo tanto, la recomendación es buscar una palabra, hashtag o frase que sean "medianamente virales", si se puede decir así.
