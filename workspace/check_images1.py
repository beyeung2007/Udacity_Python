#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# TODO: 0. Fill in your information in the programming header below
# PROGRAMMER: Jim  
# DATE CREATED: 12 June 2018
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print 
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # TODO: 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()
    
    # TODO: 2. Define get_input_args() function to create & retrieve command
    # line arguments
    in_arg = get_input_args()
    ##print ("Arg 1 = ", in_arg.dir, "\nArg 2 = ", in_arg.arch, "\nArg 3 = ", in_arg.dogfile)
    
    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    #in_arg is called to find the "dir" parameters --> retreive the address for "pet_images"
    answers_dic = get_pet_labels(in_arg.dir)
    
    #Followings is to check: 1) 40 items in dictionary  2) key = filename; value = label 
    # 3) label names are correctly formatted 
    ##print ("\nanswers_dic has ", len(answers_dic), " key-value items", 
    ##       "\nBelow are ten of them")
    ##count = 0
    ##for key in answers_dic:
    ##    if count < 10:
    ##        print ("%2d key: %-30s  label: %-26s" % (count+1, key, answers_dic[key])) 
    ##    count += 1

        
    # TODO: 4. Define classify_images() function to create the classifier 
    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)
    #print ("The result_dic is: ", result_dic)
    no_match = 0
    no_not_match = 0
    print ("\nMatch: ")
    
    for key in result_dic:
       print ("The type of key is: ", type(key))
       print ("the key is: ", key)
       if result_dic[key][2] == 1:
         no_match += 1
         print ("\nReal: %-26s  classifier: %-30s" % (result_dic[key][0], 
                                                      result_dic[key][1]))  
    print ("\nNot a Match: ")       
    for key in result_dic:
       if result_dic[key][2] == 0:
         no_not_match += 1
         print ("\nReal: %-26s  classifier: %-30s" % (result_dic[key][0], 
                                                      result_dic[key][1])) 
                   
    print ("Total number: ", no_match + no_not_match, "\nTotal number of match: ", 
           no_match, "\nTOtal number of not_match: ", no_not_match)               

    #Check the details 


    
    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog()

    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats()

    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results()

    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    ##print("\n** Total Elapsed Runtime:", "{}:{}:{}".format(str(int(tot_time//3600)), str(int((tot_time%3600)//60)), str(int((tot_time%3600)%60))))






# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    #Creating a Argument Parser Object named "parser"
    parser = argparse.ArgumentParser()
    
    #Creating argument 1 = directory of path of the pet images
    parser.add_argument('--dir', type=str, default='pet_images/', help='Get the path of the file')
    
    #Creating argument 2 = CNN architecture 
    parser.add_argument('--arch', type=str, default='vgg', help='Choose a CNN model: resnet, alexnet or vgg')
    
    #Creating argument 3 = dog'name
    parser.add_argument('--dogfile', type=str, default='dognames.txt', help='Dog files that has dog\'s name')
    
    return parser.parse_args()


#image_dir is the parameters representing images in pet_images
#the images are retrieved by in_arg = get_input_args()
def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
"""
    #Import listdir function from os module
    from os import listdir
    
    #Retreive the file name from file: pet_images
    filename_list = listdir(image_dir)
    ##filename_list = listdir("pet_images/")
    
    #Creating a pet dictionary
    pet_dic = dict()
    
    #determine number of items in dict
    items_in_dict = len(pet_dic)
    ##print ("\nEmpty Dictionary pet_dic - n items = ", items_in_dict)
    
    #Create a pet_label_list to store the pet labels
    #This list will be combined with filename_list later
    pet_label_list = []
    
    #Iterate through the list and retreive the name by using for loop
    #pet_label is created for each idx item/variable
    for idx in range(0,len(filename_list),1):
        
        #Skips file if starts with "." (such as .DS_Store of MAC OS)which isn't an image
        if filename_list[idx][0] != ".":
            
            ##print("\n%2d file: %-25s" % (idx + 1, filename_list[idx]))
            image_names = filename_list[idx].split("_")

            pet_label = ""

            #The following part is examining each file names 
            for word in image_names:
                if word.isalpha(): #Check if the image_names contain alphabetic characters only
                   pet_label += word.lower() + " "
        #remove the starting/tailing whitespaces characters 
            pet_label = pet_label.strip()
        
            if filename_list[idx] not in pet_dic:
               pet_dic[filename_list[idx]] = pet_label
            else:
               print("Warning: Duplicate files exist in directory", 
                     in_files[idx])
        #append each pet_label into pet_label_list
        #pet_label_list.append(pet_label)

    ##Zip two lists (pet_label, filename_list) into dictionary
    ##pet_dic = dict(zip(filename_list,pet_label_list))
    ##print (type(pet_dic))
    
    #return the pet_dic as a result of this function
    return (pet_dic)
    ##print ("This is the pet_label_list: " + str(pet_label_list) + "\n\nThis is filename_list: " + str(filename_list))
    #Extracting the animal labels from each picture ---- label_list = [name.split("_")[0] for name in filename_list]
    #print("\nThe animal labels of each picture are shown as below: ")
    
def classify_images(image_dir, pet_dic, model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
    #Creating a dictionary for comparison results 
    #the key is the filename
    #value is a list consists of [pet_image_label, classifier_label, 1/0] **1/0 = match or not
    results_dic = dict()
    
    #Retreive the files in pet_dic
    #The key is the filename
    for key in pet_dic: 
        
        #Create a model label by using the input (image address = image_dir + filename) and (model)
        #print ("the key is: ", key)
        model_label = classifier(image_dir + key, model)
        
        #Edit the format of the model label allows for comparing with pet_dic
        model_label = model_label.lower()
        model_label = model_label.strip()
        
        #We need to match the key in pet_dic to key in model_label
        #string function .find() allows us to find the key interested in model_label in classifier
        truth = pet_dic[key]
        found = model_label.find(truth)
        
        if found >= 0:
            if ( (found == 0 and len(truth)==len(model_label)) or
                (  ( (found == 0) or (model_label[found - 1] == " ") )  and
                   ( (found + len(truth) == len(model_label)) or   
                      (model_label[found + len(truth): found+len(truth)+1] in 
                     (","," ") ) 
                   )      
                )
              ):        
                #Define the label/key with list value if the label/key match with model_label in classifier
                #if condition makes sure there is no duplicaiton in results_dic
                if key not in results_dic:
                    results_dic[key] = [truth, model_label, 1]
            #Define the label/key if the label/key is not standalone, i.e. being a part of other words
            #For example, we dont want to find "apple" in "appliepie"
            else: 
                if key not in results_dic:
                    results_dic[key] = [truth, model_label, 0]
        #Define the case when found <0, i.e it returns -1
        else:
            if key not in results_dic:
                results_dic[key] = [truth, model_label, 0]
    return (results_dic)

def adjust_results4_isadog():
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """           
    pass


def calculates_results_stats():
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    pass


def print_results():
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    pass

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()
