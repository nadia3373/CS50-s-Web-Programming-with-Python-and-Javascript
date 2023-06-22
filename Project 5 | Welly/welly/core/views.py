import json, requests
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import *
from .models import *
from telegram.views import notify


def get_choices(company, date, service):
    choices = []
    i = 0
    while i < 24:
        if i >= company.working_hours.all().first().workday_start.hour and i + service.length <= company.working_hours.all().first().workday_finish.hour:
            appointments = company.company_appointments.all().filter(appointment_date=date).filter(appointment_status__in=["Created", "Verified"])
            status = True
            for appointment in appointments:
                time = int(str(appointment.appointment_start_time).split(":")[0])
                if i in [x for x in range(time, time + appointment.service.length)]: status = False
                if i + service.length - 1 in [x for x in range(time, time + appointment.service.length)]: status = False
            if status is True: choices.append((i, i))
        i += 1
    return choices


# Create your views here.
def about(request, id):
    """
    Get company info.
    """
    company = Company.objects.filter(domain=id).first()
    if company: return render(request, "core/about.html", {'company': company, 'from': company.working_hours.all().first().workday_start.hour, 'to': company.working_hours.all().first().workday_finish.hour})
    return HttpResponseRedirect(reverse('index'))


@login_required
def appointments(request, id):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.user.manager:
            appointments = Appointment.objects.filter(company=company).order_by('-appointment_date')
            return render(request, "core/appointments.html", {
                                                            "confirmed": appointments.filter(appointment_status="Verified"),
                                                            "created": appointments.filter(appointment_status="Created"),
                                                            "cancelled": appointments.filter(appointment_status="Cancelled"),
                                                            "archived": appointments.filter(appointment_status="Archived"),
                                                            'company': company,
                                                        })
        return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


@login_required
def add_service(request, id):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.user.manager:
            if request.method == "GET": return render(request, "core/add_service.html", {'company': company, 'form': ServiceForm(), 'service': service})
            form = ServiceForm(request.POST, request.FILES)
            if form.is_valid():
                if "image" in request.FILES: Service.objects.create(company=company, description=request.POST["description"], name=request.POST["name"], length=int(request.POST["length"]), price=int(request.POST["price"]), status=bool(request.POST["status"]), image=request.FILES["image"])
                else: Service.objects.create(company=company, description=request.POST["description"], name=request.POST["name"], length=int(request.POST["length"]), price=int(request.POST["price"]), status=bool(request.POST["status"]))
                return HttpResponseRedirect(reverse("manage", kwargs={'id': company.domain}))
            return render(request, "core/add_service.html", {'company': company, 'form': form, 'service': service})
        return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


@login_required
def cancel(request, id, app):
    """
    Cancel an appointment.
    """
    company = Company.objects.filter(domain=id).first()
    if company:
        appointment = Appointment.objects.filter(company=company, pk=app).first()
        if appointment and (appointment.client == request.user or request.user.manager):
            appointment.appointment_status = "Cancelled"
            appointment.save()
        notify(appointment.client, User.objects.filter(company=company).filter(manager=True), appointment)
        if request.user.manager: return HttpResponseRedirect(reverse("appointments", kwargs={'id': company.domain}))
        return HttpResponseRedirect(reverse("profile", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


def company(request, id):
    """
    Get company by domain.
    If company exists, redirect to its main page, otherwise redirect to the index page.
    """
    company = Company.objects.filter(domain=id).first()
    if company: return render(request, "core/company.html", {'company': company})
    return HttpResponseRedirect(reverse('index'))


@login_required
def company_settings(request,id):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.user.manager:
            if request.method == "GET": return render(request, "core/company_settings.html", {'company': company, 'form': CompanyEditForm(instance=company)})
            else:
                form = CompanyEditForm(request.POST, request.FILES)
                print(form.is_valid())
                if form.is_valid():
                    if company.country != request.POST["country"]: company.country = request.POST["country"]
                    if company.city != request.POST["city"]: company.city = request.POST["city"]
                    if company.street != request.POST["street"]: company.street = request.POST["street"]
                    if company.building != request.POST["building"]: company.building = request.POST["building"]
                    if company.office != request.POST["office"]: company.office = request.POST["office"]
                    if company.name != request.POST["name"]: company.name = request.POST["name"]
                    if company.description != request.POST["description"]: company.description = request.POST["description"]
                    if "logo-clear" in request.POST:
                        if request.POST["logo-clear"] == "on": company.logo = "core/placeholder.jpg"
                    else:
                        if "logo" in request.FILES: company.logo = request.FILES["logo"]
                    response = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey=46d2f553-78c3-4527-926b-d20719dd9a72&format=json&geocode={company.country}+{company.city}+{company.street}+{company.building}&results=1").json()
                    if response and response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']:
                        company.longitude, company.latitude = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[0], response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[1]
                    else: company.longitude, company.latitude = "NULL", "NULL"
                    company.save()
                    return render(request, "core/company_settings.html", {'company': company, 'form': CompanyEditForm(instance=company)}, status = 200)
                return render(request, "core/company_settings.html", {'company': company, 'form': form}, status = 201)
        return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


@login_required
def confirm(request, id, app):
    """
    Confirm an appointment.
    """
    company = Company.objects.filter(domain=id).first()
    if company:
        appointment = Appointment.objects.filter(company=company, pk=app).first()
        if appointment and (appointment.client == request.user or request.user.manager):
            appointment.appointment_status = "Verified"
            appointment.save()
        notify(appointment.client, User.objects.filter(company=company).filter(manager=True), appointment)
        if request.user.manager: return HttpResponseRedirect(reverse("appointments", kwargs={'id': company.domain}))
        return HttpResponseRedirect(reverse("profile", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


@login_required
def delete_image(request, id, img):
    company = Company.objects.filter(domain=id).first()
    if company:
        image = Image.objects.filter(pk=img)
        if image: image.delete()
        return HttpResponseRedirect(reverse("manage", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


@login_required
def edit_service(request, id, sid):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.user.manager:
            service = Service.objects.filter(pk=sid).first()
            if service:
                if request.method == "GET": return render(request, "core/edit_service.html", {'company': company, 'form': ServiceForm(instance=service), 'service': service})
                form = ServiceForm(request.POST, request.FILES)
                if form.is_valid():
                    if service.description != request.POST["description"]: service.description = request.POST["description"]
                    if service.name != request.POST["name"]: service.name = request.POST["name"]
                    if service.length != int(request.POST["length"]): service.length = int(request.POST["length"])
                    if service.price != int(request.POST["price"]): service.price = int(request.POST["price"])
                    if service.status != bool(request.POST["status"]): service.status = bool(request.POST["status"])
                    if "image-clear" in request.POST:
                        if request.POST["image-clear"] == "on": service.image = "core/placeholder.jpg"
                    else:
                        if "image" in request.FILES: service.image = request.FILES["image"]
                    service.save()
                return render(request, "core/edit_service.html", {'company': company, 'form': form, 'service': service})
        return HttpResponseRedirect(reverse("manage", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


def gallery(request, id):
    company = Company.objects.filter(domain=id).first()
    if company: return render(request, "core/gallery.html", {'company': company, 'images': Image.objects.filter(company=company)})
    return HttpResponseRedirect(reverse('index'))


@login_required
def gallery_management(request, id):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.method == "GET": return render(request, "core/gallery_management.html", {'company': company, 'form': ImageForm()})
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            Image.objects.create(company=company, description=request.POST["description"], image=request.FILES["image"])
            return HttpResponseRedirect(reverse("manage", kwargs={'id': company.domain}))
        return render(request, "core/gallery_management.html", {'company': company, 'form': ImageForm()})
    return HttpResponseRedirect(reverse('index'))


def index(request):
    return render(request, "core/index.html")


def login_view(request):
    """
    Login view for both managers and users.
    """
    if request.method == "POST":
        # Attempt to sign user in
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        # If authentication succesful, redirect the user to the company's main page.
        # Otherwise, return an error.
        if user is not None:
            company = user.company
            login(request, user)
            return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
        return render(request, "core/login.html", {'message': 'Incorrect phone number or password'})
    return render(request, "core/login.html")


@login_required
def logout_view(request, id):
    logout(request)
    company = Company.objects.filter(domain=id).first()
    if company: return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def manage(request, id):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.user.manager:
            if request.user.telegram_id: return render(request,  "core/manage.html", {'company': company})
            else: return render(request,  "core/placeholder.html", {'company': company})
        return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def profile(request, id):
    company = Company.objects.filter(domain=id).first()
    if company:
        appointments = Appointment.objects.filter(client = request.user).order_by('-appointment_date')
        return render(request, "core/profile.html", {
                                                        "confirmed": appointments.filter(appointment_status="Verified"),
                                                        "created": appointments.filter(appointment_status="Created"),
                                                        "cancelled": appointments.filter(appointment_status="Cancelled"),
                                                        "archived": appointments.filter(appointment_status="Archived"),
                                                        'company': company,
                                                        'telegram': request.user.telegram_id if request.user.telegram_id else None
                                                    })
    return HttpResponseRedirect(reverse("index"))


def register(request, id):
    """
    Registration view for users.
    After succesfully determining a company by domain, user is presented with registration form.
    On POST request, company id gets added to the user object after data validation, and the user is saved.
    """
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.method == "POST":
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                date = datetime.strptime(request.POST["dob"], "%Y-%m-%d").date()
                current = datetime.now().date()
                if 100 < current.year - date.year or current.year - date.year < 14: return render(request, "core/register.html", {"company": company, "form": form, 'error': 'Age must be between 14 and 100 years'})
                if not request.POST["first_name"].isalpha() or 30 < len(request.POST["first_name"]) or len(request.POST["first_name"]) < 2: return render(request, "core/register.html", {'company': company, 'form': form, 'error': 'First name must contain at least 2 letters and at maximum 30 letters'})
                if not request.POST["last_name"].isalpha() or 30 < len(request.POST["last_name"]) or len(request.POST["last_name"]) < 2: return render(request, "core/register.html", {'company': company, 'form': form, 'error': 'Last name must contain at least 2 letters and at maximum 30 letters'})
                user = form.save(commit=False)
                if not user.photo: user.photo = "core/placeholder.jpg"
                user.company = company
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
            return render(request, "core/register.html", {"company": company, "form": form})
        return render(request, "core/register.html", {"company": company, "form": UserForm()})
    return HttpResponseRedirect(reverse("index"))


def register_company(request):
    """
    Registration view for companies.
    After succesfully determining a company by domain, user is presented with registration form.
    On POST request, company id gets added to the user object after data validation, and the user is saved.
    """
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            if not company.logo: company.logo = "core/placeholder.jpg"
            response = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey=46d2f553-78c3-4527-926b-d20719dd9a72&format=json&geocode={company.country}+{company.city}+{company.street}+{company.building}&results=1").json()
            if response and response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']:
                company.longitude, company.latitude = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[0], response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[1]
            else: company.longitude, company.latitude = "NULL", "NULL"
            company.save()
            Working_hours.objects.create(company=company, workday_start="9:00:00", workday_finish="18:00:00")
            return HttpResponseRedirect(reverse("register_manager", kwargs={'id': company.domain}))
        return render(request, "core/register_company.html", {"form": form})
    else: return render(request, "core/register_company.html", {"form": CompanyForm()})


def register_manager(request, id):
    """
    Registration view for users.
    After succesfully determining a company by domain, user is presented with registration form.
    On POST request, company id gets added to the user object after data validation, and the user is saved.
    """
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.method == "POST":
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                date = datetime.strptime(request.POST["dob"], "%Y-%m-%d").date()
                current = datetime.now().date()
                if 100 < current.year - date.year or current.year - date.year < 14: return render(request, "core/register_manager.html", {"company": company, "form": form, 'error': 'Age must be between 14 and 100 years'})
                if not request.POST["first_name"].isalpha() or 30 < len(request.POST["first_name"]) or len(request.POST["first_name"]) < 2: return render(request, "core/register.html", {'company': company, 'form': form, 'error': 'First name must contain at least 2 letters and at maximum 30 letters'})
                if not request.POST["last_name"].isalpha() or 30 < len(request.POST["last_name"]) or len(request.POST["last_name"]) < 2: return render(request, "core/register.html", {'company': company, 'form': form, 'error': 'Last name must contain at least 2 letters and at maximum 30 letters'})
                user = form.save(commit=False)
                if not user.photo: user.photo = "core/placeholder.jpg"
                user.company = company
                user.manager = True
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("manage", kwargs={'id': company.domain}))
            return render(request, "core/register_manager.html", {"company": company, "form": form})
        return render(request, "core/register_manager.html", {"company": company, "form": UserForm()})
    return HttpResponseRedirect(reverse("index"))


def services(request, id):
    """
    Get company's list of services.
    """
    company = Company.objects.filter(domain=id).first()
    if company: return render(request, "core/services.html", {'company': company, 'services': company.services.all})
    return HttpResponseRedirect(reverse('index'))


@login_required
def service(request, id, sid):
    """
    Get service availability by id.
    """
    company = Company.objects.filter(domain=id).first()
    if company: service = Service.objects.filter(company=company, pk=sid).first()
    if company and service: return render(request, "core/service.html", {'company': company, 'days': range(7), 'service': service, 'weeks': range(6)})
    return HttpResponseRedirect(reverse('index'))


@login_required
def settings(request, id):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.method == "GET": return render(request, "core/settings.html", {'company': company, 'form': UserForm(instance=request.user, use_required_attribute=False)})
        else:
            password = False
            form = UserForm(request.POST, request.FILES)
            date = datetime.strptime(request.POST["dob"], "%Y-%m-%d").date()
            if request.user.dob != date:
                current = datetime.now().date()
                if 14 <= current.year - date.year <= 100: request.user.dob = date
                else: return render(request, "core/settings.html", {'company': company, 'form': form, 'error': 'Age must be between 14 and 100 years'})
            if request.user.email != request.POST["email"]:
                try:
                    validate_email(request.POST["email"])
                    request.user.email = request.POST["email"]
                except validate_email.ValidationError: return render(request, "core/settings.html", {'company': company, 'form': form})
            if request.user.first_name != request.POST["first_name"]:
                if request.POST["first_name"].isalpha() and 2 <= len(request.POST["first_name"]) <= 30: request.user.first_name = request.POST["first_name"]
                else: return render(request, "core/settings.html", {'company': company, 'form': form, 'error': 'First name must contain at least 2 letters and at maximum 30 letters'})
            if request.user.last_name != request.POST["last_name"]:
                if request.POST["last_name"].isalpha() and 2 <= len(request.POST["last_name"]) <= 30: request.user.last_name = request.POST["last_name"]
                else: return render(request, "core/settings.html", {'company': company, 'form': form, 'error': 'Last name must contain at least 2 letters and at maximum 30 letters'})
            if request.user.phone_number != request.POST["phone_number"]:
                if request.POST["phone_number"].isdigit() and len(request.POST["phone_number"]) == 10: request.user.phone_number = request.POST["phone_number"]
                else: return render(request, "core/settings.html", {'company': company, 'form': form, 'error': 'Phone number must contain 10 digits, symbols or letters not allowed'})
            if "photo" in request.FILES: request.user.photo = request.FILES["photo"]
            if request.POST["password1"] != '' and request.POST["password2"] != '':
                try:
                    password_validation.validate_password(request.POST["password1"])
                    if request.POST["password1"] == request.POST["password2"]:
                        password = True
                        request.user.password = make_password(request.POST["password1"])
                    else: return render(request, "core/settings.html", {'company': company, 'form': form, 'error': "Passwords do not match"})
                except Exception as e: return render(request, "core/settings.html", {'company': company, 'form': form, 'error': e})
            request.user.save()
            if password is True: return HttpResponseRedirect(reverse("login"))
            return render(request, "core/settings.html", {'company': company, 'form': UserForm(instance=request.user, use_required_attribute=False), 'message': "Your profile has been updated successfully"})
    return HttpResponseRedirect(reverse("index"))


@login_required
def times(request, id, sid, date):
    """
    Get free time slots for a service.
    """
    company = Company.objects.filter(domain=id).first()
    if company:
        service = Service.objects.filter(company=company, pk=sid).first()
        if service:
            choices = get_choices(company, date, service)
            form = AppointmentForm(choices) if len(choices) > 0 else None
            if request.method == "GET": return render(request, "core/times.html", {'company': company, 'date': date, "form": form, 'service': service})
            else:
                time = json.loads(request.body)["appointment_start_time"]
                if (int(time), int(time)) in form.fields["appointment_start_time"].choices:
                    # date = datetime.strptime(date, "%d-%m-%Y").date()
                    appointment = Appointment.objects.create(appointment_start_time = time + ":00", appointment_date = date, client = request.user, company = company, service = service)
                    message = "Appointment is successfull"
                    notify(appointment.client, User.objects.filter(company=company).filter(manager=True), appointment)
                else: message = "Something went wrong"
                return JsonResponse({"message": message})
        return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse('index'))


@login_required
def wh(request, id):
    company = Company.objects.filter(domain=id).first()
    if company:
        if request.user.manager:
            if request.method == "GET": return render(request, "core/wh.html", {'company': company, 'form': WHForm(instance=company.working_hours.all().first())})
            else:
                form = WHForm(request.POST)
                hours = company.working_hours.all().first()
                try:
                    start = datetime.strptime(request.POST['workday_start'] + ":00:00", "%H:%M:%S").time()
                    finish = datetime.strptime(request.POST['workday_finish'] + ":00:00", "%H:%M:%S").time()
                except: return render(request, "core/wh.html", {'company': company, 'form': WHForm(), 'error': 'Incorrect working hours'})
                print(start < finish)
                if start < finish:
                    hours.workday_start = start
                    hours.workday_finish = finish
                    hours.save()
                    return render(request, "core/wh.html", {'company': company, 'form': WHForm(instance=company.working_hours.all().first()), 'message': 'Working hours were successfully updated'})
                return render(request, "core/wh.html", {'company': company, 'form': form, 'error': 'Incorrect working hours'})
        return HttpResponseRedirect(reverse("company", kwargs={'id': company.domain}))
    return HttpResponseRedirect(reverse("index"))


"""
Notes

1. Login and registration views mustn't be accessible for authenticated users.
2. Modify company function to work with custom domains.

"""