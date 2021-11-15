characters = ["Dog", "Cat", "Hamster"]

dog_in = ["ball", "crate", "bone"]

cat_in = ["yarn", "catnip", "nails"]

hamster_in = ["wheel", "bowl", "grass"]


dogtup = [characters[0],] + dog_in
cattup = [characters[1],] + cat_in
hamstertup = [characters[2],] + hamster_in


finaltup = [dogtup, cattup, hamstertup]


char1hold = [finaltup[0][0], finaltup[0][1], finaltup[0][3]]
char2hold = [finaltup[1][0], finaltup[1][2], finaltup[1][3]]
char3hold = [finaltup[2][0], finaltup[2][1], finaltup[2][2]]

charsholding = [char1hold, char2hold, char3hold]

def modify_holding(charsholding, finaltup, charIndex, item1, item2):
    charsholding[charIndex][1] = finaltup[charIndex][item1]
    charsholding[charIndex][2] = finaltup[charIndex][item2]
    return print_holding(charsholding, charIndex)
    #print(charsholding[charIndex][0] + " is holding the " +charsholding[charIndex][1]+ " and the " +charsholding[charIndex][2]+ ".")
    
    
def print_inv(charlist, charhold, charIndex):
  chars = []
  char = charlist[charIndex]
  chars.append(char[0])
  linebreak = ''
  for i in range(len(chars[0])+3):
    linebreak = linebreak + "-"
  chars.append(linebreak)
  for item in range(1, len(char)):
    chars.append(char[item])
  chars.append("")
  chars.append(print_holding(charhold,charIndex))
  return chars
    
  
  


def print_holding(charsholding, charIndex):
    while len(charsholding[charIndex]) < 3:
        charsholding[charIndex].append("")
    return charsholding[charIndex][0] + " is holding the " +charsholding[charIndex][1]+ " and the " +charsholding[charIndex][2]+ "."

def firstquestion():
    val = ["These are your options", "", "1: Print a  character's inventory", "2: Modify what a character is holding", "3: Add to a character's inventory", "4: Add a new character", "5: Removing Items", "6: Quit", "", "What would you like to do? Enter a number 1-6: "]
    #make sure they chose a valid option  
    return val

def pickChars(chars):
  opt = ["These are the characters in the game: ", "", chars,"", "Which character do you want?: "]
  return opt


def main():
  #ask what they want to do
  firststep = firstquestion()

      
  while firststep != 6:
      #ask which character to use
      if firststep == 1 or firststep == 2 or firststep == 3 or firststep == 5:
          whichchar = input("These are the characters in the game: \n" + str(characters) + "\nWhich character do you want?: ")
          whichchar = whichchar.capitalize()


          #Make sure they chose a valid character
          while whichchar not in characters:
                  whichchar = input("That is not a character. These are the characters in the game: \n" + str(characters) + "\nWhich character do you want?: ")
                  whichchar = whichchar.capitalize()
          print("")

          #get the index of the character in the character list
          indchar = characters.index(whichchar)
              
      #print if they choose option 1. Add item if they choose option 2.
      if firststep == 1:
          print_inv(indchar)
      elif firststep == 2:
          print("This is " +whichchar+ "'s inventory: ")
          print_inv(indchar)
          item_to_change = input("What is the first item you would like " +whichchar+ " to be holding from the inventory?: ")
          while item_to_change.lower() not in finaltup[indchar]:
              item_to_change = input("That is not in " +whichchar+ "'s inventory. What is the first item you would like " +whichchar+ " to be holding from the inventory?: ")
          item_to_change2 = input("What is the second item you would like " +whichchar+ " to be holding from the inventory?: ")
          while item_to_change2.lower() not in finaltup[indchar]:
              item_to_change2 = input("That is not in " +whichchar+ "'s inventory. What is the second item you would like " +whichchar+ " to be holding from the inventory?: ")
          while item_to_change2.lower() == item_to_change.lower():
              item_to_change2 = input("You already chose that item. What is the second item you would like " +whichchar+ " to be holding from the inventory?: ")

          indItem1 = finaltup[indchar].index(item_to_change.lower())
          indItem2 = finaltup[indchar].index(item_to_change2.lower())
          modify_holding(indchar, indItem1, indItem2)
      
      elif firststep == 3:
          item_to_add = input("What would you like to add to " +whichchar+ "'s inventory?: ")
          finaltup[indchar].append(item_to_add.lower())
          print_inv(indchar)
      elif firststep == 4:
          char_to_add = input("What is the name of your character?: ")
          char_to_add = char_to_add.capitalize()
          characters.append(char_to_add)
          charinv = [char_to_add]
          newcharhold = [char_to_add]
          num_items = int(input("How many items are in the character's inventory?: "))
          for x in range(num_items):
              item_to_add = input("Enter an item: ")
              charinv.append(item_to_add.lower())
              if x < 2:
                  newcharhold.append(item_to_add.lower())
          indchar = len(finaltup)
          finaltup.append(charinv)
          charsholding.append(newcharhold)
          print("")
          print_inv(indchar)
      elif firststep == 5:
          print("This is your character's inventory: ")
          print_inv(indchar)
          item_to_remove = input("Which item would you like to remove?: ")
          item_list = finaltup[indchar][1:]
          
          while item_to_remove.lower() not in item_list:
              item_to_remove = input("Invalid item. Which item would you like to remove?: ")
          finaltup[indchar].remove(item_to_remove.lower())
          if item_to_remove.lower() in charsholding[indchar]:
              charsholding[indchar].remove(item_to_remove.lower())
          print("")
          print_inv(indchar)
          
          
          

      firststep = firstquestion()

if __name__ == "__main__":
  main()