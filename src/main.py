import bot

# The main file that does everything
def main():
    instance = bot.Bot("abhishekpratapa@gmail.com", "AlinaSchroeder#123", "5129831767", bot.Sites.LinkedIn,
                       bot.UserAgent.Firefox, True, "mongodb://localhost:27017", ["LinkedIn_Data_Base"])


    instance.siteAgent.search("Dogs", 20, True, True, 3)
    instance.close()
    pass

if __name__ == '__main__':
    main()