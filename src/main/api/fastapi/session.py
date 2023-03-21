from bot_world_classes import SessionRecommendations


def load_session():
    session = SessionRecommendations()
    return session


if __name__ == "__main__":
    session = load_session()
    print("Load Session Success!")