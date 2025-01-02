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

# inheritance stuff starts here

class Beagle(Dog):
    """a class that represents specific breed """
    def __init__(self, my_name, my_gender, my_age, is_gun_shy):
        # calls super (parent) class initialization

        super().__init__(my_name, my_gender, my_age)
        self.is_gun_shy = is_gun_shy

    def canIshoot(self):
        if self.is_gun_shy:
            print("no, dont shoot")
        else:
            print("go ahead, shoot")

    # a parent class method can be overriden:
    def bark (self, is_loud):
        if is_loud:
            print('HOWL HOWL HOOOOWWWWWLLL')
        else:
            print('howl')

dog1 = Beagle('doggie', 'male', 10, True)
dog2 = Dog('Rex', 'male', 3)
dog1.bark(True)
dog1.bark(False)
dog2.bark(True)
dog2.bark(False)
