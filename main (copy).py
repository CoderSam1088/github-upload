from flask import Flask, request, redirect, render_template, session
import random
import inventory

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'SIH*v-6u)c>q<;;h&);cRw,1E_CO8>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      if session['currentchoice']!= None:
        if session['currentchoice']==1 or session['currentchoice']==2 or session['currentchoice']==3 or session['currentchoice']==5:
          if session['indchar']!= None:
            if session['currentchoice']==2:
              if session['round']!= None:
                  choice1a = "What is the first item you want to hold from the inventory?"
                  choice2a = "What is the second item you want to hold from the inventory?"
                  if request.form['choice2'].lower() not in session['fullinv'][session['indchar']]:
                    session['options'] = [request.form['choice2'] + " is not in " + session['currentchar'] + "'s inventory"] + session['options']
                  if request.form['choice1'].lower() not in session['fullinv'][session['indchar']]:
                    session['options'] = [request.form['choice1'] + " is not in " + session['currentchar'] + "'s inventory"] + session['options']
                    render_template('next.html', options=session['options'], choice1a=choice1a, choice2a=choice2a)
                  elif request.form['choice1'].lower() == request.form['choice2'].lower():
                    session['options'] = ["You can't pick the same item twice. Pick two different items."] + session['options']
                    render_template('next.html', options=session['options'], choice1a=choice1a, choice2a=choice2a)
                  elif request.form['choice1'].lower() in session['fullinv'][session['indchar']] and request.form['choice2'].lower() in session['fullinv'][session['indchar']]:
                    ind1 = session['fullinv'][session['indchar']].index(request.form['choice1'].lower())
                    ind2 = session['fullinv'][session['indchar']].index(request.form['choice2'].lower())
                    session['options'] = [inventory.modify_holding(session['holding'],session['fullinv'],session['indchar'], ind1,ind2)]
                    session['options'].append("")
                    session['options'] += inventory.firstquestion()
                    session['round'] = None
                    session['currentchoice'] = None
                    session['indchar']=None
                    return render_template('index.html', options=session['options'])
                  else:
                    render_template('next.html', options=session['options'], choice1a=choice1a, choice2a=choice2a)
              return render_template('next.html', options=session['options'], choice1a=choice1a, choice2a=choice2a)

          
          try:
            #see if a valid value is entered as an option
            session['currentchar']=request.form['choice'].capitalize() 
            session['indchar'] = session['chars'].index(session['currentchar'])
          except:
            #throw an error if value is invalid
            session['options'] = ["That is not a character.", "These are the characters in the game: ","", session['chars'],"", "Which character do you want?: "]
          
          if session['indchar']!= None:
            
            #check that value was valid
            if session['currentchoice']==1:
              #if choice is 1, print the inventory
              session['options']=inventory.print_inv(session['fullinv'], session['holding'], session['indchar']) + ["",] + inventory.firstquestion()
              #reset session values
              session['currentchoice']=None
              session['indchar']=None
            if session['currentchoice']==2:
              choice1a = "What is the first item you want to hold from the inventory?"
              choice2a = "What is the second item you want to hold from the inventory?"
              session['currentchar'] = request.form['choice']
              session['options'] = ["This is " + session['currentchar']+ "'s' inventory: ", ""]
              session['options']+= inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
              session['round']=1
              return render_template('next.html', options=session['options'], choice1a=choice1a, choice2a=choice2a)
          
          return render_template('index.html', options=session['options'])
      try:
        choice = int(request.form['choice'])
      except:
        errors = "{!r} is not a number. Enter a whole number 1-6.\n".format(request.form['choice'])
      if choice != None:
        session['currentchoice'] = choice
        if (choice == 1 or choice == 2 or choice == 3 or choice == 5):
          session['options'] = inventory.pickChars(session['chars'])
          return render_template('index.html', options=session['options'])
        return render_template('index.html', options=session['options'])
        


        

    else:
        session['options'] = inventory.firstquestion()
        session['chars'] = inventory.characters
        session['fullinv'] = inventory.finaltup
        session['holding'] = inventory.charsholding
        errors = ''
        session['currentchoice'] = None
        session['currentchar'] = ''
        session['indchar'] = None
        session['currentchar'] = None
        session['item1'] = None
        session['item2'] = None
        session['round'] = None
        session['error'] = False


    return render_template('index.html', options=session['options'], errors=errors)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
