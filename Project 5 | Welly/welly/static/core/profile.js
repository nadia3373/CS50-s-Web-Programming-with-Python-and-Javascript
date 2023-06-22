document.querySelectorAll(".appointments-created>div, .appointments-confirmed>div").forEach((e) => {
    let card = e.querySelector(".appointment-card-body").querySelector(".appointment-card-content");
    console.log(card);
    let button = document.createElement("a");
    button.href = `/companies/${company}/cancel/${e.dataset.id}`;
    button.classList.add("btn", "btn-outline-danger");
    button.innerHTML = "Cancel";
    card.append(button);
});