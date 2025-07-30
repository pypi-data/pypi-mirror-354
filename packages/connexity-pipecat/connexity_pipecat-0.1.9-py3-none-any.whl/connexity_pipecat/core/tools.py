from pipecat_tools import ToolManager

tool_manager = ToolManager()

def register_custom_tools(handlers_dir, config_file):
    tool_manager.register_tools_from_directory(
        handlers_dir=handlers_dir,
        config_file=config_file
    )
    return tool_manager


def get_tool_manager():
    """
    Return the current global ToolManager instance, reflecting all registrations.
    """
    return tool_manager