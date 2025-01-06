# Eye Test Validation and Contact Lens Power Calculation

This repository contains a set of utility functions and classes for handling eye test validations and contact lens power calculations. These functions are designed to ensure that user inputs for eye test data are valid and formatted correctly.

## Table of Contents

- [Classes](#classes)
  - [eye_test_validit](#eye_test_validit)
  - [convert_to_contact_lens_validit](#convert_to_contact_lens_validit)
- [Functions](#functions)
  - [check_SG](#check_SG)
  - [check_axis](#check_axis)
  - [check_pd](#check_pd)
  - [check_add](#check_add)
  - [remove_sign](#remove_sign)
  - [remove_sign_axs](#remove_sign_axs)
  - [power_format](#power_format)

## Classes

### eye_test_validit

The `eye_test_validit` class contains various methods to validate and format data related to an eye test prescription. This class helps ensure that the values entered by the user are correct according to the predefined rules for SPH, CYL, AX, and other parameters.

#### Methods:



1. **`check_SG(value)`**:
   - **Description**: Checks if the value of SG (Spherical Power or other related parameter) is between 7 and 50 and is a positive float.
   - **Parameters**:
     - `value` (str or float): The value to check.
   - **Returns**: 
     - `True` if the value is valid (between 7 and 50, positive).
     - `False` otherwise.
   
2. **`check_axis(value)`**:
   - **Description**: Checks if the AX (Axis) value is between 1 and 180 degrees and is positive.
   - **Parameters**:
     - `value` (str or float): The value to check.
   - **Returns**:
     - `True` if the value is valid.
     - `False` otherwise.

3. **`check_pd(value)`**:
   - **Description**: Checks if the PD (Pupil Distance) value is between 19 and 85 and is positive.
   - **Parameters**:
     - `value` (str or float): The value to check.
   - **Returns**:
     - `True` if the value is valid.
     - `False` otherwise.

4. **`check_add(value)`**:
   - **Description**: Checks if the ADD (Addition) value is between 0.25 and 4 and is positive.
   - **Parameters**:
     - `value` (str or float): The value to check.
   - **Returns**:
     - `True` if the value is valid.
     - `False` otherwise.

5. **`remove_sign(value)`**:
   - **Description**: Removes the sign of a number (positive or negative) and returns the absolute value formatted as a string with two decimal places.
   - **Parameters**:
     - `value` (str or float): The value to process.
   - **Returns**:
     - The absolute value of `value` as a string with two decimal places.

6. **`remove_sign_axs(value)`**:
   - **Description**: Removes the sign and returns the absolute value of AX as a string, rounded to the nearest integer.
   - **Parameters**:
     - `value` (str or float): The value to process.
   - **Returns**:
     - The absolute value of AX as a string, rounded to the nearest integer.

7. **`power_format(data)`**:
   - **Description**: Takes a dictionary with SPH, CYL, and AX values, and formats them according to the rules. Adjusts SPH and CYL if necessary.
   - **Parameters**:
     - `data` (dict): The dictionary containing the SPH, CYL, and AX values.
   - **Returns**:
     - A dictionary with the formatted SPH, CYL, and AX values.

### convert_to_contact_lens_validit

The `convert_to_contact_lens_validit` class contains methods for converting and formatting eye test values into contact lens prescriptions. It handles calculations to convert spherical powers into spherical equivalents for contact lenses.

#### Methods:

1. **`convert__contact_lens_to_spheric(data)`**:
   - **Description**: Converts the provided eye test data into a contact lens prescription for spherical lenses.
   - **Parameters**:
     - `data` (dict): A dictionary containing SPH, CYL, AX, and other relevant data.
   - **Returns**:
     - A dictionary with the converted SPH, ADD values, and formatted results.

2. **`convert__contact_lens_to_toric(data)`**:
   - **Description**: Converts the provided eye test data into a contact lens prescription for toric lenses (with CYL and AX).
   - **Parameters**:
     - `data` (dict): A dictionary containing SPH, CYL, AX, and other relevant data.
   - **Returns**:
     - A dictionary with the converted SPH, CYL, AX, and ADD values.

3. **`spheric_withOut_vertex_distance(sphere, vertex_distance)`**:
   - **Description**: Adjusts the spherical power based on the vertex distance.
   - **Parameters**:
     - `sphere` (float): The spherical power.
     - `vertex_distance` (float): The vertex distance (usually 12mm).
   - **Returns**:
     - The adjusted spherical power.

4. **`spherical_equivalent(sphere, cylinder)`**:
   - **Description**: Calculates the spherical equivalent of a prescription by adding half the cylinder to the sphere.
   - **Parameters**:
     - `sphere` (float): The spherical power.
     - `cylinder` (float): The cylindrical power.
   - **Returns**:
     - The spherical equivalent as a float.

5. **`round_to_nearest_quarter(num)`**:
   - **Description**: Rounds a number to the nearest quarter.
   - **Parameters**:
     - `num` (float): The number to round.
   - **Returns**:
     - The rounded number (float).

6. **`format_number_custom(value)`**:
   - **Description**: Formats the value to two decimal places if it's a valid multiple of 0.25.
   - **Parameters**:
     - `value` (str or float): The value to format.
   - **Returns**:
     - A string representing the formatted value or `False` if not a valid multiple of 0.25.

## How to Use

1. **Creating an Object of `eye_test_validit`**:

   ```python
   eye_test = eye_test_validit()

   # Validate SG
   print(eye_test.check_SG("10"))  # True
   print(eye_test.check_SG("60"))  # False



contact_lens = convert_to_contact_lens_validit()

# Convert SPH and CYL to contact lens prescription
data = {'SPH': '-2.00', 'CY': '-1.50', 'AX': '90', 'ADD': '2.50'}
result = contact_lens.convert__contact_lens_to_toric(data)
print(result)  # Output: {'SPH': '+2.00', 'CY': '0.50', 'AX': '0', 'ADD': '2.50'}



