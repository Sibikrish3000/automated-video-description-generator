class PromptEngineer:
    def __init__(self, template: str):
        self.template = template

    def build_prompt(self, frames):
        #could add frame count or other info
        return self.template 