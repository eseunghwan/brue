# -*- coding: utf-8 -*-

class FileReader:
    @property
    def result(self) -> str:
        return ""

    def onload(self):
        pass

    def readAsText(self, source:str, encoding:str):
        pass

class JSON:
    def parse(self, source:str) -> dict:
        return {}

    def stringify(self, source:dict) -> str:
        return ""
