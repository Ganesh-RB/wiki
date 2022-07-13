from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
import markdown

from . import util


def index(request):
    if request.method == "POST":
        return util.search_bar(request)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": util.NewSearchForm(),
            "random_page": util.random_entry()
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
        "form": util.NewSearchForm(),
        "random_page": util.random_entry()
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
        "form": util.NewSearchForm(),
        "random_page": util.random_entry()
    })


def new(request):
    if request.method == "POST":
        if "Save" not in request.POST:
            return util.search_bar(request)
        else:
            data = util.EditorForm(request.POST)
            if data.is_valid():
                title = data.cleaned_data["title"]
                content = data.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
            else:
                return render(request, "encyclopedia/editor.html", {
                    "form": util.NewSearchForm(),
                    "newPageForm": data,
                    "random_page": util.random_entry()
                })

    return render(request, "encyclopedia/editor.html", {
        "form": util.NewSearchForm(),
        "newPageForm": util.EditorForm(),
        "random_page": util.random_entry()
    })


def edit(request, title):
    if request.method == "POST":
        if "Save" not in request.POST:
            return util.search_bar(request)
        else:
            data = util.EditEntryForm(request.POST)
            if data.is_valid():
                content = data.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
            else:
                return render(request, "encyclopedia/editEntry.html", {
                    "form": util.NewSearchForm(),
                    "newPageForm": data,
                    "random_page": util.random_entry()
                })

    return render(request, "encyclopedia/editEntry.html", {
        "title": title,
        "form": util.NewSearchForm(),
        "newPageForm": util.EditEntryForm(initial={"title": title, "content": util.get_entry(title)}),
        "random_page": util.random_entry()
    })
