class User:
    def __init__(self, id, firstname, lastname, student_number, email, password, isteacher):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.student_number = student_number
        self.email = email
        # For dummy users this will not be displayed as hash, after login through helsinki servers this must be deleted 
        self.password = password
        self.isteacher = isteacher
