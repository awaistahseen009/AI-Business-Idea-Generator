from supabase import create_client, Client
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

class Database:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.url or not self.key or not self.service_role_key:
            raise ValueError("SUPABASE_URL, SUPABASE_KEY, and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
        
        self.client: Client = create_client(self.url, self.key)
        self.service_client: Client = create_client(self.url, self.service_role_key)

    def get_client(self) -> Client:
        return self.client

    def get_service_role_client(self) -> Client:
        return self.service_client

# Initialize database connection
db = Database()

class User:
    def __init__(self, id: int = None, email: str = None, password_hash: str = None, 
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(email: str, password_hash: str) -> Optional['User']:
        """Create a new user in the database"""
        try:
            # Use service role client to bypass RLS for user creation
            result = db.get_service_role_client().table('users').insert({
                'email': email,
                'password_hash': password_hash,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }).execute()
            
            if result.data:
                user_data = result.data[0]
                return User(
                    id=user_data['id'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    created_at=user_data['created_at'],
                    updated_at=user_data['updated_at']
                )
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def get_by_email(email: str) -> Optional['User']:
        """Get user by email"""
        try:
            # Use service role client to bypass RLS for checking user existence
            result = db.get_service_role_client().table('users').select('*').eq('email', email).execute()
            
            if result.data:
                user_data = result.data[0]
                return User(
                    id=user_data['id'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    created_at=user_data['created_at'],
                    updated_at=user_data['updated_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional['User']:
        """Get user by ID"""
        try:
            # Use service role client to bypass RLS for user lookups
            result = db.get_service_role_client().table('users').select('*').eq('id', user_id).execute()
            
            if result.data:
                user_data = result.data[0]
                return User(
                    id=user_data['id'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    created_at=user_data['created_at'],
                    updated_at=user_data['updated_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

class BusinessIdea:
    def __init__(self, id: int = None, user_id: int = None, niche: str = None,
                 ideas: List[Dict[str, Any]] = None, web_search_used: bool = False,
                 created_at: datetime = None):
        self.id = id
        self.user_id = user_id
        self.niche = niche
        self.ideas = ideas or []
        self.web_search_used = web_search_used
        self.created_at = created_at
    
    @staticmethod
    def create(user_id: int, niche: str, ideas: List[Dict[str, Any]], 
               web_search_used: bool = False) -> Optional['BusinessIdea']:
        """Create a new business idea record in the database"""
        try:
            result = db.get_service_role_client().table('business_ideas').insert({
                'user_id': user_id,
                'niche': niche,
                'ideas': json.dumps(ideas),
                'web_search_used': web_search_used,
                'created_at': datetime.now().isoformat()
            }).execute()
            
            if result.data:
                idea_data = result.data[0]
                return BusinessIdea(
                    id=idea_data['id'],
                    user_id=idea_data['user_id'],
                    niche=idea_data['niche'],
                    ideas=json.loads(idea_data['ideas']) if isinstance(idea_data['ideas'], str) else idea_data['ideas'],
                    web_search_used=idea_data['web_search_used'],
                    created_at=idea_data['created_at']
                )
            return None
        except Exception as e:
            print(f"Error creating business idea: {e}")
            return None
    
    @staticmethod
    def get_by_user_id(user_id: int, limit: int = 10) -> List['BusinessIdea']:
        """Get business ideas by user ID"""
        try:
            result = db.get_service_role_client().table('business_ideas').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            
            ideas = []
            if result.data:
                for idea_data in result.data:
                    ideas.append(BusinessIdea(
                        id=idea_data['id'],
                        user_id=idea_data['user_id'],
                        niche=idea_data['niche'],
                        ideas=json.loads(idea_data['ideas']) if isinstance(idea_data['ideas'], str) else idea_data['ideas'],
                        web_search_used=idea_data['web_search_used'],
                        created_at=idea_data['created_at']
                    ))
            return ideas
        except Exception as e:
            print(f"Error getting business ideas by user ID: {e}")
            return []
    
    @staticmethod
    def get_by_id(idea_id: int) -> Optional['BusinessIdea']:
        """Get business idea by ID"""
        try:
            result = db.get_service_role_client().table('business_ideas').select('*').eq('id', idea_id).execute()
            
            if result.data:
                idea_data = result.data[0]
                return BusinessIdea(
                    id=idea_data['id'],
                    user_id=idea_data['user_id'],
                    niche=idea_data['niche'],
                    ideas=json.loads(idea_data['ideas']) if isinstance(idea_data['ideas'], str) else idea_data['ideas'],
                    web_search_used=idea_data['web_search_used'],
                    created_at=idea_data['created_at']
                )
            return None
        except Exception as e:
            print(f"Error getting business idea by ID: {e}")
            return None
