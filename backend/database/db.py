import motor.motor_asyncio
from beanie import init_beanie
import logging
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from passlib.context import CryptContext

# Import User from models.user
from models.user import User
# TODO: Create and import these models
# from models import Lecture, Concept, FlaggedConcept

# Set up logging
logger = logging.getLogger(__name__)

# Set up password hashing context

async def init_db():
    """Initialize database connection and register models with Beanie"""
    try:
        # Get connection details from environment
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        db_name = os.getenv("DATABASE_NAME", "clarifai")
        
        # Create Motor client
        client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
        
        # Initialize Beanie with our document models
        await init_beanie(
            database=client[db_name],
            document_models=[
                User,
                # TODO: Add these models when they're defined
                # Lecture,
                # Concept,
                # FlaggedConcept
            ]
        )
        
        logger.info(f"Connected to MongoDB: {mongodb_url}, Database: {db_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return False

# Authentication helpers




# User operations
async def create_user(email: str, password: str, full_name: Optional[str] = None) -> Optional[User]:
    """
    Create a new user with hashed password
    """
    try:
        # Check if user already exists
        existing_user = await User.find_one({"email": email})
        if existing_user:
            logger.warning(f"User with email {email} already exists")
            return None
            
        # Create new user with hashed password
        user = User(
            email=email,
            full_name=full_name
        )
        await user.insert()
        return user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return None

async def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password
    """
    try:
        user = await User.find_one({"email": email})
        if not user:
            return None
       
            
        # Update last login time
        user.last_login = datetime.utcnow()
        await user.save()
        
        return user
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None

async def get_user(user_id: str) -> Optional[User]:
    """Get user by ID"""
    return await User.get(user_id)

async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email"""
    return await User.find_one({"email": email})

# Temporary implementation of functions needed by websockets.py
async def save_lecture(user_id: str, title: str, organized_notes: str) -> str:
    """Temporary implementation to save a lecture and return its ID"""
    logger.warning("Using temporary implementation of save_lecture. Database save not implemented.")
    return "temp_lecture_id"

async def get_user_lectures(user_id: str) -> List[Dict[str, Any]]:
    """Temporary implementation to get lectures for a user"""
    logger.warning("Using temporary implementation of get_user_lectures. Database query not implemented.")
    # Return a list with dummy lecture data
    return [
        {
            "id": "lecture1",
            "title": "Introduction to AI",
            "created_at": datetime.utcnow(),
            "dict": lambda: {
                "id": "lecture1",
                "title": "Introduction to AI",
                "created_at": datetime.utcnow().isoformat()
            }
        },
        {
            "id": "lecture2",
            "title": "Machine Learning Basics",
            "created_at": datetime.utcnow(),
            "dict": lambda: {
                "id": "lecture2",
                "title": "Machine Learning Basics",
                "created_at": datetime.utcnow().isoformat()
            }
        }
    ]

async def save_concept(user_id: str, lecture_id: str, concept_name: str, 
                      text_snippet: str, difficulty_level: int, 
                      start_position: int, end_position: int) -> str:
    """Temporary implementation to save a concept"""
    logger.warning("Using temporary implementation of save_concept. Database save not implemented.")
    return "temp_concept_id"

async def save_flagged_concept(user_id: str, lecture_id: str, concept_name: str,
                              explanation: str, text_snippet: str, 
                              difficulty_level: int, start_position: int = 0, 
                              end_position: int = 0) -> str:
    """Temporary implementation to save a flagged concept"""
    logger.warning("Using temporary implementation of save_flagged_concept. Database save not implemented.")
    return "temp_flagged_concept_id"

async def get_flagged_concepts(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Temporary implementation to get flagged concepts"""
    logger.warning("Using temporary implementation of get_flagged_concepts. Database query not implemented.")
    return []

# Transcript operations
# TODO: Uncomment when Transcript model is defined
# async def save_transcript(user_id: Optional[str], lecture_id: Optional[str], text: str) -> str:
#     """Save a transcript and return its ID"""
#     transcript = Transcript(
#         user_id=user_id,
#         lecture_id=lecture_id,
#         text=text
#     )
#     await transcript.insert()
#     return str(transcript.id)
# 
# async def get_transcript(transcript_id: str) -> Optional[Transcript]:
#     """Retrieve a transcript by ID"""
#     return await Transcript.get(transcript_id)
# 
# async def get_user_transcripts(user_id: str) -> List[Transcript]:
#     """Get all transcripts for a specific user"""
#     return await Transcript.find({"user_id": user_id}).to_list()

# Temporary implementations for transcript functions
async def get_transcript(transcript_id: str) -> Optional[Dict[str, Any]]:
    """Temporary implementation to retrieve a transcript by ID"""
    logger.warning("Using temporary implementation of get_transcript. Database query not implemented.")
    # Return a dummy transcript object
    return {
        "id": transcript_id,
        "user_id": None,
        "lecture_id": None,
        "text": "This is a placeholder transcript text.",
        "created_at": datetime.utcnow(),
        "dict": lambda: {
            "id": transcript_id,
            "user_id": None,
            "text": "This is a placeholder transcript text.",
            "created_at": datetime.utcnow().isoformat()
        }
    }

async def get_user_transcripts(user_id: str) -> List[Dict[str, Any]]:
    """Temporary implementation to get all transcripts for a specific user"""
    logger.warning("Using temporary implementation of get_user_transcripts. Database query not implemented.")
    # Return a list with a single dummy transcript
    return [{
        "id": "temp_transcript_id",
        "user_id": user_id,
        "text": "This is a placeholder transcript text.",
        "created_at": datetime.utcnow(),
        "_id": "temp_transcript_id",
        "title": "Sample Transcript",
        "dict": lambda: {
            "id": "temp_transcript_id",
            "user_id": user_id,
            "text": "This is a placeholder transcript text.",
            "created_at": datetime.utcnow().isoformat(),
            "title": "Sample Transcript"
        }
    }]

# OrganizedNotes operations
# TODO: Uncomment when OrganizedNotes model is defined
# async def save_organized_notes(
#     user_id: Optional[str], 
#     lecture_id: Optional[str], 
#     title: str,
#     content: str,
#     raw_transcript: str
# ) -> str:
#     """Save organized notes and return its ID"""
#     notes = OrganizedNotes(
#         user_id=user_id,
#         lecture_id=lecture_id,
#         title=title,
#         content=content,
#         raw_transcript=raw_transcript
#     )
#     await notes.insert()
#     return str(notes.id)
# 
# async def get_organized_notes(notes_id: str) -> Optional[OrganizedNotes]:
#     """Retrieve organized notes by ID"""
#     return await OrganizedNotes.get(notes_id)
# 
# async def get_user_notes(user_id: str) -> List[OrganizedNotes]:
#     """Get all organized notes for a specific user"""
#     return await OrganizedNotes.find({"user_id": user_id}).to_list()

# Temporary implementations for notes functions
async def get_organized_notes(notes_id: str) -> Optional[Dict[str, Any]]:
    """Temporary implementation to retrieve organized notes by ID"""
    logger.warning("Using temporary implementation of get_organized_notes. Database query not implemented.")
    # Return a dummy notes object
    return {
        "id": notes_id,
        "user_id": None,
        "lecture_id": None,
        "title": "Sample Notes",
        "content": "This is a placeholder for organized notes content.",
        "raw_transcript": "This is the raw transcript text.",
        "created_at": datetime.utcnow(),
        "dict": lambda: {
            "id": notes_id,
            "user_id": None,
            "title": "Sample Notes",
            "content": "This is a placeholder for organized notes content.",
            "raw_transcript": "This is the raw transcript text.",
            "created_at": datetime.utcnow().isoformat()
        }
    }

async def get_user_notes(user_id: str) -> List[Dict[str, Any]]:
    """Temporary implementation to get all organized notes for a specific user"""
    logger.warning("Using temporary implementation of get_user_notes. Database query not implemented.")
    # Return a list with a single dummy notes
    return [{
        "id": "temp_notes_id",
        "user_id": user_id,
        "title": "Sample Notes",
        "content": "This is a placeholder for organized notes content.",
        "raw_transcript": "This is the raw transcript text.",
        "created_at": datetime.utcnow(),
        "dict": lambda: {
            "id": "temp_notes_id",
            "user_id": user_id,
            "title": "Sample Notes",
            "content": "This is a placeholder for organized notes content.",
            "raw_transcript": "This is the raw transcript text.",
            "created_at": datetime.utcnow().isoformat()
        }
    }]

# OtherConcept operations
# TODO: Uncomment when OtherConcept model is defined
# async def save_other_concept(
#     concept_name: str,
#     text_snippet: str,
#     difficulty_level: int,
#     start_position: int,
#     end_position: int,
#     transcript_id: Optional[str] = None,
#     lecture_id: Optional[str] = None
# ) -> str:
#     """Save a detected but unflagged concept and return its ID"""
#     concept = OtherConcept(
#         concept_name=concept_name,
#         text_snippet=text_snippet,
#         difficulty_level=difficulty_level,
#         start_position=start_position,
#         end_position=end_position,
#         transcript_id=transcript_id,
#         lecture_id=lecture_id
#     )
#     await concept.insert()
#     return str(concept.id)
# 
# async def get_other_concepts(transcript_id: Optional[str] = None) -> List[OtherConcept]:
#     """Get unflagged concepts, optionally filtered by transcript"""
#     query = {"transcript_id": transcript_id} if transcript_id else {}
#     return await OtherConcept.find(query).to_list()

# Temporary implementation for other concepts
async def get_other_concepts(transcript_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Temporary implementation to get unflagged concepts"""
    logger.warning("Using temporary implementation of get_other_concepts. Database query not implemented.")
    # Return an empty list for now
    return [{
        "id": "temp_concept_id",
        "concept_name": "Sample Concept",
        "text_snippet": "This is where the concept appears in text.",
        "difficulty_level": 2,
        "transcript_id": transcript_id if transcript_id else "default_transcript_id",
        "dict": lambda: {
            "id": "temp_concept_id",
            "concept_name": "Sample Concept",
            "text_snippet": "This is where the concept appears in text.",
            "difficulty_level": 2,
            "transcript_id": transcript_id if transcript_id else "default_transcript_id"
        }
    }]

# Lecture operations
# TODO: Uncomment when Lecture model is defined
# async def save_lecture(user_id: str, title: str, organized_notes: str) -> str:
#     """Save a lecture and return its ID"""
#     lecture = Lecture(
#         user_id=user_id,
#         title=title,
#         organized_notes=organized_notes
#     )
#     await lecture.insert()
#     return str(lecture.id)
# 
# async def get_user_lectures(user_id: str) -> List[Lecture]:
#     """Get all lectures for a specific user"""
#     return await Lecture.find({"user_id": user_id}).to_list()

# Concept operations
# TODO: Uncomment when Concept model is defined
# async def save_concept(user_id: str, lecture_id: str, concept_name: str, text_snippet: str, difficulty_level: int, start_position: int, end_position: int) -> str:
#     """Save a concept and return its ID"""
#     concept = Concept(
#         user_id=user_id,
#         lecture_id=lecture_id,
#         concept_name=concept_name,
#         text_snippet=text_snippet,
#         difficulty_level=difficulty_level,
#         start_position=start_position,
#         end_position=end_position
#     )
#     await concept.insert()
#     return str(concept.id)
# 
# async def get_concepts_by_lecture(lecture_id: str) -> List[Concept]:
#     """Get all concepts for a specific lecture"""
#     return await Concept.find({"lecture_id": lecture_id}).to_list() 