# hog - Sending multiple HTTP requests ON GREEN thread.

version_info = (0, 1, 4)

__version__ = version = '.'.join(map(str, version_info))
__project__ = PROJECT = 'django-summernote'
__author__ = AUTHOR = "Park Hyunwoo <ez.amiryo@gmail.com>"


from .hog import run
