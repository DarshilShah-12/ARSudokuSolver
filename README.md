# ARSudokuSolver
This is a basic augmented reality project I picked up to learn more about computer vision and gain experience using the OpenCV library in Python. Upon being shown an incomplete sudoku board on a camera through a live video feed, I augment the missing digits back onto the board in real-time. As I primarily wanted to focus on the computer vision part of this project, I used an existing sudoku solver developed by Alex Beals. That repo can be found here: https://github.com/dado3212/Sudoku-Solver.

# Input / Output
<p align="middle">
  <img src="visual_media/1_input_image.jpg" height=363/>
  <img src="visual_media/7_final_image.jpg" height=363/>
</p>

# Approach Overview
To solve this problem, I first isolate the sudoku board from the rest of the environment. I then evenly split up the board to crop even smaller images of the 81 cells. Using a convolutional neural net trained for 10 potential image inputs (digits from 1-9 as well as a blank input), I was able to determine exactly what digits are present and where they lie on the board. I reformatted this information to fit the sudoku solver and upon parsing the solved return value, I populated the cells with missing digits to produce the final result.

# Image Processing
This project was quite heavy on image processing as I needed to ensure I got the most accurate results for digit localization and recognition. In this subsection, I will briefly go over some of the transformations I applied and explain why I believed they were necessary.

# Disclaimer
