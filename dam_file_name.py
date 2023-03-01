from pathlib import Path
import re
from urllib.parse import unquote, urlparse

class DamFileName:
    
    def __init__(self):
        self.special_chars = re.compile('[^a-zA-Z0-9_\-\s/]')
        self.special_chars_w_space = re.compile('[^a-zA-Z0-9_\-/]')
        self.spaces_undescores_hyphen_chars = re.compile('[_\s\-]+')
        self.multiple_spaces_underscores_hyphens_chars = re.compile('[_\s\-]{2,}')

    def create_proper_name(self, filename):
        """Takes a filename and returns a modified filename per the Capgemini rules

        Args:
            filename (str): The filename we want to make proper
        
        Returns:
            proper_filename (str): The modified filename per the Capgemini rules
        """
        filename = Path(filename)
        stem = filename.stem
        suffix = filename.suffix
        proper_stem = self._fix_special_chars(stem)
        if suffix:
            proper_suffix = '.' + self._fix_special_chars(suffix)
        else:
            proper_suffix = ''
        proper_name = f'{proper_stem}{proper_suffix}'
        return proper_name
    
    def create_proper_name_wo_suffix(self, filename):
        """Takes a filename and returns a modified filename per the Capgemini rules

        Args:
            filename (str): The filename we want to make proper
        
        Returns:
            proper_filename (str): The modified filename per the Capgemini rules
        """
        proper_filename = self._fix_special_chars(filename)        
        return proper_filename

    def _fix_special_chars(self, string):
        wo_special_chars = re.sub(self.special_chars, '-', string.lower().strip())
        wo_spaces_undescores_chars = re.sub(self.spaces_undescores_hyphen_chars, '-', wo_special_chars)
        wo_spaces_undescores_chars = re.sub(self.multiple_spaces_underscores_hyphens_chars, '-', wo_spaces_undescores_chars) # to eliminate multiple '-'
        wo_spaces_undescores_chars = wo_spaces_undescores_chars.strip('-')
        return wo_spaces_undescores_chars

    def is_proper_url(self, url):
        """Takes a url and returns True if it's proper (no special chars) 
        else it returns False

        Args:
            url (str): The filename we want to make proper
        
        Returns:
            (bool): True if the filename doesn't contain special chars, False otherwise
        """
        path = urlparse(url).path 
        matchgroup = self.special_chars_w_space.search(path)
        if matchgroup:
            return True
        matchgroup = self.multiple_spaces_underscores_hyphens_chars.search(path)
        if matchgroup:
            return True
        return False