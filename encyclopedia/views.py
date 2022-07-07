from django import forms
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
import markdown

from . import util


def index(request):
    if request.method == "POST":
        return util.search_bar(request)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": util.NewSearchForm()
        })


def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return HttpResponseNotFound(request)

    html = markdown.markdown(content)

    if request.method == "POST":
        return util.search_bar(request)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html,
        "form": util.NewSearchForm()
    })


def search_similar(request, title):
    if request.method == "POST":
        return util.search_bar(request)

    search_entries = []
    for entry in util.list_entries():
        if title.lower() in entry.lower():
            search_entries += [entry]

    return render(request, "encyclopedia/search.html", {
        "entries": search_entries,
        "form": util.NewSearchForm()
    })


def new(request):
    if request.method == "POST":
        data = util.CreateNewPageForm(request.POST)
        if data.is_valid():
            title = data.cleaned_data["title"]
            content = data.cleaned_data["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/new.html", {
                "form": util.NewSearchForm(),
                "newPageForm": data
            })

    return render(request, "encyclopedia/new.html", {
        "form": util.NewSearchForm(),
        "newPageForm": util.CreateNewPageForm()
    })
