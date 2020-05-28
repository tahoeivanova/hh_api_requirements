from flask import Flask, render_template, request
from hh_api_pro import avarage_salary, hh_requirements

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def about_hh_parsing():
    return render_template('index.html')

@app.route('/hh_api', methods=['GET', 'POST'])
def hh_api_salary():
    if request.method == 'POST':
        vacancy = request.form['vacancy']
        city = request.form['city']
        data = avarage_salary(vacancy, city)
        return render_template('average_salary_results.html', **data)
    else:
        return render_template('hh_api_parser.html')


@app.route('/hh_api_pro')
def hh_api_requirements():
    return render_template('hh_api_parser_pro.html')

@app.route('/requirements_results')
def hh_api_requirements_results():
    results_all, results_list = hh_requirements()
    results_dict = {str(a): results_list[a] for a in range(10)}

    return render_template('requirements_results.html', results_all=results_all,results_dict=results_dict)

@app.route('/average_salary')
def salary_results():
    data = avarage_salary()
    return render_template('average_salary_results.html', **data)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
