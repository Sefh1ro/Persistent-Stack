from flask import Flask, render_template, request
from stack import load_stacks, process_request, merge_stacks # Добавьте функцию merge_stacks

app = Flask(__name__)

@app.route('/presentation')
def presentation():
    return render_template('presentation.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    stacks = load_stacks()
    current_stack = request.form.get('current_stack')
    if current_stack not in stacks:
        current_stack = None
    if request.method == 'POST':
        stacks, current_stack = process_request(request.form, stacks, current_stack)
    
    return render_template('index.html', stacks=stacks, current_stack=current_stack)

@app.route('/merger', methods=['GET', 'POST'])
def merger():
    stacks = load_stacks()
    steps = []  # Инициализация steps
    if request.method == 'POST':
        stack1 = request.form.get('stack1')
        stack2 = request.form.get('stack2')
        merged_name = request.form.get('merged_name')
        if stack1 in stacks and stack2 in stacks and merged_name:
            # Заполнение steps данными о процессе слияния
            steps = merge_stacks(stacks[stack1], stacks[stack2])
            stacks[merged_name] = steps[-1]['stack']  # Сохранение результата слияния
    return render_template('merger.html', stacks=stacks, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)