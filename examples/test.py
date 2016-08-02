import bot

instance = bot.Bot("abhishekpratapa@utexas.edu", "BedruSe7", "5129831767", bot.Sites.Google, bot.UserAgent.Firefox, False, ["Google_Data_Base"], ["stocks_article"])

# test post
#instance.post("hello")

# searching
instance.search(["ariana grande"], 10, [])

# test message
#instance.message("abhishekpratapa@gmail.com", "test_subject", "here is a test message")

# close instance
instance.close()