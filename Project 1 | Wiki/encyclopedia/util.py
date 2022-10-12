import markdown2, random, re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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


def get_entry(title, type):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        if type is "html":
            return markdown2.markdown(f.read().decode("utf-8"))
        else:
            return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def pick_random():
    """
    Returns a random encyclopedia entry from the storage.
    """
    title = random.choice(list_entries())
    return get_entry(title, "html"), title


def search(title):
    """
    Returns all encyclopedia entries that have the query as a substring.
    """
    return [x for x in list_entries() if re.search(title, x, re.IGNORECASE)]