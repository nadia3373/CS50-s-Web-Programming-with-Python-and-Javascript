let appointments = document.querySelector(".appointments-created");
if (appointments !== null) {
    renderButtons(appointments, "both");
};
appointments = document.querySelector(".appointments-confirmed");
if (appointments !== null) {
    renderButtons(appointments, "cancel");
};
appointments = document.querySelector(".appointments-cancelled");
if (appointments !== null) {
    renderButtons(appointments, "confirm");
};

function renderButtons(appointments, types) {
        Array.from(appointments.children).forEach((e) => {
        let buttons = e.querySelector(".appointment-buttons");
        if (buttons !== null) {
            if (types === "both")
            {
                buttons.innerHTML = `<div class="cancel">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red" class="bi bi-x-square-fill" viewBox="0 0 16 16">
                                      <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm3.354 4.646L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708z"/>
                                    </svg>
                                </div>
                                <div class="confirm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="green" class="bi bi-check-square-fill" viewBox="0 0 16 16">
                                      <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z"/>
                                    </svg>
                                </div>`;
            } else if (types === "cancel") {
                buttons.innerHTML = `<div class="cancel">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red" class="bi bi-x-square-fill" viewBox="0 0 16 16">
                                          <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm3.354 4.646L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708z"/>
                                        </svg>
                                    </div>`;
            } else if (types === "confirm") {
                buttons.innerHTML = `<div class="confirm">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="green" class="bi bi-check-square-fill" viewBox="0 0 16 16">
                                          <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z"/>
                                        </svg>
                                    </div>`;
            };
        };
    });
}

handleButtons()

function handleButtons() {
    document.querySelectorAll(".confirm").forEach((e) => {
        e.addEventListener("click", function() {
            fetch(`/companies/${company}/confirm/${this.parentElement.parentElement.dataset.id}`).then(response => {
                window.location.href = response.url;
            });
        });
    });
    document.querySelectorAll(".cancel").forEach((e) => {
        e.addEventListener("click", function() {
            console.log(this);
            fetch(`/companies/${company}/cancel/${this.parentElement.parentElement.dataset.id}`).then(response => {
                window.location.href = response.url;
            });
        });
    });
}