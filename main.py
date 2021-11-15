from flask import Flask, request, redirect, render_template, session
import random
import inventory

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'SIH*v-6u)c>q<;;h&);cRw,1E_CO8>'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      errors = []
      if session['round'] != None:
        char = session['currentchar']
        choice = session['currentchoice']
        if session['round'] == 1:
          if choice==1 or choice == 2 or choice == 3 or choice == 5:
            char = request.form['choice'].capitalize()
            try:
              session['indchar'] = session['chars'].index(char)
            except:
              errors = [char + " is not a character in the game. Pick from the given list of characters."]
              return render_template('index.html', options=session['options'], errors=errors)
            if session['indchar'] != None:
              session['currentchar'] = char
              session['round'] = 2

          if choice == 4:
            charname = request.form['choice'].capitalize()
            if charname not in session['chars']:
              session['chars'].append(charname)
              session['fullinv'].append([charname])
              session['holding'].append([charname])
              session['currentchar'] = charname
              char = charname
              session['options'] = ["How many items are in " + char +"'s inventory?: "]
              session['round'] = 2
              #return render_template('index.html', options=session['options'], errors=errors)
            else:
              errors = [charname + ' is already in the game. Pick another character.']
            return render_template('index.html', options=session['options'], errors=errors)
          
          if choice == 6:
            session['options'] = inventory.firstquestion()
            session['chars'] = inventory.characters
            session['fullinv'] = inventory.finaltup
            session['holding'] = inventory.charsholding
            session['round']=None
            return render_template('index.html', options=session['options'], errors=errors)



        if session['round'] == 2:
          if choice == 1:
            session['options'] = inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
            session['options'].append("")
            session['options']+=inventory.firstquestion()
            session['round']=None
            session['indchar']=None
            session['currentchar']=None
            session['currentchoice']=None
            return render_template('index.html', options=session['options'], errors=errors)

          if choice==2:
            session['options'] = ["This is what is in " +char+ "'s inventory.", ""]
            session['options'] += inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
            session['options'].append("")
            choice1a = "What is the first item you would like " +str(char)+ " to hold from the inventory?"
            choice2a = "What is the second item you would like " +str(char)+ " to hold from the inventory?"
            session['round'] = 3
            return render_template('next.html', options=session['options'], choice1a=choice1a, choice2a=choice2a, errors=errors)

          if choice == 3:
            session['options'] = ["These are the items in " + char + "'s inventory.", ""]
            session['options'] += inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
            session['options'].append("")
            session['options'].append("What would you like to add?: ")
            session['round'] = 3
            return render_template('index.html', options=session['options'], errors=errors)
          
          if choice == 4:
            num = request.form['choice']
            try:
              session['vals'] = int(num)
            except:
              errors = [num + " is not a number. Enter the number of items in " +session['currentchar']+ "'s inventory."]
            if session['vals'] is not None:
              vals = session['vals']
              session['options'] = ["Enter each of the items below: "]
              session['round'] = 3
              return render_template('next1.html', options=session['options'], errors=errors, vals=vals)
            return render_template('index.html', options=session['options'], errors=errors)
          
          if choice == 5:
            session['options'] = ["This is in " + char + "'s inventory.", ""]
            session['options'] += inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
            session['options'].append("")
            session['options'].append("What would you like to remove?: ")
            session['round'] = 3
            return render_template('index.html', options=session['options'], errors=errors)


              

            

        if session['round'] == 3:
          if choice == 2:
            choice1a = "What is the first item you would like " +str(char)+ " to hold from the inventory?"
            choice2a = "What is the second item you would like " +str(char)+ " to hold from the inventory?"
            choice1 = request.form['choice1'].lower()
            choice2 = request.form['choice2'].lower()
            session['item1']=None
            session['item2']=None
            try:
              session['item1'] = session['fullinv'][session['indchar']].index(choice1)
            except:
              errors.append(choice1 + " is not in " +char+ "'s inventory. Pick items from the inventory.")
              
            try:
              session['item2'] = session['fullinv'][session['indchar']].index(choice2)
            except:
              errors.append(choice2 + " is not in " +char+ "'s inventory. Pick items from the inventory.")
            if session['item1'] is not None and session['item2'] is not None:
              if choice1 == choice2:
                errors.append("You cannot choose two of the same items. Pick two different items from the inventory.")
              else:
                session['options'] = [inventory.modify_holding(session['holding'], session['fullinv'], session['indchar'], session['item1'], session['item2'])]
                session['options'].append("")
                session['options'] += inventory.firstquestion()
                session['round']=None
                session['indchar']=None
                session['currentchar']=None
                session['currentchoice']=None
                session['item1']=None
                session['item2']=None
                return render_template('index.html', options=session['options'], errors=errors)
            return render_template('next.html', options=session['options'], choice1a=choice1a, choice2a=choice2a, errors=errors)
          if choice == 3:
            newitem = request.form['choice'].lower()
            if newitem not in session['fullinv'][session['indchar']]:
              session['fullinv'][session['indchar']].append(newitem)
              session['options'] = inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
              session['options'].append("")
              session['options']+=inventory.firstquestion()
              session['round']=None
              session['indchar']=None
              session['currentchar']=None
              session['currentchoice']=None
              
            else:
              session['options']=["That item is already in " + char + "'s inventory. Choose an item not already in the inventory","","These are the items currently in " + char + "'s inventory", ""]
              session['options'] += inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
              session['options'].append("")
              session['options'].append("What would you like to add?: ")
            return render_template('index.html', options=session['options'], errors=errors)
          
          if choice == 4:
            itemlist = []
            vals = session['vals']
            for i in range(vals):
              item = request.form['choice['+str(i)+']'].lower()
              if item in itemlist:
                errors = ["Do not use duplicate items. Enter unique items in the list"]
                return render_template('next1.html', options=session['options'], errors=errors, vals=vals)
              else:
                itemlist.append(item)
            session['fullinv'][-1] += itemlist
            length = len(itemlist)
            if length >= 2:
              session['holding'][-1].append(itemlist[0])
              session['holding'][-1].append(itemlist[1])
            elif length>1:
              session['holding'][-1].append(itemlist[0])
              session['holding'][-1].append("")
            else:
              session['holding'][-1].append("")
              session['holding'][-1].append("")
            session['options'] = inventory.print_inv(session['fullinv'], session['holding'], -1)
            session['options'].append("")
            session['options'] += inventory.firstquestion()
            session['round'] = None
            session['indchar']=None
            session['currentchar']=None
            session['currentchoice']=None
            session['vals']=None
            return render_template('index.html', options=session['options'], errors=errors)

          if choice==5:
            itemremove = request.form['choice'].lower()
            itemlist = session['fullinv'][session['indchar']]
            if itemremove not in itemlist:
              errors = ["This item is not in the list. Choose an item from the list."]
            else:
              session['fullinv'][session['indchar']].remove(itemremove)
              if itemremove in session['holding'][session['indchar']]:
                session['holding'][session['indchar']].remove(itemremove)
              session['options'] = ["These are now the items in " + char + "'s inventory. ", ""]
              session['options'] += inventory.print_inv(session['fullinv'], session['holding'], session['indchar'])
              while len(session['holding'][session['indchar']])<3:
                session['holding'][session['indchar']].append("")
              session['options'].append("")
              session['options'] += inventory.firstquestion()
              session['round'] = None
              session['indchar']=None
              session['currentchar']=None
              session['currentchoice']=None

              

            return render_template('index.html', options=session['options'], errors=errors)


              

          
            
              





            

              




      try:
        session['currentchoice'] = int(request.form['choice'])
      except:
        errors = "{!r} is not a number. Enter a whole number 1-6.\n".format(request.form['choice'])
      if session['currentchoice'] != None:
        choice = session['currentchoice']
        if (choice == 1 or choice == 2 or choice == 3 or choice == 5):
          session['options'] = inventory.pickChars(session['chars'])
        elif choice == 4:
          session['options'] = ["What is the name of the character you would like to add?: "]
        elif choice == 6:
          session['options'] = ["Great game!"]
          session['round'] = 1
          return render_template('end.html', options=session['options'], errors=errors)
        session['round'] = 1
        


      return render_template('index.html', options=session['options'], errors=errors)
      
        


        

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
        session['choice'] = None
        session['vals'] = None


    return render_template('index.html', options=session['options'], errors=errors)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
