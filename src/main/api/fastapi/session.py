from bot_world_classes import SessionRecommendations

"""
Creates and returns a SessionRecommendations instance
"""
def load_session():
    session = SessionRecommendations()
    return session

"""
Generates unique identifier for session recommendations
notes:
given chat_id = 123, user_id = 312
id is 123_312
"""
def get_session_id(**id_parts):
    return "_".join(map(str,id_parts.values()))



if __name__ == "__main__":
    session = load_session()
    print("Load Session Success!")