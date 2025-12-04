from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

def init_guess_game():
    session['secret_number'] = random.randint(1, 100)
    session['guess_tries'] = 0

PICTURE_QUESTIONS = [
    {
        "id": 1,
        "question": "Энэ зурагт ямар жимс байна?",
        "image": "https://images.pexels.com/photos/102104/pexels-photo-102104.jpeg",
        "answer": "гүзээлзгэнэ"
    },
    {
        "id": 2,
        "question": "Энэ зурагт ямар амьтан байна?",
        "image": "https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg",
        "answer": "муур"
    },
    {
        "id": 3,
        "question": "Энэ зурагт ямар унаа байна?",
        "image": "https://images.pexels.com/photos/210019/pexels-photo-210019.jpeg",
        "answer": "машин"
    }
]

MAZE_SIZE = 5
EXIT_POS = (4, 4)

def init_maze():
    session['maze_pos'] = [0, 0]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess_number():
    if 'secret_number' not in session:
        init_guess_game()

    message = None
    last_guess = None
    tries = session.get('guess_tries', 0)

    if request.method == 'POST':
        guess_str = request.form.get('guess')
        if guess_str:
            try:
                g = int(guess_str)
                last_guess = g
                tries += 1
                session['guess_tries'] = tries
                secret = session['secret_number']

                if g < secret:
                    message = "Бага байна!"
                elif g > secret:
                    message = "Их байна!"
                else:
                    message = f"🎉 Зөв таалаа! Тоо: {secret}. Оролдлого: {tries}."
                    init_guess_game()
                    tries = 0
            except:
                message = "Зөв бүхэл тоо оруул."

    return render_template('guess.html',
                           message=message,
                           last_guess=last_guess,
                           tries=tries)


@app.route('/rps', methods=['GET', 'POST'])
def rps():
    choices = ["чулуу", "даавуу", "хайч"]
    player_choice = None
    computer_choice = None
    result = None

    if request.method == 'POST':
        player_choice = request.form.get('choice')
        computer_choice = random.choice(choices)

        if player_choice == computer_choice:
            result = "Тэнцлээ 😐"
        elif (
            (player_choice == "чулуу" and computer_choice == "хайч") or
            (player_choice == "хайч" and computer_choice == "даавуу") or
            (player_choice == "даавуу" and computer_choice == "чулуу")
        ):
            result = "Чи яллаа! 🎉"
        else:
            result = "Компьютер яллаа 😢"

    return render_template('rps.html',
                           choices=choices,
                           player_choice=player_choice,
                           computer_choice=computer_choice,
                           result=result)


@app.route('/picture', methods=['GET', 'POST'])
def picture_quiz():
    message = None

    if request.method == 'GET':
        question = random.choice(PICTURE_QUESTIONS)
        session['picture_answer'] = question['answer']
        return render_template('picture.html', question=question, message=None)

    if request.method == 'POST':
        user_answer = request.form.get('answer', '').lower().strip()
        correct = session.get('picture_answer', '').lower()

        if user_answer == correct:
            message = "🎉 Зөв хариуллаа!"
        else:
            message = f"Буруу. Зөв нь: {correct}"

        question = random.choice(PICTURE_QUESTIONS)
        session['picture_answer'] = question['answer']
        return render_template('picture.html', question=question, message=message)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci_game():
    message = None

    if request.method == 'POST':
        try:
            n = int(request.form.get('n'))
            ans = int(request.form.get('answer'))
            correct = fib(n)

            if ans == correct:
                message = f"🎉 Зөв! F({n}) = {correct}"
            else:
                message = f"❌ Буруу. Зөв нь: {correct}"
        except:
            message = "Бүхэл тоогоор оруулна уу."

    return render_template('fibonacci.html', message=message)


@app.route('/maze', methods=['GET', 'POST'])
def maze():
    if 'maze_pos' not in session:
        init_maze()

    r, c = session['maze_pos']
    message = None
    finished = False

    if request.method == 'POST':
        mv = request.form.get('move')

        if mv == 'up' and r > 0:
            r -= 1
        if mv == 'down' and r < MAZE_SIZE - 1:
            r += 1
        if mv == 'left' and c > 0:
            c -= 1
        if mv == 'right' and c < MAZE_SIZE - 1:
            c += 1

        if 'reset' in request.form:
            init_maze()
            r, c = session['maze_pos']
            message = "Дахин эхэллээ."
        else:
            session['maze_pos'] = [r, c]

        if (r, c) == EXIT_POS:
            message = "🎉 Гарцад хүрлээ!"
            finished = True

    grid = []
    for i in range(5):
        row = []
        for j in range(5):
            if (i, j) == (0, 0):
                t = "start"
            elif (i, j) == EXIT_POS:
                t = "exit"
            elif (i, j) == (r, c):
                t = "current"
            else:
                t = "normal"
            row.append(t)
        grid.append(row)

    return render_template('maze.html',
                           grid=grid,
                           message=message,
                           finished=finished)


if __name__ == '__main__':
    app.run(debug=True)
