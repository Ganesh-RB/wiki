from random import randint
import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django import forms
from django.http import Http404, HttpResponseRedirect


class NewSearchForm(forms.Form):
    q = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'class': 'search', 'placeholder': 'Search Encyclopedia'}))


class EditorForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter page title here'}))

    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={"placeholder": "Enter Markdown content here", 'class': 'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        if get_entry(title) != None:
            raise forms.ValidationError("title already exists")

        return title


class EditEntryForm(forms.Form):
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search_bar(request):
    """
    Check for the submission of form through POST method and retrun response
    """
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["q"]
            if get_entry(title) != None:
                return HttpResponseRedirect(f"/wiki/{title}")
            else:
                return HttpResponseRedirect(f"/search/{title}")

        else:
            return Http404(request)
    else:
        return Http404(request)


def random_entry():
    entries = list_entries()
    if entries:
        return entries[randint(0,len(entries)-1)]
    else:
        return None