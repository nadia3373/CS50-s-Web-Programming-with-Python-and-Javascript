from django import forms
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError

from . import util

class EntryForm(forms.Form):
    content = forms.CharField(label="Entry content", widget=forms.Textarea)

class NewEntryForm(EntryForm):
    title = forms.CharField(label="Entry title")


def add(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title, "html"):
                return render(request, "encyclopedia/add.html", {
                    "error": "A page with this name already exists. Please choose another name.",
                    "form": form
                })
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(f"wiki/{title}")
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })


def edit(request, title):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(f"/wiki/{title}")
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": util.get_entry(title, "markdown"),
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title, "html"),
        "link": title,
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def random(request):
    entry, title = util.pick_random()
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "link": title,
    })


def search(request):
    try:
        q = request.GET['q']
        entry = util.get_entry(title=q, type="html")
        if q == "":
            return redirect("/")
        if entry is not None:
            return render(request, "encyclopedia/entry.html", {
                "entry": entry,
                "link": q,
            })
        return render(request, "encyclopedia/search.html", {
            "entries": util.search(q),
            "query": q,
        })
    except MultiValueDictKeyError:
        return redirect("/")
