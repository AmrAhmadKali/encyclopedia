from django.shortcuts import render

from . import util
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from django.urls import reverse
from django import forms
from random import randint

class NewEntryForm(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(widget=forms.Textarea, label="Enter your content here")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title) 
    if content is not None:
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })    
    return HttpResponse(f"{title}\n The requested Page not found")
    

def search(request):
    # get the search term from the request/URL
    search_term = request.GET['q']
    # list of all entries available
    entry_names = util.list_entries()
    results = []
    if search_term in entry_names:
        return HttpResponseRedirect(reverse("entry", args = (search_term,)))
    else:
        for entry_name in entry_names:
            if search_term in entry_name:
                results.append(entry_name)
        return render(request, "encyclopedia/search.html", {
            "results":results
        })


def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["title"] not in util.list_entries():
                util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
                return HttpResponseRedirect(reverse("entry", args = (form.cleaned_data["title"],)))  #??
            return HttpResponse(f"Error: the title {form.cleaned_data['title']} already exists")    
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })


def edit(request, title):
    if request.method =="POST":
        util.save_entry(title, request.POST["edited_content"])
        return HttpResponseRedirect(reverse("entry", args=(title,)))   
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content    
        })
    

def random(request):
    entries = util.list_entries()
    random_entry = entries[randint(0, len(entries)-1)]
    return entry(request, random_entry)
