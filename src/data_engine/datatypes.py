import random
import string
from typing import Type, Optional

class Datatype:
    """
    A base class for all data types which make up a column schema.
    This class is not meant to be instantiated directly, but rather to be subclassed by specific data types.
    """

    def __init__(self):
        """
        Initializes the datatype object. Must be called by subclasses.
        """
        pass

    def generator_rule(self):
        """
        For every column of a given basic type, we have a default generator rule.
        This is a function that generates a random value of the specified type.
        This will need to be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def __str__(self):
        """
        Returns a string representation of the datatype.
        """
        return f"{self.__class__.__name__}"
    
    
    _registry: dict[str, Type["Datatype"]] = {}

    @classmethod
    def register(cls, *names: str):
        """Decorator to register subclasses."""
        def wrapper(subclass: Type["Datatype"]):
            for name in names:
                cls._registry[name] = subclass
            return subclass
        return wrapper

    @classmethod
    def get_class(cls, name: str) -> "Datatype":
        """Returns a subclass based on a string identifier."""
        if name in cls._registry:
            return cls._registry[name]
        raise ValueError(f"Unknown datatype: {name}")
    

@Datatype.register("string")
class StringType(Datatype):
    """
    A class representing a string data type.
    """
    def __init__(self, length: int = 10):
        """
        Initializes the StringType object with a specified length.
        """
        super().__init__()
        if length is None:
            length = 10
        if length <= 0:
            raise ValueError("Length must be a positive integer.")
        self.length = length

    def generator_rule(self):
        """
        Generates a random string of the specified length.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=self.length))
    

@Datatype.register("int", "integer")
class IntegerType(Datatype):
    """
    A class representing an integer data type.
    """
    def __init__(self, min_value: int = 0, max_value: int = 100):
        """
        Initializes the IntegerType object with a specified range.
        """
        super().__init__()
        if min_value is None and max_value is None:
            min_value = 0
            max_value = 100
        elif max_value is None and min_value is not None:
            max_value = max(100+min_value, 100)
        elif min_value is None and max_value is not None:
            min_value = min(max_value-100, 0)
        
        if min_value >= max_value:
            raise ValueError("min_value must be less than max_value.")
        
        self.min_value = int(min_value)
        self.max_value = int(max_value)

    def generator_rule(self):
        """
        Generates a random integer within the specified range.
        """
        return random.randint(self.min_value, self.max_value)
    

@Datatype.register("float")
class FloatType(Datatype):
    """
    A class representing a float data type.
    """
    def __init__(self, min_value: float = 0.0, max_value: float = 100.0):
        """
        Initializes the FloatType object with a specified range.
        """
        super().__init__()
        if min_value is None and max_value is None:
            min_value = 0.0
            max_value = 100.0
        elif max_value is None and min_value is not None:
            max_value = max(100.0+min_value, 100.0)
        elif min_value is None and max_value is not None:
            min_value = min(max_value-100.0, 0.0)
        
        self.min_value = min_value
        self.max_value = max_value

    def generator_rule(self):
        """
        Generates a random float within the specified range.
        """
        return round(random.uniform(self.min_value, self.max_value), 2)
    

@Datatype.register("category")
class CategoryType(Datatype):
    """
    A class representing a categorical data type.
    """
    def __init__(self, categories: list = ["A", "B", "C"]):
        """
        Initializes the CategoryType object with a specified list of categories.
        """
        super().__init__()
        if categories is None or len(categories) == 0:
            raise ValueError("Categories cannot be None.")
        self.categories = list(set(categories))

    def generator_rule(self):
        """
        Generates a random category from the specified list of categories.
        """
        return random.choice(self.categories) if self.categories else None
    

@Datatype.register("boolean")
class BooleanType(Datatype):
    """
    A class representing a boolean data type.
    """
    def __init__(self):
        """
        Initializes the BooleanType object.
        """
        super().__init__()

    def generator_rule(self):
        """
        Generates a random boolean value (True or False).
        """
        return random.choice([True, False])