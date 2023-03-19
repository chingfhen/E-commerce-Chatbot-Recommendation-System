from typing import List, Optional


"""
Stores a set of recommendations for each user - optimizes system i.e. don't need further model or database calls after the first
"""
class SessionRecommendations(object):
    def __init__(self):
        self.session = dict()
    """
    Checks that 1. Session recommendations for a user was made before 2. Session recommendations is not empty
    """
    def session_exists(self, user_id: str):
        return (self.session.get(str(user_id)) is not None) and (len(self.session[str(user_id)])>0)
    """
    Add new session - add new set of recommendations
    """
    def add_session(self, user_id: str, recommendations: List):
        self.session[str(user_id)] = deque(recommendations)
    """
    Make 1 recommendation for user - if session exists
    """
    def recommend(self, user_id: str):
        assert self.session_exists(user_id)
        item = self.session[str(user_id)].popleft()
        return item 

