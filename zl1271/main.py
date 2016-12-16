'''
Created on Dec 12, 2016

@author: felix
'''
from main_funcs import *
from Data import *
from Correlation import *

def main():
    while True:
        try:
            begin_game_instructions()    
            user_input_str = get_valid_user_input()
            
            if clean_str(user_input_str) == 'quit':
                pass
            elif clean_str(user_input_str) == 'all':
                run_all_model()
            elif clean_str(user_input_str) == 'explore':
                run_explore()
            else:
                raise Exception
            
            break

        except KeyboardInterrupt:
            break
        except:
            print('Unexpected input')
            pass
    print('Program finished')
    
if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass