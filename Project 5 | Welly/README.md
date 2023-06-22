<h1>WEB50 Project 5: Capstone</h1>

# Distinctiveness and Complexity

This project is a SaaS multitenant web app for professionals in the beauty industry and their clients. It’s built with Django and uses a shared database approach. The project is based on a unique idea of a convenient tool, which allows beauty masters organise their workflow, control the appointments and stay in touch with their clients.

## Main features for masters (managers):
    * Register company
    * Add and edit company services
    * View and manage appointments
    * Edit company logo, information and business hours
    * Receive telegram notifications about new appointments and appointment status changes (production environment only)

## Main features for clients:
    * Register
    * View company information, location on a map and list of services
    * Book an appointment for a particular date, time and service
    * Control status of own appointments
    * Update profile
    * Receive telegram notifications about appointment status changes (production environment only)

# What’s contained in each file

The project consists of 2 apps – Telegram and Core.
The Telegram app is responsible for receiving and sending messages, the Core app is responsible for everything else.

## Contents of the Telegram app:
* urls.py – a webhook path
* views.py – views to receive and send messages to Telegram users

## Contents of the Core app:
* admin.py – registered key models for the superuser to be able to control these objects – Appointment, Company, Image, Service, User
* forms.py – contains all the forms used in the app
* models.py – contains all the database models used in the app:
    * Company – company object, containing company name, domain, address, coordinates etc.
    * Image – gallery image object
    * Service – service objects, containing service name, image, price, length and status
    * User – user object, containing standard AbstractUser fields plus phone number (used for authentication), manager status, telegram id and date of birth
    * Working hours – object that stores information about business hours of a company
* urls.py – contains all the paths used in the app.
* views.py – contains all the views used in the app:

    ### Manager views:
    * add_service – add a new service for given company
    * appointments – get list of appointments for given company and manafe them
    * company_settings – view and edit company information
    * confirm – confirm an appointment
    * delete_image – delete image from the gallery
    * edit_service – edit a service
    * gallery_management – editable gallery for managers, upload and delete images
    * manage – company management page (main)
    * register_manager – registration for manager, after registration User.manager is set to True
    * wh – view and update working hours

    ### Views for all users:
    * about – get company information (for company homepage)
    * cancel – cancel an appointment
    * company – company homepage (main)
    * gallery – get and display images from company gallery
    * index – landing page, where company registration is available
    * login_view – log user in
    * logout_view – log user out
    * profile – get all the appointments for current user, user can cancel them
    * register – registration for users, after registration User.manager is set to False
    * register_company – registration for companies, company address is converted to coordinates with help of geocoding, coordinates are saved in database as well
    * services – get all services list for given company (for company homepage)
    * service – get service availability by id (for company homepage)
    * settings – view and update user profile information
    * times – get available time slots and make appointments (for company homepage)

## Templates:
* about.html – used in “about” view, part of company.html
* add_service.html – used in “add_service” view, part of manage.html
* appointment-card.html – used for displaying appointment card on the company page, part of profile.html
* appointment-management-card.html – used for displaying appointment card on the management page, part of appointments.html
* appointments.html – used in “appointments” view, appointments list for managers
* company_settings.html – used in “company_settings" view, part of manage.html
* company_menu.html – main menu for the management page, part of manage.html
* company.html – used in “company” view, company page for the users
* edit_service.html – used in “edit_service” view, part of manage.html
* gallery_management.html – used in “gallery_management” view, part of manage.html
* gallery.html – display gallery images, part of company.html
* index.html – landing page
* manage.html – company management page
* menu.html – main menu for the company homepage, part of company.html
* placeholder.html – optional page to display to managers instead of management page if they haven’t verified telegram account (disabled because the Telegram app features don't work on localhost)
* profile.html – used in “profile” view, appointments list for the users
* register_company.html – company registration page
* register_manager.html – manager registration page
* register.html – user registration page
* service.html – calendar to choose a day from for given service, part of company.html
* services.html – used in “services” view, part of company.html and manage.html
* settings.html – view and edit user profile information
* times.html – time choices for chosen service and day
* wh.html – view and update company working hours

### JavaScript files:
* appointments.js – used to handle appointments on the management page
* company-page.js – used to handle company homepage
* manage.js – used to handle management page
* profile.js – used to handle appointments on the users personal area

### CSS files:
* styles.css – all the styling for the project
