from fuzzywuzzy import fuzz

class profanityfilter:
	def __init__(self, profanities, threshold):
		self.profanities = profanities
		self.threshold = threshold
	def scan(self, query):
		for profanity in self.profanities:
			rating = fuzz.partial_ratio(query, profanity)
			if rating >= self.threshold:
				return True
		return False
