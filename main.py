from app.Bot import BotAgenda
from app.Config import config

if __name__ == "__main__":
    BotAgenda().run(config.dicordBotToken)
