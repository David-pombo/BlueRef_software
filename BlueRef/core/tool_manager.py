from enum import Enum

class ToolType(Enum):
    SELECT = 1
    SCALE = 2
    ROTATE = 3  # optional for future

class ToolManager:
    def __init__(self):
        self.current_tool = ToolType.SELECT

    def set_tool(self, tool: ToolType):
        self.current_tool = tool

    def get_tool(self):
        return self.current_tool
