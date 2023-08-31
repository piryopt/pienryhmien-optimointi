### Steps of the Hungarian algorithm
The algorithm is based on the steps presented on [hungarianalgorithm.com](https://www.hungarianalgorithm.com/hungarianalgorithm.php) and uses the [SciPy optimize function linear_sum_assignment](https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html) for the group assignment once the matrix has been modified to the correct form. linear_sum_assignment covers steps 5-7
The steps 3-6 presented below follow steps 1-4 on hungarianalgorithm.com

**Step 1: Create an nxn matrix where each row represents a student, each column represents a space open for a student, and the cells represent the profit of placing a student to a group**
- If a choice in the questionnaire has multiple spaces, represent each of these with a column. These columns are identical with each other
- If there are more spaces open than there are students, add empty rows to match the number of rows to the number of columns
- The cell values are calculated as profits based on how the student has ranked the group (see Weights at the bottom of this page)

**Step 2: Transform profit matrix to cost matrix**
- Find the maximum value in the matrix
- Invert all values by multiplying with -1
- Add the original maximum value to all cell values

**Step 3: Subtract row minima**
- Find the lowest cell value in each row and subtract it from all values in the row

**Step 4: Subtract column minima**
- Find the lowest cell value in each column and subtract it from all values in the column

**Step 5: Cover all zeros with a minimum number of lines**
- Model drawing lines through each zeroes with minimum number of lines
- If number of lines is equal to n, andoptimal assignment can be found. If not, move to 6

**Step 6: Create additional zeros if needed**
- Find the minimum value that is not covered by a line in Step 5
- Subtract this minimum value from all elements not covered by a line in step 5
- Add the minimum value to all elements that were covered by two lines in step 5
- Repeat Steps 5 and 6 until number of lines drawn matches n

**Step 7: Find optimal combination of zeros**
- Choose zeroes so that no chosen zeroes are on the same column or same row

### Weights
The current weights are a function of the number of students and the number of possible choices. Number of possible choices is the number of groups a student can organize in a list of preferred groups.

The weights class returns a dictionary of values where number of values = number of choices + 2. Keys range from 0 to number of choices - 1. The weights range from highest at 0 to lowest at number of choices -1. The highest weight is number of choices multiplied by (number of students + 2) and each other weight is the previous higher weight - number of students. Keys -1 and Null have the same weight value, that is also the lowest weight.
