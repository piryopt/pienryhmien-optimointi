class Weights:
    '''
    Class for creating and managing weights in the hungarian algorithm
    '''
    def __init__(self, n_choices:int, n_students:int):
        """
        Calls function calculate_weights to create self.weights list of
        int numbers that act as profit weights in hungarian algorithm.
        The weights are relative to the number of students

        Args:
            n_choices (int): number of choices levels in the questionnaire,
            e.g. levels when ranking  
            n_students (int): number of students to sort in the groups
        
        Variables:
            self.weights (dict): dictionary of weights with keys from 0 to n_choices
            paired with weights in order where highest weight is paired with
            lowest key. One extra weight with key -1 outside of choices added as a weight
            that is !=0 to be given to options not chosen by student
        """
        self.weights = self.calculate_weights(n_choices, n_students)

    def calculate_weights(self, n_choices, n_students):
        """
        Takes number of choices and number of students, returns dictionary of weights
        where interval of weights is the number of students, there's one weight for every
        choice index plus one extra weight with key -1 that can be given to options outside
        of student choices and that is >0 but lower than the lowest weight. This same value
        is used for key Null.

        Args:
            n_choices (int): number of choices a student makes and additional
            minimum if needed
            n_students (int): number of students to sort in the groups

        Returns:
            weights (dict): dictionary of weights with keys 0-(n_choices-1)
            paired with weights in order where highest weight is paired with
            lowest key
        """
        weights = list(range((n_choices+2)*n_students, n_students*2, -n_students))
        weights = dict(zip(list(range(len(weights))), weights))
        weights[-1] = n_students*2
        weights[None] = n_students*2
        return weights

    def get_weights(self):
        return self.weights
