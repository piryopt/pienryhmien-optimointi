class Weights:
    '''
    Class for creating and managing weights in the hungarian algorithm
    '''
    def __init__(self, n_choices:int, n_students:int, min_in_choices:bool):
        """
        Calls function calculate_weights to create self.weights list of
        int numbers that act as profit weights in hungarian algorithm.
        The weights are relative to the number of students and number of
        choices. More info in documentation/hungarian.md
        TODO: minimum weight isn't 0, that way 0 can be given to students
        when they must not be put to a certain group. Requires changes to
        Hungarian function reshape_matrix and tests

        Args:
            n_choices (int): number of choices a student makes
            n_students (int): number of students to sort in the groups
            min_in_choices (bool): Tells the function wether the minimum
            weight should be included in the number of choices or if in
            addition to the number of choices there should be a separate
            minimum weight cathegory for options not chosen by student
        """
        if min_in_choices:
            self.weights = self.calculate_weights(n_choices, n_students)
        else:
            self.weights = self.calculate_weights(n_choices+1, n_students)

    def calculate_weights(self, n_choices, n_students):
        """calculate_weights
        Calculates the interval for weights in the hungarian algorithm based
        on the number of choices and students by using the number of students
        as the minimum weight a student can give to a group either by choosing
        it last or not giving it a ranking. The interval between weights is
        the number of students and nuber of weights is the number of choices
        a student makes.

        Args:
            n_choices (int): number of choices a student makes and additional
            minimum if needed
            n_students (int): number of students to sort in the groups

        Returns:
            weights_dict (dict): dictionary of weights with keys 0-n_choices
            paired with weights in order where highest weight is paired with
            lowest key
        """

        weights = []
        for i in range(n_choices):
            weights.append(n_students+n_students*i)
        weights = sorted(weights, reverse=True)
        weights_dict = {}
        for i in range(n_choices):
            weights_dict[i] = weights[i]
        weights_dict[None] = n_students
        return weights_dict

    def get_weights(self):
        return self.weights
