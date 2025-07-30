def main():

    # This is a study quiz game in which users create their own questions and quiz themselves. They input their questions, answers, and correct answers and get a score based on the number of correct answers they get. 

    print('Welcome to the study quiz game!')
    print('\nHere are the rules of the game: \nYou create your own questions\nEach correct answer is 5 points\nEach wrong answer is 0 points\nYour total points after answering all of the questions is your final score.')

    # Step 3
    def readQuestions():
        questions_list = []
        # Open and read quiz file
        with open('quiz-questions.txt', 'r') as myfile:
            unformatted_questions = myfile.readlines()
        # Append questions, answer choices and correct answers as elements in the questions list. 
        for lines in unformatted_questions:
            # There are newline characters in the file, so to remove them use .strip()
            #https://codedamn.com/news/python/remove-newline-from-string
            questions_list.append(lines.strip().split('|'))

        answers_list = []
        # Create copy of questions list
        for elements in questions_list:
            new_list = elements[:]  
            answers_list.append(new_list)

        # Remove the question (first element index [0]) and the correct answer (last element index[-1]) from the questions list, leaving correct answers for the answers list since formatting instructions indicate that first element (0) is always the question and the last element (-1) is always the correct answer 
        for question_element in answers_list:
            question_element.pop(0)
            question_element.pop(-1)
        
        # Return questions_list and answers_list as a tuple
        return (questions_list, answers_list)

    # Step 4
    def getScore(quantity_correct):
        # Add points for correct answers and no points for incorrect answers
        final_score = quantity_correct * 5
        return final_score

    # Step 5
    def playAgain():
        # After all of the questions have been answered, give score and prompt user if they want to play again or exit
        while True:
            try:
                play_again = input('\nWould you like to play again? Enter "Y" to play again, enter "N" to quit: ').upper()
                if play_again == 'Y':
                    while True:
                        same_questions = input('\nWould you like to use the same questions or create new ones? Enter "SQ" for same questions. Enter "NQ" for new questions: ').upper()
                        if same_questions == 'SQ':
                            print('-------------------------------------------- Same Questions --------------------------------------------')
                            # Repeat Step 2
                            startGame()
                            break
                        elif same_questions == 'NQ':
                            print('-------------------------------------------- New Questions --------------------------------------------')
                            # Repeat Step 1
                            createQuestions()
                            break
                        else:
                            print('ERROR: Please enter "SQ" or "NQ"!')
                            continue
                elif play_again == 'N':
                    print('Quiting the game! Goodbye!')
                    break
                else:
                    raise ValueError
            except ValueError:
                print('ERROR: Please enter "Y" or "N"!')
                continue

            
                

    # Step 2
    def startGame():
        # Unpack the questions_list and answers_list tuples and associate questions_list with questions and answers_list with answers
        questions, answers = readQuestions()
        # Initialize string to be used for verifying answer choices and display choice of answers. 
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        # Display questions and answers and prompt user to answer by selecting one of the multiple choice answers
        while True:
            num_correct_answers = 0
            print('\nThe game is now starting! Enter "Q" to quit!\n')
            for index, quiz_questions in enumerate(questions):
                # print the questions, which is the first element [0] of the current element [index] in questions list
                print(f'{questions[index][0]}')
                # get the associated list of answers from answers list
                current_answer = answers[index]

                # get the associated slice of letters from the letters string based on the length of current_answer list. E.g. if the current_answer has 4 elements/answers, then the slice of letters is 'ABCD'
                letter_length = letters[0:len(current_answer)]

                # print the current question's answers
                for quiz_answers in current_answer:
                    print(f'{quiz_answers}')
                letter_list = ''

                # create string for letter list to display in answer prompt (Answer (A, B, C, D))
                for curr_letter in letter_length:
                    # Concatenates the letters from the letters slice and adds a comma between all of them. E.g. from letter slice 'ABCD', it creates: 'A, B, C, D, '
                    letter_list += f'{curr_letter}, '
                while True:
                    # Input with instructions to enter a valid answer from the letter_list. It displays a slice of letter_list (letter_list[0:(len(letter_list)-2)]), removing the last two indexes because the trailing ', ' is not needed to be displayed. 
                    current_question = input(f'Answer ({letter_list[0:(len(letter_list)-2)]}): ').upper() 
                    
                    # Exit the game completely
                    if current_question == 'Q':
                        print('\nExiting game...')
                        return

                    # https://www.squash.io/how-to-check-if-something-is-not-in-a-python-list/
                    # Error handling if the input the user gives is not a valid answer from letter_list
                    if current_question not in letter_list:
                        print(f'\nERROR: The input you entered is not an answer choice! Please enter one of the following: ({letter_list[0:(len(letter_list)-2)]})')
                        continue
                    break

                # Increment correct answer if it mathces the correct answer element in questions list (which is the last element in questions list [-1])
                if current_question == (questions[index][-1].upper()):
                    num_correct_answers += 1
                    
                
                print()
            
            # Call getScore function with argument of the quantity of correct answers
            final_score = getScore(num_correct_answers)
            print(f'\nYour final score is : {final_score}!')

            # End the loop when at the end of questions if the index is equal to the length of questions list minus 1. 
            if index == (len(questions)-1):
                break
        # Ask user if they would like to play again after display final score
        playAgain()

    # Step 1
    def createQuestions():
        # Instructions:
        print('\nLet\'s start by creating some questions')
        print('\nEnter your multiple choice questions with this exact format: "Question|Answers|Correct Answer(Letter)"')
        print('An example question with proper formatting is: "What is the capital of Japan?|A. Beijing| B. Seoul|C. Tokyo|D. Bangkok|C"')
        print('Each question should be seperated with a \'|\' character between the questions, answers, and correct answer.')
        print('Make sure for each question to include letter in front of each answer (e.g. A. Beijing| B. Seoul[...] etc.)')

        with open('quiz-questions.txt', 'w') as quizfile:
            questions_input = ''
            while questions_input != 'd' and questions_input != 'D':
                questions_input = input('\nNow enter quiz questions (remember to use the correct format!"). Enter "D" when done to start the game with your questions!: ')
                # Basic error handling for formatting
                if questions_input != 'd' and questions_input != 'D' and questions_input.count('|') >= 3:
                    quizfile.write(f'{questions_input}\n')
                elif questions_input == 'd' or questions_input == 'D':
                    break
                elif questions_input.count('|') < 3 or len(questions_input) < 4:
                    print("ERROR: Please check your formatting! Correct format is: Question|Answers|Correct Answer(Letter)")
                    continue

        startGame()

    # intially starting the game by doing Step 1: Creating Questions
    createQuestions()