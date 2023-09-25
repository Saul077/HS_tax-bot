#Import modules
import os
import telebot
from hs_code import hs_code

#Define bot token and call telebot function
TOKEN="Bot-Token-Here"
bot = telebot.TeleBot(TOKEN)

def allowed_users(user_id):
    "this function checks whether the current user of the bot is authorized to use it"	
    file = open("users.txt", "r")
    user_list = file.read().split(",")
    if user_id in user_list:
        return True
    else:
        return False

#start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if allowed_users(str(message.chat.id)) == True:
        bot.reply_to(message,"Hi! Please type in the HS code to get the relevant tax (Ex; 96045000)")
    else:
        bot.reply_to(message,"You don't have access to this bot")

#handling the hs codes given
@bot.message_handler(func=lambda message: True)
def send_tax(message):
    if allowed_users(str(message.chat.id)) == True:
        bot.send_message(message.chat.id, "Calculating...")
        tax, hs_desc = hs_code(str(message.text))
        if tax == "":
            bot.send_message(message.chat.id, "Exact tax value could not be found, Please refer to the html file below and calculate the tax")
            with open("HS.html", "rb") as file:
                bot.send_document(message.chat.id, document=file)
            
        else:
            tax = "ITEM DESCRIPTION\n"+hs_desc+"\n\nTOTAL TAX\n"+str(tax)        
            bot.send_message(message.chat.id, tax)
    else:
        bot.send_message(message.chat.id,"You don't have access to this bot") 

bot.polling(none_stop=True)

