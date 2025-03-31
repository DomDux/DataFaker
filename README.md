# Data Faker
When building a proof of concept for a data project, or testing out a product, it is often necessary to use notional data as opposed to real-world data due to concerns with data protection or availability. Often, this involves a developer spending time manually creating fake datasets where ther are none available, and then needing to manually update them whenever changes are made to the proposed data model.


Issues with this approach include:
 - **Time**: This is a huge time sink for developers which could be better spent
 - **Volume**: A developer can quickly mock up a dataset of 10-20 rows, but very soon the data becomes too much to manage and the volumes are impractical for our purposes
 - **Patterns**: We may wish to create data with real patterns to be revealed in analysis. This is possible for a developer to manually set, but it is very difficult to track or keep consistent
 - **Complexity**: Maintaining control of 1 dataset is simple, but updating a full data model while maintaining referential integrity is complex and very hard to manage

Alternatively, the user could use a number of tricks tand tools to generate more data (e.g. by randomly populating numbers in the dataset). However, this has downsides too:
 - **Patterns**: If data is randomly generated for each column independently, there are no relationships between columns to give interesting/useful results in analysis. The data could also make no sense (e.g. birth dates after death dates etc.)
 - **Referential Integrity**: There is little to no control over the values of primary and foreign keys, meaning the relationships between tables can not be managed
 - **Non-numeric Rules**: Setting rules for non-numeric data to be generated randomly is complicated and often produces strange results. For example, we generate strings of gibberish text.

The goal of this project is to simplify this process for non-technical users so that anyone can quickly create fake datasets for their project which follows a few sets consistent rules.


## Solution
The user requires an interface to specify the structure of their data. This will be in the form of a ~metadata table~ determining teh schema of the generated table(s) with any rules which should be followed. The user can then specify the relationships between tables, and the number of rows the wish to generate for each, then hit a button to create the required datasets which can then be downloaded as CSV of EXCEL files.

### 1. Data Generation
We will use the `python [Faker](https://faker.readthedocs.io/en/master/) package as the basis for this data generation. This has a suite of existing rules for generating fake data points such as:
| Rule | Code | Example |
| --- | --- | --- |
| Name | `fake.name()` | `Elizabeth Winfrey` |
| Bothify (random strings of numbers and provided letters) | `fake.bothify(text="##???, letters="ABDC")` | `18BAD` |
| Language Code | `fake.language_code()` | `en` |
| Random Choices | `fake.random_choices(elements=('a', 'b', 'c', 'd'))` | `['a', 'b', 'a', 'c']` |
| Random Element | `fake.random_element(elements=('a', 'b', 'c', 'd'))` | `b` |
| Address | `fake.address()` | `3513 John Divide Suite 155\nRodriguezside, LA 93111` |
| Company | `fake.company()` | `Change-Fisher` |
| Date (between 1970-01-01 and end_datetime) | `fake.date(pattern="%Y-%m-%d", end_datetime='2024-01-01')` | `1998-05-27` |
| Long-Lat | `locat_lating(country_code: str = 'US', coords_only: bool = False)` | `('40,56754', '-89.64066', 'Perkin', 'US', 'America/Chicago')` |
| IP Address | `fake.ipv4()` | `171.174.170.81` |
| Sentences | `fake.sentence()` | `American whole magazine truth stop whose.` |
| Phone | `fake.phone_number()` | `(460)648-7647x5938` |

_\*Detailed construction of `fake.random_choices()`:_ 
```
fake.random_choices(elements=OrderedDict([
    ("variable_1, 0.5),     # Generates "variable_1" 50% of the time
    ("variable_2, 0.5),     # Generates "variable_2" 50% of the time
    ("variable_3, 0.2),     # Generates "variable_3" 20% of the time
    ("variable_4, 0.1),     # Generates "variable_4" 10% of the time
  ]), unique=False
)
```

There is also the `profile()` function which generates a dictionary with a fake user profile for a person with all of the above mentioned providers grouped together.

The other addtional packages for `Faker` may also be useful:
 - `faker-datasets`: User a sample dataset to generate samples of the dataset from random rows. Not useful for faking data from scratch, but good for sampling.
 - `faker_pyspark`: Generates a pyspark dataframe. Can pass a schema to it to ensure that the schema is fullfilled.

We want to write a function which accepts a (modified) schema for a dataset and uses the approriate faker rules to generate a row of data. We also want to write a function which calls this function repeatedly to generate a list of rows which make up the base of this dataset.

### 2. User Interface
The user will need to specify the schema of the data they wish to generate. This will reequire them entering data into a table like so:
| Field Name | Data Type | Generate from Rule | Nullable | Length | Attribute Domain |
| --- | --- | --- | --- | --- | --- |
| User Name | string | Name | - | - | - |
| Date of Birth | date | Date | - | - | - |
| UserID | string | - | FALSE | 12 | - |
| Team | string | - | TRUE | - | ["HR", "Finance", "Sales"] |

This will then inform us what information to pass to our faker functions.
