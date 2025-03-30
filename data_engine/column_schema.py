import random
from typing import Optional, Union
from faker import Faker
import numpy as np

from datatypes import Datatype
from datatypes import (
    StringType, 
    IntegerType,
    FloatType, 
    # DateType,
    BooleanType,
    # EmailType,
    # PhoneNumberType,
    # URLType,
    # AddressType,
    # NameType, 
)

class ColumnSchema:
    """
    Represents a series of data in a column of a table. Each column is equipped with rules to determine how the data should be generated.

    Attributes:
        name (String): The name of the column (e.g. CustomerID)
        datatype (String): The data type of the column (e.g. int, str, float, etc.)
        completeness (float): The percentage of non-null values in the column. 1 by default (no null values).
        generator_rule (Callable): A Faker function which randomly generates the data for the column. If `None`, then the default generator will be used.
        datatype_kwargs (dict): Additional keyword arguments for the datatype class (e.g. length for StringType, categories for CategoryType).
    """
    def __init__(
        self,
        name: str,
        datatype: Datatype | str = None,
        completeness: float = 1.0,
        generator_rule: Optional[callable] = None,
        **datatype_kwargs: Optional[dict]
    ) -> None:
        self.name = name

        if datatype is None:
            # If no datatype is provided, we use StringType as the default.
            datatype = StringType()
        elif isinstance(datatype, str):
            # If a string is provided, we convert it to the corresponding Datatype class.
            datatype = Datatype.get_class(datatype)(**datatype_kwargs)
        elif not isinstance(datatype, Datatype):
            raise TypeError(f"Invalid datatype: {datatype}. Expected a Datatype object or a string.")
        
        self.datatype = datatype
        self.completeness = completeness
        self.generator_rule = generator_rule
        
    def __str__(self) -> str:
        return f"ColumnSchema(name={self.name}, datatype={self.datatype}, length={self.length}, completeness={self.completeness}, attribute_domain={self.attribute_domain})"
    
    def __repr__(self) -> str:
        return self.__str__()

    def generate(self, *args):
        """
        Generates a value for the column based on the specified rules.
        """
        # When completeness is not 100%, we set the output to None with a probability of (1 - completeness).
        provide_null_value = random.random() > self.completeness
        if provide_null_value and self.completeness < 1.0:
            return None
                
        # If we have a generator rule, we use it to generate the value.
        if self.generator_rule is not None:
            return self.generator_rule()
        
        # If we don't have a generator rule, we use the default generator based on the datatype.
        return self.datatype.generator_rule()
    
