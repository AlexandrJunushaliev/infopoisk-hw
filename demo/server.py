from flask import Flask, request, render_template, jsonify
from hw5 import getSearch


app = Flask(__name__)

# Обработчик запроса на поиск
@app.route('/', methods=['GET', 'POST'])
def search_handler():
    if request.method == 'POST':
        query = request.args.get('query')
        result = getSearch(query)
        print(result)
        return jsonify(result)
    
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)