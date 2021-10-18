# -*- coding: utf-8 -*-
from browser import html
from ._base import global_state, Base
from urllib.parse import urlparse


class Video:
    def __init__(self, src:str, poster:str = None, autoplay:bool = False, **attrs):
        if src.startswith("http://") or src.startswith("https://"):
            try:
                urlparse(src)
                if "www.youtube.com/" in src or "youtu.be/" in src and not "embed" in src:
                    if "www.youtube.com/" in src:
                        splitter = "www.youtube.com/"
                    else:
                        splitter = "youtu.be/"
                    
                    video_id = src.split(splitter)[-1]
                    src = f"https://www.youtube.com/embed/{video_id}"

                if autoplay:
                    if "?" in src:
                        src += "&autoplay=1"
                    else:
                        src += "?autoplay=1"
                element = html.IFRAME(src = src, frameborder = "0", allow = "accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture", **attrs)
            except:
                pass
        else:
            element = html.VIDEO(src = src, poster = poster, crossorigin = "*", **attrs)
            if autoplay:
                element.setAttribute("autoplay", "")

        global_state.current_layout <= element

class Audio(Base, html.AUDIO):
    def __init__(self, src:str, controls:bool = True, autoplay:bool = False, **attrs):
        html.AUDIO.__init__(self, src = src, crossorigin = "*")
        Base.__init__(self, **attrs)

        if controls:
            self.setAttribute("controls", "")

        if autoplay:
            self.setAttribute("autoplay", "")
