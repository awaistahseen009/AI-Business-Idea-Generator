from models import BusinessIdea
from typing import List, Dict, Any, Optional

class IdeaStorageService:
    """Service for storing and retrieving business ideas"""
    
    @staticmethod
    def save_ideas(user_id: int, niche: str, ideas: List[Dict[str, Any]], 
                   web_search_used: bool = False) -> Optional[BusinessIdea]:
        """
        Save generated business ideas to the database
        
        Args:
            user_id: ID of the user
            niche: The niche/industry for which ideas were generated
            ideas: List of generated business ideas
            web_search_used: Whether web search was used in generation
            
        Returns:
            BusinessIdea object if successful, None otherwise
        """
        try:
            return BusinessIdea.create(
                user_id=user_id,
                niche=niche,
                ideas=ideas,
                web_search_used=web_search_used
            )
        except Exception as e:
            print(f"Error saving ideas: {e}")
            return None
    
    @staticmethod
    def get_user_ideas(user_id: int, limit: int = 10) -> List[BusinessIdea]:
        """
        Get business ideas for a specific user
        
        Args:
            user_id: ID of the user
            limit: Maximum number of ideas to retrieve
            
        Returns:
            List of BusinessIdea objects
        """
        try:
            return BusinessIdea.get_by_user_id(user_id, limit)
        except Exception as e:
            print(f"Error retrieving user ideas: {e}")
            return []
    
    @staticmethod
    def get_idea_by_id(idea_id: int) -> Optional[BusinessIdea]:
        """
        Get a specific business idea by its ID
        
        Args:
            idea_id: ID of the business idea
            
        Returns:
            BusinessIdea object if found, None otherwise
        """
        try:
            return BusinessIdea.get_by_id(idea_id)
        except Exception as e:
            print(f"Error retrieving idea by ID: {e}")
            return None
    
    @staticmethod
    def validate_ideas_format(ideas: List[Dict[str, Any]]) -> bool:
        """
        Validate that ideas have the correct format
        
        Args:
            ideas: List of idea dictionaries to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        if not isinstance(ideas, list) or len(ideas) != 3:
            return False
        
        required_keys = {'name', 'pitch', 'audience', 'revenue_model'}
        
        for idea in ideas:
            if not isinstance(idea, dict):
                return False
            
            if not all(key in idea for key in required_keys):
                return False
            
            if not all(isinstance(idea[key], str) and idea[key].strip() for key in required_keys):
                return False
        
        return True
