class Dog():
    """ a class to represent a general dog """
    
    def __init__(self, my_name, my_gender, my_age):
        """ initialize attributes """
        self.name = my_name
        self.gender = my_gender
        self.age = my_age

    def eat(self):
        """ feed the dog """
        if self.gender == "male":
            print(" here " + self.name + " ! Good boy! Eat up.")
        else: 
            print(" here " + self.name + " ! Good girl! Eat up.")

    def bark(self, is_loud):
        """ get the dog speak """
        if is_loud:
            print("WOOF WOOF WOOF")
        else:
            print("woof")
    def compute_age(self):
        """ compute the age in dog years """
        dog_years = self.age*7
        print(self.name + " is " + str(dog_years) + " in dog years")




my_dog = Dog("Spot", "male", 10)
some_other_dog = Dog('Moon', 'female', 1)

my_dog.eat()
some_other_dog.eat()

my_dog.bark(True)
my_dog.bark(False)

my_dog.compute_age()
some_other_dog.compute_age()