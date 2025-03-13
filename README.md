Telegram Bot – Weather and Currency Converter
This is a Telegram bot that provides weather information, currency conversion, and basic interaction features.

Features
✅ Weather Check – Get real-time weather updates for any city.
✅ Currency Converter – Convert currency between multiple options.
✅ Basic Chat Interaction – The bot responds to simple greetings.
✅ Social Media Link – Provides a link to the creator’s Instagram.


Installation:
  Clone the Repository:
      git clone https://github.com/your-repo.git
      cd your-repo
      
  Install Dependencies:
      pip install -r requirements.txt
      
  Set Up Environment Variables:
      Create a .env file and add your API keys:
          TELEGRAM_BOT_TOKEN=your_telegram_token
          WEATHER_API_KEY=your_openweather_api_key
          CURRENCY_API_KEY=your_currency_api_key
  
  Run the Bot:
      python bot.py


Commands
    /start – Start the bot.
    /help – Get a list of available commands.
    /social_media – Get a link to the creator's Instagram.
    /weather – Check the weather in any city.
    /currency – Convert an amount from one currency to another.

    
Usage
    Weather Command
        Send /weather.
        Enter a city name.
        The bot will return the temperature in Celsius.

Currency Converter
        Send /currency.
        Enter an amount to convert.
        Select a currency pair from the inline buttons or enter a custom pair (e.g., USD/EUR).
        The bot will return the converted amount.

Dependencies
    pyTelegramBotAPI – For Telegram bot functionality
    requests – To fetch weather and currency data
    currency_converter – For currency conversion
    python-dotenv – For environment variables

Notes
    Make sure you have a valid OpenWeather API key for weather updates.
    The currency conversion uses both CurrencyConverter and CurrencyAPI.

License
    This project is open-source. Feel free to modify and improve it!
