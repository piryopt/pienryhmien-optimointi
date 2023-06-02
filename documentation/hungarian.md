### Steps of the Hungarian algorithm
The algorithm is based on the steps presented on [hungarianalgorithm.com](https://www.hungarianalgorithm.com/hungarianalgorithm.php) and uses the [SciPy optimize function linear_sum_assignment](https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html) for the group assignment once the matrix has been modified to the correct form, this covers steps 5-7
The steps 3-6 presented below follow steps 1-4 on hungarianalgorithm.com

**Step 1: Create an nxn matrix where each row represents a student, each column represents a spot open for a student, and the cells represent the profit of placing a student to a group**
- If a group has multiple spots represent each of these with a separate column
- If there are more spots open than there are students, add empty rows to match the number of rows to the number of columns
- The cell values are calculated as profits based on how high the student has placed the group on their ranked list

**Step 2: Transform profit matrix to cost matrix**
- Find maximum value in the matrix
- Invert all values by multiplying by -1
- Add the original maximum value to all cell values

**Step 3: Subtract row minima**
- Find the lowest cell value in each row and subtract it from all values in the row

**Step 4: Subtract column minima**
- Find the lowest cell value in each column and subtract it from all values in the column

**Step 5: Cover all zeros with a minimum number of lines**
- model drawing lines through each zeroes with minimum number of lines
- if number of lines is equal to n, and optimal assignment can be found, if not move to 6

**Step 6: Create additional zeros if needed**
- Find the minimum value that is not covered by a line in Step 5
- Subtract this minimum value from all elements not covered by a line in step 5
- Add the minimum value to all elements that were covered by two lines in step 5
- Repeat Steps 5 and 6 until number of lines drawn matches n

**Step 7: Find optimal combination of zeros**
- Choose zeroes so that no chosen zeroes are on the same column or same row