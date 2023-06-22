let button = document.querySelector(".menu-button.active");
const content = document.querySelector(".content");
document.querySelectorAll(".menu-button").forEach(button => {
    button.addEventListener("click", (e) => {
        button = e.target;
        fetchData(button);
        document.querySelector(".menu-button.active").classList.remove("active");
        e.target.classList.add("active");
    })
});

fetchData(button);

function displayMap(e) {
    e.innerHTML = `<p class="mb-3 mt-3">Our address: ${address}</p>
                  <img id="map" src="https://static-maps.yandex.ru/1.x/?ll=${lon},${lat}&size=650,300&z=17&l=map&pt=${lon},${lat},pm2rdl" hidden="true"">
                  <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>`;
    document.querySelector("#map").addEventListener("load", (e) => {
    document.querySelector(".spinner-border").remove();
    e.target.removeAttribute("hidden");
    });
};

function fetchData(button) {
    switch (button.dataset.type) {
        case "services":
            fetch(`${currentCompany}/${button.dataset.type}`).then(response => {
                return response.text()
            }).then(data => {
                content.innerHTML = data;
                handleServices();
            });
            break;
        case "gallery":
            fetch(`${currentCompany}/${button.dataset.type}`).then(response => {
                return response.text()
            }).then(data => {
                content.innerHTML = data;
            });
            break;
        case "location":
            displayMap(content);
            break;
        default:
            fetch(`${currentCompany}/${button.dataset.type}`).then(response => {
                return response.text()
            }).then(data => {
                content.innerHTML = data;
            });
            break;
    }
};

function handleServices() {
    document.querySelectorAll(".service-card").forEach((service) => {
        service.addEventListener("click", (e) => {
            fetch(`${currentCompany}/service/${service.dataset.id}`).then(response => {
                return response.text();
            }).then(data => {
                content.innerHTML = data;
                const calendar = document.querySelector(".calendar");
                if (calendar !== null) {
                    renderCalendar();
                    addEventListeners();
                };
            });
        });
    });
};

function renderCalendar() {
    let calendarShift = parseInt(document.querySelector(".calendar").dataset.shift);
    // Select all calendar squares and determine today's date for a base.
    const days = document.querySelectorAll(".day");
    const today = new Date();
    // Calculate a shift – i.e. how many days from the previous month should be placed to fill the first week.
    let shift = -(new Date(today.getFullYear(), today.getMonth() + calendarShift, 1).getDay() - 2);
    if (shift === 2) shift = -5;
    // If the calendar is rendered for future months, add previous months to the shift.
    for (let i = 0; i < calendarShift; i++) new Date(today.getFullYear(), today.getMonth() + i, 0);
    // Display back and forth buttons and the name of the month.
    const finishDay = new Date(today.getFullYear(), today.getMonth() + calendarShift + 1, 0);
    if (calendarShift === 0) document.querySelector(".back-button").setAttribute("hidden", "true");
    else document.querySelector(".back-button").removeAttribute("hidden");
    if (calendarShift === 3) document.querySelector(".forth-button").setAttribute("hidden", "true");
    else document.querySelector(".forth-button").removeAttribute("hidden");
    const month = document.querySelector(".month");
    document.querySelector(".month-name").innerHTML = finishDay.toLocaleString('default', { month: 'long' });
    // Fill calendar squares with the days.
    let length = days.length;
    for (let i = 0; i < length; i++) {
        let tempDate = new Date(today.getFullYear(), today.getMonth() + calendarShift, shift);
        // Display days from the next and previous months to fill the weeks.
        if (shift <= 0 || shift > finishDay.getDate()) {
            if (shift > finishDay.getDate() && length - i > 7) length -= 7;
            days[i].classList.add("non-current");
        }
        // Display days from the current month.
        else {
            if (tempDate.getDate() === today.getDate() && tempDate.getMonth() === today.getMonth()) days[i].classList.add("chosen", "current", "today");
            else {
                if (tempDate.getDate() === 1 && calendarShift > 0) days[i].classList.add("chosen");
                if (tempDate.getMonth() === today.getMonth() && tempDate.getDate() < today.getDate()) days[i].classList.add("disabled");
                days[i].classList.add("current");
            }
            days[i].dataset.date = `${tempDate.getFullYear()}-${tempDate.getMonth() + 1}-${tempDate.getDate()}`;
        };
        days[i].innerHTML = tempDate.getDate();
        shift++;
    };
    fetchTimes();
    handleDayClicks();
};

function addEventListeners() {
    let button = document.querySelector(".back-button");
    button.addEventListener("click", function() {
        let calendarShift = parseInt(document.querySelector(".calendar").dataset.shift);
        document.querySelector(".calendar").dataset.shift = calendarShift - 1;
        clearCalendar();
        renderCalendar();
    });
    button = document.querySelector(".forth-button");
    button.addEventListener("click", function() {
        let calendarShift = parseInt(document.querySelector(".calendar").dataset.shift);
        document.querySelector(".calendar").dataset.shift = calendarShift + 1;
        clearCalendar();
        renderCalendar();
    });
};

function clearCalendar() {
    document.querySelectorAll(".day").forEach((day) => {
        day.innerHTML = "";
        day.className = "day";
    });
};

function fetchTimes() {
    fetch(`${currentCompany}/${document.querySelector(".info").dataset.service}/${document.querySelector(".chosen").dataset.date}`).then(response => {
                return response.text()
            }).then(data => {
                document.querySelector(".time").innerHTML = data;
                const button = document.querySelector("#time");
                if (button !== null) {
                    document.querySelector("#time").addEventListener("click", (e) => {
                        e.preventDefault();
                        const value = document.querySelector("#id_appointment_start_time").value;
                        fetch(`${currentCompany}/${document.querySelector(".info").dataset.service}/${document.querySelector(".chosen").dataset.date}`, {
                            // Update status on the server side.
                            body: JSON.stringify({appointment_start_time: value}),
                            credentials: 'same-origin',
                            headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
                            method: 'POST'
                        }).then(response => response.json())
                        .then((data) => {
                            document.querySelector(".time").innerHTML = data["message"];
                        });
                    });
                };
            });
};

function handleDayClicks() {
    document.querySelectorAll(".day").forEach((day) => {
        console.log(day);
        if (!day.classList.contains("disabled") && day.classList.contains("current"))
        {
            day.addEventListener("click", dayClick);
        } else {
            day.removeEventListener("click", dayClick);
        };
    });
};

function dayClick() {
    console.log("click");
    document.querySelector(".chosen").classList.remove("chosen");
    this.classList.add("chosen");
    fetchTimes();
}