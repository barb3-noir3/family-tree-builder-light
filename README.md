# family-tree-builder-light

This programme creates a family tree with a user interface to add, edit and delete family members.
You can use it for your own family, for monarchs/families you want to study, or for fictional characters.
At the moment I don't know how many generations it can handle, but I think it can handle a lot of them.
The export format is svg, so you can print it in a large format and it stays clear.
This version is a standalone version, I called it the light version because I'm not going to update it. It works as is.

Author: Barb3 Noire3

Date: 02/02/2025

Version: 1.0

Licence: GNU General Public License v3.0 

# Description

I'm a big fan of genealogy and family tree building, I was building my own manually but started to struggle at the 5th generation.
I didn't want to have my own family tree on an online platform wondering if it could be visible to anyone, so I started this project.

## How it Works ?

You have a visual interface to visualize the data you saved and can create a family tree in svg format to visualize it. The infos of each person is represented on what I call the "card".

You can:

* Create a new card
* Edit an existing card
* Delete the currently selected card
* Generate the family tree based on the data provided in the csv
* Visualize the data after each update in the user interface

### Main

Here are the variables for each card:

* ID: It is unique for each person, it will help the module to generate the tree.
* No Gen: This is the generation number of the person. The youngest generation is 1, then the parents are 2, the grandparents are 3 and so on.
* Surname:
* Name:
* Gender: Male or Female, it will then create cards in light pink or light blue to help visualisation in the family tree.
* Date of birth: Its format is dd/mm/yyyy.
* Date of Death: Its format is dd/mm/yyyy, but if the person is still alive, tick the box "Is Alive" and it will assign the value "Unknown" to the date of death.
* Birthplace:
* Job : You can leave this blank, it will create a blank space on the card between the dates and birthplace.
* ID Spouse: If the person is not married, you can leave it blank. It will show an error if it is the same ID as the current card.
* ID Mother: The mother comes first, it will show an error if it is the same ID as the current card.
* ID Father: It will show an error if it is the same ID as the current card.
  
### Tree Generation

After entering some data into the csv, click on the generate tree button and it will export the family tree in .svg format.
The tree will have a line for each generation, so be careful and check that you don't have any errors.
For the married person, it will create an intermediate dot where the spouse arrows merge and then are links to the children.
I don't know how many generations it can handle before it gets difficult to understand and I don't know how many people you can have on it.
You don't have to add an ID for spouse, father or mother. Even if you don't know the father of an ancestor, you can just leave it blank.

## Limitations

The model can't handle multiple spouses. 
Let's say a father has 2 children from a first marriage and then another child from his second marriage. 
The 3 children will be related to their father, but the second wife will not be related to her child.
The family tree could not be very nice if you have a generation with tens of children, because each one is linked to its parents by the intermediate dot.
It could be difficult to manage the ID of people when you have 100+ people in your tree, so maybe you could manage like this:

* For the first 3 generations: children, parents, grandparents do it normally, so you'll be ID 1, your parents ID 2 & 3, your grandparents 4 & 5 and 6 & 7.
* Then maybe you could focus on each branch at a time, so your grandmother's (mother's) family, then grandfather's (mother's) family and so on. Be careful with the ID and the No Gen.

## Modules
I use:

* Pandas
* Tkinter
* Numpy
* Datetime
* Tkcalendar
* os
* graphviz

# Example

Here you can see an example based on the family tree of the king Charles III of the UK. I do not know if all infos are accurate as it was autocompleted by AI.
In this example I have 34 persons on 5 levels of generation.
![image](https://github.com/user-attachments/assets/c29106ee-f638-4a89-a61f-d56513db2c23)
![family_tree](https://github.com/user-attachments/assets/58e869b6-5d47-466a-9f26-ba10eb352ea1)<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"

# Have fun! 😀



