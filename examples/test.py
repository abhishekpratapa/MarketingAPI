import bot

instance = bot.Bot("email", "password", "phone", bot.Sites.Google, bot.UserAgent.Firefox, True, "mongodb://localhost:27017", ["Google_Data_Base"])

# test post
#instance.post("hello")

# searching
instance.search(["ariana grande"], 10, [], "0/0/0", "0/0/0", 0, "website_urls")

# test message
#instance.message("abhishekpratapa@gmail.com", "test_subject", "here is a test message")

# close instance
instance.close()
