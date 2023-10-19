from flask import render_template, request
from src import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:word>')
def word(word):
    return f'{word} ' * 5

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




if __name__ == '__main__':
    app.run(debug=True)