import emoji
from typing import Dict, List

class EmojiDataset:
    """
    A class to handle emoji data and provide functionalities for the emoji search application.
    """
    
    def __init__(self):
        """Initialize the EmojiDataset class by loading emoji data."""
        self.emoji_data = self._load_emoji_data()
        
    def _load_emoji_data(self) -> List[Dict[str, str]]:
        """
        Load emoji data from emoji package and format it for the application.
        
        Returns:
            List[Dict[str, str]]: A list of emoji dictionaries containing emoji, name, and group.
        """
        emoji_list = []
        
        # Get all emoji data from the emoji package
        for emoji_code, emoji_name in emoji.EMOJI_DATA.items():
            # Skip emoji with skin tone modifiers
            if any(modifier in emoji_code for modifier in ['1F3FB', '1F3FC', '1F3FD', '1F3FE', '1F3FF']):
                continue
                
            # Extract information
            name = emoji_name.get('en', '').replace('_', ' ').title()
            
            # Some emoji groups
            group = None
            if "face" in name.lower() or "emotion" in name.lower():
                group = "Faces & Emotions"
            elif "hand" in name.lower() or "person" in name.lower():
                group = "People & Body"
            elif "flag" in name.lower():
                group = "Flags"
            elif "food" in name.lower() or "drink" in name.lower() or "fruit" in name.lower():
                group = "Food & Drink"
            elif "animal" in name.lower() or "plant" in name.lower():
                group = "Animals & Nature"
            elif "travel" in name.lower() or "place" in name.lower():
                group = "Travel & Places"
            elif "activity" in name.lower() or "sport" in name.lower():
                group = "Activities"
            elif "object" in name.lower() or "tool" in name.lower():
                group = "Objects"
            elif "symbol" in name.lower():
                group = "Symbols"
            else:
                group = "Other"
                
            # Create keywords from the name
            keywords = name.lower().split()
            
            emoji_list.append({
                "emoji": emoji_code,
                "name": name,
                "group": group,
                "keywords": keywords
            })
            
        return emoji_list
    
    def get_all_emojis(self) -> List[Dict[str, str]]:
        """
        Get all emojis in the dataset.
        
        Returns:
            List[Dict[str, str]]: A list of all emoji dictionaries.
        """
        return self.emoji_data
    
    def get_emoji_by_group(self, group: str) -> List[Dict[str, str]]:
        """
        Get emojis filtered by group.
        
        Args:
            group (str): The emoji group to filter by.
            
        Returns:
            List[Dict[str, str]]: A list of emoji dictionaries filtered by group.
        """
        return [e for e in self.emoji_data if e.get("group") == group]
    
    def get_emoji_groups(self) -> List[str]:
        """
        Get all emoji groups in the dataset.
        
        Returns:
            List[str]: A list of all emoji groups.
        """
        return sorted(list(set(e.get("group") for e in self.emoji_data if e.get("group"))))
    
    def format_for_frontend(self) -> List[Dict[str, str]]:
        """
        Format the emoji data for the frontend.
        
        Returns:
            List[Dict[str, str]]: A list of emoji dictionaries formatted for frontend.
        """
        formatted_data = []
        for item in self.emoji_data:
            formatted_data.append({
                "emoji": emoji.emojize(item["emoji"]),
                "name": item["name"],
                "group": item["group"]
            })
        return formatted_data

emoji_dataset = EmojiDataset()
