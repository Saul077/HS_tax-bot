# HS_tax-bot
This is the code for a telegram bot that gives the user the total tax in Sri Lanka for a product of a specific HS Code

<img width="397" alt="image" src="https://github.com/Saul077/HS_tax-bot/assets/117183987/c13400e4-153e-4b95-99ec-bb09f0472e38">

The bot works by getting the HS code as input from the user, extracting the relevant chapter number in which the hs code given is found (first 2 digits of a valid hs code), and then downloading the relevant chapter from the Sri Lankan official import tariff website. As the hs codes and the relevant taxes involved is presented in the form of tables, the file downloaded, which is in pdf form, is then converted into a csv file to make it easier to extract information from the file. FInally, the relevant hs code is then searched from the csv file, and taxes relevant to the hs code is then presented to the user through telegram

This bot was fully coded using python and its relevant modules

You can directly run the bot from your local pc by downloading all files to ur pc, installing the requirements.txt file using pip and inserting the telegram bot token obtained to the relevant "TOKEN" variable in bot.py. Finally, run the bot.py file, and use command "/start" to start the bot.
