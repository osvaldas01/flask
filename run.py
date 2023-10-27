from Flask.src.routes import app, db


#this is the main file to run the app
if __name__ == '__main__':
    with app.app_context():
        # db.delete_user_id(4)
        # db.add_record(Match, team1="Lithuania", team2="Latvia", match_date="2023-10-27", result=None)
        app.run(debug=True)