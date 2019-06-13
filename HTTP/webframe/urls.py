"""
    规定能解析的请求格式
"""
from views import *

urls = [
    ('/time', show_time),
    ('/hello', say_hello),
    ('/bye', say_bye)
]

