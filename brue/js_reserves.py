# -*- coding: utf-8 -*-

class FileReader:
    @property
    def result(self) -> str:
        return ""

    def onchange(self):
        pass

class JSON:
    def parse(self, source:str) -> dict:
        return {}

    def stringify(self, source:dict) -> str:
        return ""
