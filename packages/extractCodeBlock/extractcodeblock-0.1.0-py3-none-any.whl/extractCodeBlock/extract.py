import re

def extractCodeBlock(text):
    """
    Extracts content within triple backtick blocks and returns a list of dictionaries.
    Each dictionary has the block name as key and the corresponding block content as value.
    """
    pattern = re.findall(r"```([^\n]+)\n([\s\S]*?)```", text)
    
    ls_out = [{block_name.strip(): content.strip()} for block_name, content in pattern]
    
    return ls_out