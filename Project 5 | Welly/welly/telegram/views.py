from core.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json, os, requests
from dotenv import load_dotenv


root = os.path.expanduser('~/welly')
load_dotenv(os.path.join(root, '.env'))

BOT_TOKEN = os.getenv('BOT_TOKEN')


# Create your views here.
@csrf_exempt
def messages(request):
    data = json.loads(request.body)
    print(data)
    try:
        message = data["message"]
        user = User.objects.filter(pk = message["text"].split()[1].split("-")[1]).first()
        if not user.telegram_id:
            user.telegram_id = message["chat"]["id"]
            user.save()
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": user.telegram_id, "text": "You have successfully subscribed", "parse_mode": "Markdown"})
    except: pass
    return HttpResponse(request, "ok")


def notify(user, managers, appointment):
    if user.telegram_id:
        if appointment.appointment_status == "Cancelled":
            text = f'Unfortunately, your appointment has been cancelled by manager. Contact manager for more details: {managers.first().phone_number}\nDate: {appointment.appointment_date} {appointment.appointment_start_time}\nService: {appointment.service.name}'
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": user.telegram_id, "text": text, "parse_mode": "Markdown"})
        elif appointment.appointment_status == "Verified":
            text = f'Your appointment has been confirmed by manager. Manager contact: {managers.first().phone_number}\nDate: {appointment.appointment_date} {appointment.appointment_start_time}\nService: {appointment.service.name}'
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": user.telegram_id, "text": text, "parse_mode": "Markdown"})
        elif appointment.appointment_status == "Created":
            text = f'Your appointment has been created and needs to be approved by manager. Manager contact: {managers.first().phone_number}\nDate: {appointment.appointment_date} {appointment.appointment_start_time}\nService: {appointment.service.name}'
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": user.telegram_id, "text": text, "parse_mode": "Markdown"})
    for manager in managers:
        if manager.telegram_id:
            if appointment.appointment_status == "Cancelled":
                text = f'Appointment cancelled\nDate: {appointment.appointment_date} {appointment.appointment_start_time}\nService: {appointment.service.name}\nClient: {appointment.client}'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": manager.telegram_id, "text": text, "parse_mode": "Markdown"})
            elif appointment.appointment_status == "Verified":
                text = f'Appointment confirmed\nDate: {appointment.appointment_date} {appointment.appointment_start_time}\nService: {appointment.service.name}\nClient: {appointment.client}'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": manager.telegram_id, "text": text, "parse_mode": "Markdown"})
            elif appointment.appointment_status == "Created":
                text = f'Appointment created\nDate: {appointment.appointment_date} {appointment.appointment_start_time}\nService: {appointment.service.name}\nClient: {appointment.client}'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": manager.telegram_id, "text": text, "parse_mode": "Markdown"})
