document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';
  if (document.querySelector(".alert")) document.querySelector(".alert").remove();

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Autofocus the first field.
  document.querySelector('#compose-recipients').focus();

  // Handle form submission.
  document.querySelector("#compose-form").onsubmit = (event) => {
    event.preventDefault();
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => {if (!response.ok) throw response})
    // After submission load the "Sent" mailbox if successful.
    .then(() => {
        load_mailbox("sent");
        showAlert({"success": "Email has been sent successfully."});
    })
    // Else display the error received from the server.
    .catch(error => {error.json().then((error) => showAlert(error))});
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#email-content').innerHTML = "";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Request the emails for the current mailbox.
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Display the emails.
      displayEmails(emails, mailbox);
  });
}

function displayEmails(emails, mailbox) {
  if (emails.length === 0) document.querySelector("#emails-view").innerHTML = `<h3>There are no emails yet.</h3>`;
  for (const i in emails) {
    const emailBox = document.createElement("div");
    emailBox.className = "emails";
    emailBox.setAttribute("data-id", emails[i].id);
    document.querySelector('#emails-view').append(emailBox);
    let prefix = "";
    let address = "";
    if (mailbox === "inbox" || mailbox === "archive") {
      prefix = "From: ";
      address = emails[i].sender;
      if (!emails[i].read) {
        emailBox.className = "emails not-read";
      }
    } else if (mailbox === "sent") {
      prefix = "To: ";
      emails[i].recipients.length === 1 ? address = emails[i].recipients[0] : address = `${emails[i].recipients[0]}, ...`;
    }

    // Display sender address.
    addressBlock = document.createElement("div");
    addressBlock.className = "address";
    addressBlock.innerHTML = `${prefix}${address}`;
    emailBox.append(addressBlock);

    // Display subject.
    subjectBlock = document.createElement("div");
    subjectBlock.className = "subject";
    subjectBlock.innerHTML = emails[i].subject;
    emailBox.append(subjectBlock);
    
    // Display timestamp.
    timestampBlock = document.createElement("div");
    timestampBlock.className = "timestamp";
    timestampBlock.innerHTML = emails[i].timestamp;
    emailBox.append(timestampBlock);

    // Open email when it is clicked.
    emailBox.addEventListener("click", function() {
      loadEmail(this.dataset.id, mailbox);
    })
  }
}

function loadEmail(id, mailbox) {
  // Request the email by its id.
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Display the email.
      showEmail(email, mailbox);
    })
}

function showEmail(email, mailbox) {
  // Mark the email as read.
  if (!email.read) {
    toggleState(email.id, {read: true});
  }

  // Show the email content view and hide other views.
  document.querySelector('#emails-view').style.display = 'none';
  const view = document.querySelector('#email-content');
  view.style.display = "block";

  // Display sender address.
  const values = {"From: ": email.sender, "To: ": email.recipients, "Subject: ": email.subject, "Timestamp: ": email.timestamp};
  for (const i in values) {
    const row = document.createElement("div");
    row.innerHTML = `<strong>${i}</strong>`;
    if (i !== "To: "){
      row.innerHTML += `${values[i]}`;
    } else {
      for (j in email.recipients) {
        row.innerHTML += email.recipients[j];
        if (Number(j) < email.recipients.length - 1) {
          row.innerHTML += ", ";
        }
      }
    }
    view.append(row);
  }

  // Display "Reply" button.
  let button = document.createElement("button");
  button.className = "btn btn-sm btn-outline-primary";
  button.innerHTML = "Reply";
  view.append(button);

  // When the "Reply" button is clicked, open compose view and fill the form with current email's data.
  button.addEventListener("click", function() {
    compose_email();
    reply(email);
  });

  // For "Inbox" and "Archive" views display "Archive/Unarchive" button.
  if (mailbox !== "sent") {
    button = document.createElement("button");
    button.className = "btn btn-sm btn-outline-primary";
    email.archived ? button.innerHTML = "Unarchive" : button.innerHTML = "Archive";
    view.append(button);
    button.addEventListener("click", function() {
      toggleState(email.id, {archived: !email.archived});      
    });
  }

  // Add a border.
  const border = document.createElement("hr");
  view.append(border);

  // Display the body of the email.
  const body = document.createElement("p");
  body.innerHTML = email.body;
  view.append(body);
}

// Pre-fill email sender, subject and body for a reply.
function reply(email) {
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.startsWith("Re: ")) {
    document.querySelector('#compose-subject').value = email.subject;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#compose-body').focus();
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}\n-----------------------------------------------------\n`;
}

// Handle email reading, archiving and unarchiving.
function toggleState(id, body) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  })
  // After archiving or unarchiving load the "Inbox" mailbox.
  .then(() => {if ("archived" in body) load_mailbox("inbox");})
}

// Show success or error alerts. 
function showAlert(message) {
  const alert = document.createElement("div");
  alert.className = "alerts";
  let alertClass, elementId, text;
  if ("error" in message) {
    alertClass = "alert alert-danger";
    elementId = "#compose-view";
    text = `Error: ${message.error}`;
  } else {
    alertClass = "alert alert-success";
    elementId = "#emails-view";
    text = `Success: ${message.success}`;
  }
  alert.className = alertClass;
  alert.innerHTML = text;
  document.querySelector(elementId).insertBefore(alert, document.querySelector(elementId).firstChild);
}