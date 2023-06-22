let button = document.querySelector(".menu-button.active");
const content = document.querySelector(".content");
let status = 0;
document.querySelectorAll(".menu-button").forEach(button => {
    button.addEventListener("click", (e) => {
        button = e.target;
        fetchData(button);
        document.querySelector(".menu-button.active").classList.remove("active");
        e.target.classList.add("active");
    })
});

fetchData(button);

function addImageButtons() {
    document.querySelectorAll(".image-wrapper").forEach((e) => {
        let badge = document.createElement("span");
        badge.classList.add("position-absolute", "top-0", "start-100", "translate-middle", "badge", "rounded-pill", "bg-danger");
        badge.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                              <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"/>
                            </svg>`;
        badge.addEventListener("click", function() {
            deleteImage(this, this.parentElement.dataset.id);
        });
        e.appendChild(badge);
    });
}

function deleteImage(img, id) {
    fetch(`delete_image/${id}`).then(response => {
        return response.text()
    }).then(data => {
        img.parentElement.remove();
    });
}

function fetchData(button) {
    switch (button.dataset.type) {
        case "gallery":
            fetch(`gallery`).then(response => {
                return response.text()
            }).then(data => {
                content.innerHTML = data;
                let button = document.createElement("a");
                button.classList.add("btn", "btn-primary", "confirm-button");
                button.innerHTML = "Upload images";
                document.querySelector(".content").insertBefore(button, document.querySelector(".content").children[0]);
                addImageButtons();
                button.addEventListener("click", (e) => {
                    fetch(`gallery_management`).then(response => {
                        return response.text()
                    }).then(data => {
                        content.innerHTML = data;
                    });
                });
            });
            break;
        case "settings":
            fetch(`company_settings`).then(response => {
                return response.text()
            }).then(data => {
                content.innerHTML = data;
                document.querySelector(".save-settings").addEventListener("submit", (e) => {
                    handleFormSubmission(e);
                });
            });
            break;
        case "appointments":
            fetch(`appointments`).then(response => {
                window.location.href = response.url;
            });
            break;
        case "wh":
            fetch(`wh`).then(response => {
                window.location.href = response.url;
            });
            break;
        default:
            fetch(`services`).then(response => {
                    return response.text()
                }).then(data => {
                    content.innerHTML = data;
                    let button = document.createElement("a");
                    button.classList.add("btn", "btn-primary", "confirm-button");
                    button.href = "add_service";
                    button.innerHTML = "New service";
                    document.querySelector(".content").insertBefore(button, document.querySelector(".service-card"));
                    handleServices();
                });
                break;
    }
};

function handleFormSubmission(e) {
    e.preventDefault();
    const formData = new FormData();
    const clear = document.getElementById("logo-clear_id");
    if (clear !== null) {
        if (clear.value === "on") {
            formData.append('logo-clear', "on");
        };
    };
    formData.append('country', document.getElementById("id_country").value);
    formData.append('city', document.getElementById("id_city").value);
    formData.append('street', document.getElementById("id_street").value);
    formData.append('building', document.getElementById("id_building").value);
    formData.append('office', document.getElementById("id_office").value);
    formData.append('name', document.getElementById("id_name").value);
    formData.append('description', document.getElementById("id_description").value);
    formData.append('logo', document.getElementById("id_logo").files[0]);
    fetch('company_settings', {
        credentials: 'same-origin',
        headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        method: 'POST',
        body: formData
    }).then(response => {
        status = response.status;
        return response.text();
    }).then(data => {
        content.innerHTML = data;
        document.querySelector(".save-settings").addEventListener("submit", (e) => {
            handleFormSubmission(e);
        });
        console.log(status);
        if (status === 200) {
            const header = document.querySelector(".header");
            const alert = document.createElement("div");
            alert.classList.add("alert", "alert-success");
            alert.role = "alert";
            alert.innerHTML = "Company settings successfully updated";
            header.insertBefore(alert, header.children[header.children.length]);
            setTimeout(function() {
                alert.remove();
            }, 2000);
        };
    });
}

function handleServices() {
    document.querySelectorAll(".service-card").forEach((service) => {
        service.addEventListener("click", (e) => {
            fetch(`edit_service/${service.dataset.id}`).then(response => {
                window.location.href = response.url;
            });
        });
    });
};