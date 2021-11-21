from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render
from .consumers import *
from dataapp.models import UserData
import telegram 
TELEGRAM_URL = "https://api.telegram.org/bot"
TOKEN = '2107502935:AAFFG4hKkGfNDJltz4BvIUTnqqfzV18Y5N0'

bot = telegram.Bot(token=TOKEN)

@csrf_exempt
def chat(request):
    print(request)
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
    
    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
    
    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message
    

class YoMamaBotView(generic.View):
    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print(incoming_message)
        if incoming_message["message"] != "":
            userid = incoming_message["message"]["from"]["id"]
            if incoming_message["message"]["text"] == "/start":
                custom_keyboard = [[ telegram.KeyboardButton("fat"),
                telegram.KeyboardButton("stupid"),telegram.KeyboardButton("dumb") ]]
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
                bot.sendMessage(chat_id=userid, text="Please select one", reply_markup=reply_markup)
            text = incoming_message["message"]["text"]
            # userid = incoming_message["message"]["from"]["id"]
            username = incoming_message["message"]["from"]["username"]
            UserData.objects.create(userid=userid,user_name=username)
            # print(incoming_message["message"]["from"]["id"])
            message = {'text':text}
            response = respond_to_websockets(message)
            send_message(response["text"],userid)
        else:
            pass
        return HttpResponse(response)


def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(TELEGRAM_URL+TOKEN+"/sendMessage", data=data)