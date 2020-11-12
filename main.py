from flask import Flask, render_template, request, session, redirect, flash
import os
import chatbot

test_list = ["1. When did Steve Jobs announce the iPhone?;At the keynote speech for Macworld 2007;"
             "At the opening event for the 2007 Worldwide Developers Conference (WWDC);At the 2008 'It's Only Rock 'n' Roll' event.;"
             "At the 2008 Live event.",
             "2. Great things must be kept secret! What codename did Apple employees use to the iPhone before it was announced?;"
             "Project Purple;Death Start;Alan Parsons Project;Operation Wang Chung",
             "3. Which model of the iPhone was released in 2013?;iPhone 3s;iPhone 4s;iPhone 5s;iPhone 6s",
             "4. When were iPhone 7 and 7 plus unveiled?;2013;2015;2016;2017",
             "5. What 'i' in the iPhone stands for, according to Steve Jobs?;Ideal;Imagine;Internet;Intelligent",
             "6. What was the first iPhone model with the OLED display?;iPhone 7;iPhone 8;iPhone X;iPhone 11",
             "7. In August 2007, this New Jersey 17-year-old hacker became the first person to carrier-unlock an iPhone. "
             "Today he works for AI startup comma.ai.;Greg Harris;George Hotz;Gus Hillier;James Hotter",
             "8. What is the first iPhone model to use Lightning cables?;iPhone 4;iPhone 5;iPhone 6;iPhone 7",
             "9. What was the first iPhone model released in gold?;iPhone 4;iPhone 4s;iPhone 5;iPhone 5s",
             "10. What compilers apple using?;GCC - GNU Compiler Collations;Dalvik;Clang;Bartok"
             ]
ans_result = [["At the keynote speech for Macworld 2007"],["Project Purple"],["iPhone 5s"],["2016"],["Ideal"],["iPhone X"],
              ["George Hotz"],["iPhone 5"],["iPhone 5s"],["GCC - GNU Compiler Collations"]]

app = Flask(__name__)

app.secret_key = os.urandom(24)


def result_check(user_result):
    res = 0
    crt = 0
    wrg = 0
    for ur in user_result:
        if ur == ans_result[res]:
            crt += 1
        else:
            wrg += 1
        res += 1
    acc = round((crt/10)*100)
    crt_cnt = crt
    return crt_cnt, acc


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_answer = []
        session.pop('user', None) #drop the session
        user_answer.append(request.form.getlist('q1options'))
        user_answer.append(request.form.getlist('q2options'))
        user_answer.append(request.form.getlist('q3options'))
        user_answer.append(request.form.getlist('q4options'))
        user_answer.append(request.form.getlist('q5options'))
        user_answer.append(request.form.getlist('q6options'))
        user_answer.append(request.form.getlist('q7options'))
        user_answer.append(request.form.getlist('q8options'))
        user_answer.append(request.form.getlist('q9options'))
        user_answer.append(request.form.getlist('q10options'))

        c_count, accu = result_check(user_answer)

        if request.form['email']:
            session['user'] = request.form['email']
            print(session['user'])
            name = session['user'].split('.')[0]
            answer_result = 'Thank you '+ str(name.capitalize()) +' for taking our quiz!;' \
                            'You got ' + str(accu) + '% of the answers correct.;Congratulations!;'+ str(accu)
            flash(answer_result)
            print(name.capitalize())
            print(answer_result)
            #return redirect(url_for('protected'))

    return render_template('index.html', ques=test_list)
    #return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    bot_response = chatbot.chat(user_input)
    #bot_response = "hello"

    print(user_input)
    print(bot_response)
    return str(bot_response)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
