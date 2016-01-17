class with_any_prompt():
    def __eq__(self, other):
        return isinstance(other, str)
