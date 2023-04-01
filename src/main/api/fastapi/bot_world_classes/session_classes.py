from typing import List, Optional
from itertools import cycle


"""
Stores a set of recommendations for each unique ID
notes:
Cycles through the set of recommendations with itertools.cycle
"""
class SessionRecommendations(object):
    def __init__(self):
        self.session = dict()
    """
    Checks that Session recommendations for ID exists 
    """
    def exists(self, ID: str):
        return self.session.get(str(ID)) is not None
    """
    Add new session - add new set of recommendations
    """
    def add(self, ID: str, recommendations: List):
        self.session[str(ID)] = cycle(recommendations)
        return
    """
    Make 1 recommendation for unique ID
    """
    def recommend(self, ID: str):  
        assert self.exists(str(ID))
        return next(self.session[str(ID)])


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