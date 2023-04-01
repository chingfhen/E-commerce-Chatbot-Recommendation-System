from typing import List, Optional
from collections import deque



"""
Stores a set of recommendations for each unique ID
notes:
this optimizes system i.e. reduces model and database calls 
Uses FIFO Data structure for further optimization
"""
class SessionRecommendations(object):
    def __init__(self):
        self.session = dict()
    """
    Checks that 1. Session recommendations for ID exists 2. and is not empty
    """
    def exists(self, ID: str):
        return (self.session.get(str(ID)) is not None) and (len(self.session[str(ID)])>0)
    """
    Add new session - add new set of recommendations
    """
    def add(self, ID: str, recommendations: List):
        self.session[str(ID)] = deque(recommendations)
        return
    """
    Make 1 recommendation for unique ID
    """
    def recommend(self, ID: str):  
        try:
            item = self.session[str(ID)].popleft()
        except IndexError:
            raise Exception("Session does not exist. Please add a new session with add()")
        return item

if __name__=="__main__":
    session = SessionRecommendations()
    print("Created Session!")
    ID = "0"
    session.add(ID, [1,2,3])
    print(f"Added ID {ID} session!")
    assert session.exists(ID)
    print(f"Checked ID {ID} session!")
    session.recommend(ID)
    print(f"Recommended ID {ID}!")