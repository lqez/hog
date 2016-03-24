# hog - Sending multiple HTTP requests ON GREEN thread.

version_info = (0, 1, 7)

__version__ = VERSION = '.'.join(map(str, version_info))
__project__ = PROJECT = 'hog'
__author__ = AUTHOR = "Park Hyunwoo <ez.amiryo@gmail.com>"


from .hog import print_result, run
