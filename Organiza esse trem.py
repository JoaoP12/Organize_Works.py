import pymysql as sql
import pandas as pd
import os
from datetime import date
from enum import Enum

class DataBase:
    
    '''Inserts, edits, deletes, extracts, manipulates the DataBase
    '''
    
    def __init__(self, db_cursor, db_connection):  #self, table_name, ID, wt_date, description_content, table_info, db_cursor, db_connection, subject
        self.db_connection = db_connection
        self.db_cursor = db_cursor
                
    def insert_data(self, table_name, subject_column, date_column, desc_column, work_test_subject, work_test_date, work_test_desc):
        
        '''Inserts a work/test with the info the user provided
        '''
        
        command = f"Insert into {table_name} ({subject_column}, {date_column}, {desc_column}) values ('{work_test_subject}', STR_TO_DATE('{work_test_date}', '%Y-%m-%d'), '{work_test_desc}')"
        self.db_cursor.execute(command)
        self._save_alterations()
        print("Insertion succeeded! ")
    
    def view_data(self, table_name):
        
        '''Selects data from table avaliacoes/trabalhos and show the user
        '''
        
        command = f"Select * From {table_name} Order By `Data`"
        data_frame = pd.read_sql(command, self.db_connection)
        pd.set_option('display.expand_frame_repr', False)
        return data_frame
        
    def delete_data(self, ID, table_name):
        
        '''Deletes a work or a test selected by the user
        '''
        
        command = f"Delete From {table_name} Where ID = {ID}"
        self.db_cursor.execute(command)
        self._save_alterations()
        print("Deleted! \n")
        clean_screen()
        return self.view_data(table_name)
    
    def _save_alterations(self):
        
        '''Saves all the alterations the user made in the DataBase
        '''
        self.db_connection.commit()
        
    def exit_program(self):
        
        '''Closes the connection with the DataBase and closes the DataBase
        '''
        
        self.db_connection.close()  # Closes the connection with the DataBase
        return Options(3)
    
class Options(Enum):
    
    '''Enumerates the options of the main menu to turn them more readable
    '''
    
    WORKS = 1
    TESTS = 2
    EXIT = 3

class ListOptions(Enum):
     
    '''Enumerates the options of the list_works/tests to turn them more readable
    '''
    
    BACKMENU = 1
    ADDWORKTEST = 2
    DELETEREG = 3
    

def string_to_date():
    
    '''Turns the date entered by the user into a DataBase proper date
    '''
    
    year = date.today().year
    month = int(input("Month (number): \n"))
    day = int(input("Day: \n"))
    work_test_date = f"{year}-{month}-{day}"
    return work_test_date
    
def clean_screen():
    
    '''Cleans the user screen
    '''
    
    os.system('cls' if os.name == 'nt' else 'clear')

def options_menu():
    
    '''Shows the start menu with the options the user has
    '''
    
    print("1 - Works\n")
    print("2 - Tests \n")
    print("3 - Exit \n")

def create_work_test(table_name):
    
    '''Creates a new test/work
    '''
    
    work_test_subject = input("What's the subject? ")
    work_test_date = string_to_date()
    work_test_desc = input("Description (content, what to do,etc.): ")
    DB.insert_data(table_name,'Materia', '`Data`', 'Descricao', work_test_subject, work_test_date, work_test_desc)
    return True

def list_works_tests(user_choice):
    
    '''Calls the method DataBase.view_data(*args) and then lists the works/tests to the user
    '''
    
    if user_choice == Options.WORKS:
        table_name = 'trabalhos'
        str_work_test = 'work'
    else:
        table_name = 'avaliacoes'
        str_work_test = 'test'
    
    table_n_choice = []
    table_n_choice.append(table_name)
    data_frame = DB.view_data(table_name)
    print(data_frame)
    bottom_options = f'1-Back to main menu   2-Add new {str_work_test}    3-Delete {str_work_test}'
    user_choice = int(input(bottom_options))
    table_n_choice.append(user_choice)
    return table_n_choice
    
def delete_work_test(table_name):
    
    '''Calls the method of the class DataBase that deletes data and then remove the row from the selected ID
    '''
    
    if table_name == 'trabalhos':
        name = 'work'
    else:
        name = 'test'
    ID = int(input(f"Enter the ID of the {name} you wanna delete or digit a >=0 number to cancel: \n" ))
    
    return DB.delete_data(ID, table_name)
    
def main():

    '''Main function, the one which will start the program and call all the other functions
    '''

    options_menu()
    user_choice = int(input("What do you want to do? (Enter the number of the choice) \n"))  # Asks the user which option will be chosen
    user_choice = Options(user_choice)
    if user_choice == Options.WORKS or user_choice == Options.TESTS:
        clean_screen()
        table_name, user_choice = list_works_tests(user_choice)
        user_choice = ListOptions(user_choice)
        if user_choice == ListOptions.BACKMENU:
            clean_screen()
            return ListOptions(1)
        
        elif user_choice == ListOptions.ADDWORKTEST:
            clean_screen()
            is_work_created = create_work_test(table_name)
            if is_work_created:
                return ListOptions(1)
            
        elif user_choice == ListOptions.DELETEREG:
            clean_screen()
            success = delete_work_test(table_name)
            print(success)
            return ListOptions(1)
                    
    elif user_choice == Options.EXIT:
        return DB.exit_program()
    
    else:
        print("This isn't a valid option, please try again \n")
        return ListOptions(1)

connection = sql.connect(db='trabalhos', user='root', passwd='')
fcursor = connection.cursor()
DB = DataBase(fcursor, connection)

x = main()  # Calls the function 'main' into a variable because then it's possible to put it into a loop that just stops when the user says so
while x != Options.EXIT: # If x = 3 then the program will be killed
    clean_screen() 
    x = main()