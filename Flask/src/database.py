from typing import Type

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker, declarative_base

from Flask.src.models import User, Match, Bet

Base = declarative_base()



class Duomenubazes:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    def create_tables(self):
        User.metadata.create_all(self.engine)

    def drop_tables(self):
        User.metadata.drop_all(self.engine)

    def commit(self):
        self.session.commit()

    def add_record(self, table: Type[User], **kwargs):
        record = table(**kwargs)
        self.session.add(record)
        self.commit()
        self.session.close()

    def get_bet_by_match_id(self, match_id):
        users = self.session.query(User).join(Bet).filter_by(match_id=match_id).all()
        return [(user.username, user.surname, user.guessed_score) for user in users]

    def get_match_by_id(self, match_id):
        match = self.session.query(Match).filter_by(id=match_id).first()
        return (match.team1, match.team2, match.result) if match else None

    def get_all_matches(self):
        matches = self.session.query(Match).all()
        match_data = [(match.id, match.team1, match.team2, match.result) for match in matches]
        self.session.close()
        return match_data

    def store_prediction(self, selected_game_id, user_id):
        bet = Bet(
            user_id=user_id,
            match_id=selected_game_id,
        )

        db.session.add(bet)
        db.session.commit()

    def delete_value(self, table, id, user_id=None, match_id=None):
        if table == Match:
            # Delete the match
            self.session.query(table).filter_by(id=id).delete()
            # Delete associated bets
            self.session.query(Bet).filter_by(match_id=id).delete()
        elif table == User:
            self.session.query(table).filter_by(id=id).delete()
            self.session.query(Bet).filter_by(user_id=id).delete()
        self.commit()




    def get_players_by_team_id(self, team_id):
        players = self.session.query(User).join(Bet).join(Match).filter(
            (Match.team1 == team_id) | (Match.team2 == team_id)
        ).all()

    def calculate_points(self, match_id):
        match_info = self.get_bet_by_match_id(match_id)
        the_score = self.get_match_by_id(match_id)[2]

        if the_score is None:
            return "No winner", None

        else:
            submissions = self.get_bet_by_match_id(match_id)
            closest = None
            closest_guesser = None

            for submission in submissions:
                guess_home, guess_away = map(int, submission[2].split(":"))
                true_home, true_away = map(int, the_score.split(":"))
                diff = abs(true_home - guess_home) + abs(true_away - guess_away)
                if closest is None or diff < closest:
                    closest = diff
                    closest_guesser = f"{submission[0]} {submission[1]}"
            if closest_guesser:
                winner = closest_guesser
                return winner, closest
            return "No Winner!", None


    def get_scores(self):
        users = self.session.query(Match).all()
        return [Match.result for matches in users]

    def delete_user_id(self, user_id):
        self.session.query(User).filter_by(id=user_id).delete()
        self.commit()
        
    def update_match_score(self, match_id, new_score):
        try:
            match = self.session.query(Match).filter_by(id=match_id).first()
            if match:
                match.result = new_score
                self.commit()
                return True  # Successful update
            else:
                return False  # Match not found
        except Exception as e:
            print(f"Error updating match score: {e}")
            return False  # Error occurred during the update

db = Duomenubazes('sqlite:///data.sqlite')
