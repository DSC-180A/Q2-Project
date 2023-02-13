def sentiment_analyzer(self, sentence):
        """_summary_: Analyze the sentiment of a sentence

        Args:
            sentence (str): sentence to analyze

        Returns:
            str: Positive, Negative, or Neutral
        """
        polarity = self.model.polarity_scores(sentence)
        compound_score = polarity["compound"]

        if compound_score >= 0.05:
            return "Positive"
        elif compound_score < 0.05 and compound_score > -0.05:
            return "Neutral"
        else:
            return "Negative"
