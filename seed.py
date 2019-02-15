"""utility file to seed database from gathered data from CRP API"""

# import datetime
# from sqlalchemy import func

# from model import User, Rating, Movie, connect_to_db, db
# from server import app







































if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    user_filename = ""
    movie_filename = ""
    rating_filename = ""
    # load_users(user_filename)
    # load_movies(movie_filename)
    # load_ratings(rating_filename)
    # set_val_user_id()
