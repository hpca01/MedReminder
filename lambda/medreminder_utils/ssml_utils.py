#!/usr/bin/python
import warnings

class TextHelper:
    def __init__(self):
        self._output = []

    def __repr__(self) -> str:
        return "".join(self._output)

    def sentence(self, input: str)->'TextHelper':
        sentence_tag = "<s>{}</s>"
        self._output.append(sentence_tag.format(input))
        return self
    
    def pause(self, input:int):
        break_tag="<break time=\"{number}s\"/>"
        pause_secs = None
        if type(input) is not int:
            raise Exception("Only numbers allowed, less than 10")
        elif input>10:
            warnings.warn("Number should be 10 or less")
            pause_secs = 10
        pause_secs = input
        self._output.append(break_tag.format(number = pause_secs))
        return self

    def paragraph(self, input: str):
        paragraph_tag = "<p>{}</p>"
        self._output.append(paragraph_tag.format(input))
        return self

    def speak(self, input: str):
        self._output.append(input)
        return self
    
    def emphasis(self, input:str, level=None):
        emphasis_tag = "<emphasis level=\"{level}\">{input}</emphasis>"
        if level is None or (level not in ['strong', 'moderate', 'reduced']):
            raise Exception('Incorrect use of SSML tag emphasis, please include correct strength')
        else:
            self._output.append(emphasis_tag.format(level=level, input=input))
        return self

    def to_string(self)->str:
        return self.__repr__()

class NumberHelper:
    def __init__(self):
        pass

class SSMLHelper:
    def __init__(self):
        self._obj = None

    def get_text_helper(self):
        self._obj = TextHelper()
        return self._obj

    def get_number_helper(self):
        self._obj = NumberHelper()
        return self._obj
    
    def build(self):
        return str(self._obj)
