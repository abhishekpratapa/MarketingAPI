import bot

instance = bot.Bot("abhishekpratapa@utexas.edu", "BedruSe7", "5129831767", bot.Sites.Google, bot.UserAgent.Firefox)

# test post
instance.post("hello")

# test message
instance.message("abhishekpratapa@gmail.com", "test_subject", "here is a test message")


# close instance
instance.close()