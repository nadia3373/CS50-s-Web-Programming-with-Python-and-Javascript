export function editButton() {
    const button = document.querySelector(".edit");
    if (button) {
        button.addEventListener('click', function(e) {
            // Replace post content with a textarea.
            const content = document.querySelector('.content');
            const textarea = document.createElement("textarea");
            textarea.value = content.querySelector('.text').innerHTML;
            textarea.name = "edit-textarea";
            textarea.maxLength = 280;
            content.append(textarea);
            textareaTweaks();
            content.querySelector('.text').remove();
            button.remove();
            // Add a "save" button."
            const save = document.createElement("a");
            save.className = `btn btn-outline-info btn-sm save`;
            save.setAttribute("data-id", this.dataset.id);
            save.innerHTML = `
            Save
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-save2-fill" viewBox="0 0 16 16">
                <path d="M8.5 1.5A1.5 1.5 0 0 1 10 0h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h6c-.314.418-.5.937-.5 1.5v6h-2a.5.5 0 0 0-.354.854l2.5 2.5a.5.5 0 0 0 .708 0l2.5-2.5A.5.5 0 0 0 10.5 7.5h-2v-6z"/>
            </svg>`;
            document.querySelector('.edit-button').append(save);
            // Handle post saving.
            save.addEventListener('click', function(e) {
                fetch(`/edit/${this.dataset.id}`, {
                    // Update status on the server side.
                    credentials: 'same-origin',
                    headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    method: 'PUT',
                    body: JSON.stringify({"content": textarea.value})
                }).then(response => {if (!response.ok) throw response})
                .then(() => {
                    // Update affected elements.
                    const text = document.createElement('p');
                    text.className = "text";
                    text.innerHTML = textarea.value;
                    textarea.remove();
                    save.remove();
                    content.append(text);
                    const edit = document.querySelector('.edit-button').innerHTML = `
                    <a class="btn btn-outline-info btn-sm edit" data-id="${this.dataset.id}"href=#>
                        Edit
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                            <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
                        </svg>
                    </a>`;
                    editButton();
                })
                // Otherwise display the error received from the server.
                .catch(error => {error.json().then((error) => showAlert(error))});
            });
        });
    }
}

// Handle "Like" and Follow" buttons.
export function getButtons(action) {
    let address, className;
    if (action === "like") {
        address = "/like/";
        className = ".like";
    } else {
        address = "/follow/";
        className = ".follow";
    }
    document.querySelectorAll(className).forEach((button) => {
        displayStatus(button, action);
        button.addEventListener('click', function(e) {
            fetch(`${address}${this.dataset.id}`, {
                // Update status on the server side.
                credentials: 'same-origin',
                headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
                method: 'PUT'  
            }).then(response => response.json())
            .then((i) => {
                // Update status on the client side
                button.dataset.status = i["status"];
                // Update affected elements.
                displayStatus(button, action);
                if (action === "like") {
                    button.parentElement.querySelector('.count').innerHTML = ` ${i["likes"]}`;
                } else {
                    if (i["followers"] === 0) {
                        const nofollowers = document.createElement("div");
                        nofollowers.className = "no-followers";
                        nofollowers.innerHTML = `${i["user"]} has no followers yet.`;
                        document.querySelector(".followers").append(nofollowers);
                    } else {
                        const nofollowers = document.querySelector(".no-followers");
                        if (nofollowers) {nofollowers.remove();}
                    }
                }
            });
        })
    });
}

// Update state for "Like" and "Follow" buttons.
function displayStatus(button, action) {
    if (action === "like") {
        if (button.dataset.status === "true") {
            // if the post is liked by the current user, display a "Liked" button.
            button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-suit-heart-fill" viewBox="0 0 16 16">
                <path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/>
            </svg>`;
        } else {
            // Otherwise display a "Like" button.
            button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-suit-heart" viewBox="0 0 16 16">
                <path d="m8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2 2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446 6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784 0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281 2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z"/>
            </svg>`;
        }
    } else {
        if (button.dataset.status === "true") {
            button.innerHTML = `
            Following
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-dash-fill" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M11 7.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5z"/>
                <path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
            </svg>`;
            let follower = document.querySelector(".follower-you");
            if (!follower) {
                follower = document.createElement("a");
                follower.className = "follower-you";
                follower.setAttribute("href", button.dataset.url);
                follower.innerHTML = "You";
                document.querySelector(".followers").append(follower);
            }
        } else {
            button.innerHTML = `
            Follow
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-plus-fill" viewBox="0 0 16 16">
                <path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                <path fill-rule="evenodd" d="M13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"/>
            </svg>`;
            const follower = document.querySelector(".follower-you");
            if (follower) {
                follower.remove();
            }
        }
    }
}

function showAlert(message) {
    const alert = document.createElement("div");
    alert.className = "alert alert-danger";
    alert.innerHTML = `Error: ${message.error}`;
    document.querySelector('container').insertBefore(alert, document.querySelector('.post-title'));
  }

export function textareaTweaks() {
    const inputs = document.querySelectorAll('input[type="text"], textarea');
    inputs.forEach((input) => {
        input.addEventListener('keyup', function() {
            if (this.value.length >= this.maxLength) {
                this.className = "form-control is-invalid info";
                let info = document.querySelector(`.invalid-feedback.info.${this.name}`);
                if (!info) {
                    info = document.createElement('div');
                    info.className = `invalid-feedback info ${this.name}`;
                    info.innerHTML = `Maximum length reached (max. ${this.maxLength})`;
                    this.after(info);
                }
            } else {
                this.className = "";
                const info = document.querySelector(`.invalid-feedback.info.${this.name}`);
                if (info) {
                    info.remove();
                }
            }
        })
    })
}