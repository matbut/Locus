def is_valid(url):
    return True


def clean_url(url):
    return url.split('?')[0].split('#')[0]
