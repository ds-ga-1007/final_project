#!/usr/bin/env python3
'''
Main class for the program. 

It provides two types of plots and related statistics for diferent diseases:

Plot heatmap:
User prompts six options of diseases (Measles, Hepatitis_A, Rubella, Poliomyelitis, Smallpox and Mumps)
to see the trend of decreasing number of infective people over time and its relation to the invention 
of vaccines.Generally the plot will show a distinctive declined density after vaccines were introduced.

Plot geo-heatmap:
show the geological distribution of certain disease over different states in a certain year. 
User can choose over fifty diseases and certain year which is in the range of relative disease 
with their preferred color. By entering 'help', the list of diseases can be shown. 
Generally, if you try different years for a fixed disease, the distribution will change over time.

User could enter 'quit' to switch the mode of plot 
       or  enter 'exit' to stop the program or by keyboard interrupt.

'''
from plot_heatmap import heatmap_Measles, heatmap_Hepatitis_A, heatmap_Mumps, \
                         heatmap_Poliomyelitis, heatmap_Smallpox, heatmap_Rubella
from exception_class import *
from statistics import get_mean, display_mean
from object_class import *
import sys

def main():
    while True:
        try:
            plot_type = input('Please choose one of the following kind of plot:\n Heatmap or Geo-heatmap\n')
            if plot_type.upper() == 'EXIT':
                print('EXIT!')
                sys.exit(0)
            elif plot_type.upper() not in ['HEATMAP', 'GEO-HEATMAP']:
                raise plottypeException()
            elif plot_type.upper() == 'HEATMAP':
                while True:
                    try:
                        print('-Available diseases are Measles, Hepatitis_A, Rubella, Poliomyelitis, Smallpox and Mumps.')
                        data = input('Please enter the name of disease: ').lower()
                        data = data.replace(" ", "")  # eliminating any space by mistakenly input
                        valid_list = ['measles', 'hepatitis_a', 'rubella', 'poliomyelitis', 'smallpox', 'mumps']
                        
                        if data == 'quit':
                            break
                        if data == 'EXIT':
                            print('EXIT!')
                            sys.exit(0)
                        if data.isdigit():
                            raise DigitError
                        if data not in valid_list:
                            raise InvalidDisease
             
                        if data == 'measles':
                            mean_before = get_mean('measles')[0]
                            mean_after = get_mean('measles')[1]
                            display_mean(mean_before, mean_after)
                            heatmap_Measles()
                        
                        if data == 'hepatitis_a':
                            mean_before, mean_after = get_mean('hepatitis a')
                            display_mean(mean_before, mean_after)
                            heatmap_Hepatitis_A()
                        
                        if data == 'rubella':
                            mean_before, mean_after = get_mean('rubella')
                            display_mean(mean_before, mean_after)
                            heatmap_Rubella()
                        
                        if data == 'poliomyelitis':
                            mean_before, mean_after = get_mean('poliomyelitis')
                            display_mean(mean_before, mean_after)
                            heatmap_Poliomyelitis()
                        
                        if data == 'smallpox':
                            mean_before, mean_after = get_mean('smallpox')
                            display_mean(mean_before, mean_after)
                            heatmap_Smallpox()
                        
                        if data == 'mumps':
                            mean_before, mean_after = get_mean('mumps')
                            display_mean(mean_before, mean_after)
                            heatmap_Mumps()
                    
                    except KeyboardInterrupt:
                        print('Interrupted')
                        sys.exit(0)
                    except ValueError:
                        print('Invalid input!')
                    except DigitError:
                        print('Only string disease name are valid for Heatmap!')
                    except InvalidDisease:
                        print('This is not a existing disease in our dataset, plz re-entry a name. ')
             
             
                        
            elif plot_type.upper() == 'GEO-HEATMAP':
                while True:
                    try:
                        print('-Enter the disease name to see the geo-heatmap of disease and vaccines.')
                        print('-There are more than fifty diseases offered.\n')
                        user_color = input('Please enter the color of heatmap, the color should be a float number from 0 to 1:\n')  # documentation add the circle of color\
                        if user_color.lower() == 'exit':
                            print('EXIT!')
                            sys.exit(0)
                        if user_color.lower() == 'quit':
                            break  
                        user_color = color_class(user_color)
                        user_disease = input('Please enter the disease you want to see,for example: MUMPS,MEASLES or input \'help\' to see full list of available diseases\n').upper()
            
                        if user_disease.lower() == 'exit':
                            print('EXIT!')
                            sys.exit(0)
                        if user_disease.lower() == 'quit':
                            break  
                        if user_disease.lower() == 'help':
                            print(disease_list)
                            user_disease = input('Please enter the disease you want to see,for example: MUMPS,MEASLES or input \'help\' to see full list of available diseases\n').upper()
                        user_disease = disease_class(user_disease)
                        print(user_disease)
                        user_year = input('Please enter the year\n')
                        if user_year.lower() == 'exit':
                            print('EXIT!')
                            sys.exit(0)
                        if user_year.lower() == 'quit':
                            break  
                        user_year = year_class(user_year, user_disease.name)    
                        num_for_year = get_std_data_by_year(user_year.year, user_disease.name)  
                        plot_map(user_year.year, user_disease.name, user_color.color, num_for_year)
                        
                        
                    except colortypeException:
                        print('the color you input does not meet the criteria, please enter a float\n')
                    except colorrangeException:
                        print('Please choose color in the range of 0-1\n')
                    except diseaseExceptioin:
                        print('This disease is not valid, please enter the disease in the disease list\n')
                    except yeartypeException:
                        print('the year you input is not an integer\n')
                    except yearrangeException:
                        print('The year you input is not valid for this disease, please refill the information and try again\n')

                        
        except plottypeException:
            print('The plot is not valid in this program, please choose between heatmap and geo-heatmap')
        
    

if __name__ == '__main__':
    try:
        print('')
        print("You can type 'Quit' to exit the certain plot type. For example, if you are in heatmap plotting mode, by input 'quit'")             
        print('you can exit the heatmap mode and back to choosing plot type again') 
        print("You can type 'Exit' to end the program\n")
        main()
    except EOFError:
        print()
        print('EXIT!') 
        raise SystemExit()
