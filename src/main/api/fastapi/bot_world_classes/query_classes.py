from pydantic import BaseModel, validator
from typing import Optional


"""
Request format for recommend endpoint
"""
class RecommendRequest(BaseModel):
    
    user_id: Optional[str] = None
    item_id: Optional[str] = None
    by: Optional[str] = "popularity"
                                
    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        arbitrary_types_allowed = True

    """
    Valids the inputs
    notes:
        1. user_id and item_id are first assigned without checking.
        2. during validation of "by", perform check using check_request_validity

    """
    @validator('by')
    def check_request_validity(cls, value, values):
        # only these recommendation types allowed
        allowed_values = ["user", "item", "popularity", "hybrid"]
        if value not in allowed_values:
            raise ValueError(f"Invalid value for 'by': {value}. Allowed values are {allowed_values}.")
        # when recommending by item, item_id must be given
        if value == "item" and values.get("item_id") is None:
            raise ValueError(f"Item ID is required for 'by':'item'")
        # when recommending by user, user_id is required
        if value == "user" and values.get("user_id") is None:
            raise ValueError(f"User ID is required for 'by':'user'")
        # when recommending by hybrid, user_id is required
        if value == "hybrid" and values.get("user_id") is None:
            raise ValueError(f"User ID is required for 'by':'hybrid'")
        return value

if __name__ == "__main__":
    # Catch invalid cases
    try:
        recommend_request = RecommendRequest(
            by="hybrid"
        )
    except ValueError as e:
        print(e)
        pass
    try:
        recommend_request = RecommendRequest(
            by="item"
        )
    except ValueError as e:
        print(e)
        pass
    try:
        recommend_request = RecommendRequest(
            by="user"
        )
    except ValueError as e:
        print(e)
        pass
        