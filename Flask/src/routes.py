import sqlite3

from flask import Flask, render_template, request, redirect, url_for

from Flask.src.database import Duomenubazes
from Flask.src.models import User, Match, Bet

app = Flask(__name__)
db = Duomenubazes('sqlite:///data.sqlite')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/keliamieji')
def keliamieji():
    years = []
    for year in range(1900, 2101):
        if year % 4 == 0 and year % 100 != 0 or year % 300 == 0:
            years.append(year)
    return render_template('keliamieji.html', years=years)


def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False


@app.route("/keliamieji_year", methods=["GET", "POST"])
def check_leap_year():
    if request.method == "POST":
        input_year = int(request.form["year"])
        is_leap = is_leap_year(input_year)
        result = f"{input_year} yra {'keliamieji' if is_leap else 'nekeliamieji'} metai."
        return render_template("keliamieji_year.html", result=result)
    return render_template("keliamieji_year.html")


@app.route("/metu_info/<int:year>")
def metu_info(year):
    is_year_leap = get_leap_year_info(year)
    years = range(1900, 2101)
    return render_template("metu_info.html", year=year, is_year_leap=is_year_leap, years=years)


def get_leap_year_info(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return f"{year} - Keliamieji metai"
    return f"{year} - Ne keliamieji metai"


@app.route('/submit_prediction', methods=['GET', 'POST'])
def submit_prediction():
    if request.method == 'POST':
        username = request.form.get('username')
        surname = request.form.get('surname')
        guessed_score = request.form.get('guessed_score')
        selected_game_id = request.form.get('game_id')

        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username=username, surname=surname, guessed_score=guessed_score)
            db.session.add(user)
            db.session.commit()

        user_id = user.id
        print(user_id)

        match = db.session.query(Match).filter_by(id=selected_game_id).first()

        if match:
            match_id = selected_game_id
            db.store_prediction(match_id, user_id)
        else:
            return "Invalid match selected"

        user = db.session.query(User).filter_by(id=user_id).first()

        return redirect(url_for('thank_you'))

    team_names = db.get_all_matches()
    return render_template('results.html', team_names=team_names)




@app.route('/team_bets/<int:idas>', methods=['GET'])
def get_by_id(idas):
    rungtynes_info = db.get_match_by_id(match_id=idas)
    guessed_people = db.get_bet_by_match_id(match_id=idas)
    return render_template('team_bets.html', rungtynes=rungtynes_info, guessed_people=guessed_people, match_id=idas)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/results')
def results():
    all_matches = db.get_all_matches()
    return render_template('results.html', all_matches=all_matches)


@app.route('/team_bets/<int:team_id>')
def team_bets(team_id):
    players_bets = db.get_players_by_team_id(team_id)
    return render_template('team_bets.html', players_bets=players_bets)

@app.route('/calculate_points/<int:match_id>', methods=['GET'])
def calculate_points(match_id):
    match = db.session.query(Match).filter_by(id=match_id).first()
    if match and match.result is not None:
        winner, closest = db.calculate_points(match_id)
        return render_template('calculation_results.html', winner=winner, closest=closest)
    else:
        return "No result for this match or match not found."


@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'POST':
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')
        match_date = request.form.get('match_date')
        result = request.form.get('result')

        db.add_record(Match, team1=team1, team2=team2, match_date=match_date, result=result)

        return redirect(url_for('game_created'))

    return render_template('create_game.html')

@app.route('/game_created')
def game_created():
    return render_template('game_created.html')

@app.route('/score_changed')
def score_changed():
    return render_template('score_changed.html')

@app.route('/view_matches')
def view_matches():
    match_ids = db.get_all_matches()
    return render_template('view_matches.html', match_ids=match_ids)

@app.route('/change_score/<int:match_id>', methods=['GET', 'POST'])
def change_score(match_id):
    if request.method == 'POST':
        new_score = request.form.get('new_score')
        if db.update_match_score(match_id, new_score):
            return redirect(url_for('score_changed'))
    return render_template('change_score.html', match_id=match_id)




@app.route('/delete_match/<int:match_id>', methods=['GET', 'POST'])
def delete_match(match_id):
    if request.method == 'POST':
        match = db.session.query(Match).filter_by(id=match_id).first()
        if match:
            # Get all the bets related to this match
            bets = db.session.query(Bet).filter_by(match_id=match_id).all()

            # Loop through each bet and delete the associated user
            for bet in bets:
                user_id = bet.user_id
                db.delete_value(User, id=user_id)

            db.delete_value(Match, id=match_id)

            return render_template('match_deleted.html')
    return render_template('delete_match.html', match_id=match_id)


