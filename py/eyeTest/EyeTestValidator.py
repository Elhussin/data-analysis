class EyeTestValidator:
    def __init__(self):
        """
        Initializer for EyeTestValidator class.
        This class contains various validation methods related to eyeglass prescriptions.
        """
        super().__init__()

    def is_multiple_of_quarter(self, value):
        """
        Check if a given value is a multiple of 0.25.

        Parameters:
            value (str): The input value to check.

        Returns:
            bool: True if the value is divisible by 0.25, otherwise False.
        """
        try:
            # Convert value to float and check if it's divisible by 0.25
            value = float(value)
            return value % 0.25 == 0
        except ValueError:
            # If value cannot be converted to float, return False
            print(f"Error: '{value}' is not a valid number.")
            return False

    def is_valida_eye_test_power(self, value):
        """
        Format a number to show it in the correct way if it's a multiple of 0.25.

        Parameters:
            value (str): The number to format.

        Returns:
            str: The formatted number as a string with + or - sign and 2 decimal places,
                 or False if the number is not a valid multiple of 0.25.
        """
        if self.is_multiple_of_quarter(value):
            try:
                # Format value with the sign and 2 decimal places
                value = float(value)
                return f"{value:+06.2f}"
            except ValueError:
                # Handle the error if value is not convertible to float
                print(f"Error: '{value}' could not be converted to a float.")
                return False
        else:
            return False

    def check_axis(self, value):
        """
        Validate if the axis value is between 1 and 180 (inclusive).

        Parameters:
            value (str): The axis value to check.

        Returns:
            bool: True if the axis value is valid, False otherwise.
        """
        try:
            value = float(value)
            # Axis value must be between 1 and 180
            if 1 <= value <= 180 and value > 0:
                return True
            else:
                return False
        except ValueError:
            # If the value cannot be converted to float, return False
            print(f"Error: '{value}' is not a valid axis value.")
            return False

    def check_pd(self, value):
        """
        Validate if the PD (Pupillary Distance) value is between 19 and 85 (inclusive).

        Parameters:
            value (str): The PD value to check.

        Returns:
            bool: True if the PD value is valid, False otherwise.
        """
        try:
            value = float(value)
            # PD value must be between 19 and 85
            if 19 <= value <= 85:
                return True
            else:
                return False
        except ValueError:
            # If the value cannot be converted to float, return False
            print(f"Error: '{value}' is not a valid PD value.")
            return False

    def remove_sign(self, value):
        """
        Remove the sign from a number and return it as a string with 2 decimal places.

        Parameters:
            value (str): The value to remove the sign from.

        Returns:
            str: The absolute value as a string with 2 decimal places.
            None: If the value cannot be converted to a float.
        """
        try:
            # Take the absolute value and format it
            value = abs(float(value))
            return f"{value:.2f}"
        except ValueError:
            # If value cannot be converted to float, return None
            print(f"Error: '{value}' could not be converted to a number.")
            return None

    def check_add(self, value):
        """
        Validate if the ADD (Addition) value is within the valid range (0.25 to 4) and is positive.

        Parameters:
            value (str): The ADD value to validate.

        Returns:
            bool: True if the ADD value is between 0.25 and 4 and is positive, False otherwise.
        """
        try:
            # Try converting the value to a float
            value = float(value)
            
            # Check if the value is within the range 0.25 <= value <= 4 and is positive
            if 0.25 <= value <= 4 and value > 0:
                return True
            else:
                return False
        except ValueError:
            # Return False if the value cannot be converted to a number
            return False

    def remove_sign_axs(self, value):
        """
        Remove the sign of the axis value and return it as a rounded integer.

        Parameters:
            value (str or float): The axis value to remove the sign from.

        Returns:
            str: The axis value as a positive integer string.
        """
        value = f"{abs(float(value)):.0f}"  # Get the absolute value and convert to integer string
        return str(value)

    def safe_float_convert(self,value: str, default=0) -> float:
        """
        Convert a string to float, return a default value if conversion fails or value is empty.

        Parameters:
            value (str): The string to be converted to float.
            default (float): The value to return if conversion fails or if the value is empty.

        Returns:
            float: The converted float value or the default value if conversion fails.
        """
        try:
            # Try to convert to float
            return float(value) if value.strip() else default
        except ValueError:
            # Return the default value if conversion fails
            return default

    def power_format(self, data: dict) -> dict:
        """
        Format and adjust SPH, CYL, and AX values based on specific rules.

        Parameters:
            data (dict): A dictionary containing the values of SPH, CYL, AX, and ADD.

        Returns:
            dict: A dictionary with updated SPH, CYL, and AX values.
        """
        # Use the safe_float_convert function to handle potential empty or invalid values
        SPH = self.safe_float_convert(data.get('SPH', ''))
        CY = self.safe_float_convert(data.get('CY', ''))
        AX = self.safe_float_convert(data.get('AX', ''))

        # Adjustment for SPH and CY
        if SPH <= 0 and CY <= 0:
            SPH, CY, AX = SPH, CY, AX
        elif SPH > 0 and CY <= 0:
            SPH, CY, AX = SPH, CY, AX
        else:
            SPH = SPH + CY
            CY = CY * -1
            # Adjust AX based on its value
            if AX < 90:
                AX = AX + 90  # Add 90 if AX is less than 90
            elif AX > 90:
                AX = AX - 90  # Subtract 90 if AX is greater than 90

        # Formatting the values
        SPH = self.is_valida_eye_test_power(SPH)
        CY = self.is_valida_eye_test_power(CY)
        AX = f"{AX:.0f}"  # Convert AX to integer string

        return {"SPH":SPH,"CY":CY,"AX":AX}


    def cheek_cyl_ax_not_null(self, data: dict) -> bool:
        """
        Check if either CYL or AX is provided, and ensure the other value is not empty or zero.

        Parameters:
            data (dict): A dictionary containing CYL and AX values.

        Returns:
            bool: True if both values are valid or no update is needed, 
                False if one value is provided but the other is missing or invalid.
        """
        
        # Get the CYL (CY) and AX values from the dictionary
        value1 = self.safe_float_convert(data.get('CY', '')) # CYL value (default to empty string)
        value2 = self.safe_float_convert(data.get('AX', ''))  # AX value (default to empty string)


        # Check the conditions and update the second cell if necessary
        if value1 != 0 and value2 == 0:
            # If Cell 1 has a value and Cell 2 is 0, set Cell 2 to Cell 1's value
            return False
        elif value1 == 0 and value2 != 0:
            # If Cell 1 is 0 and Cell 2 has a value, set Cell 1 to Cell 2's value
            return False
        
        # If both are empty or both have the same value, do nothing
        elif value1 == 0 and value2 == 0:
             return True  # Do nothing if both are empty or 0
        else:
            return True  # Both values are valid or both are empty, no issue


    def check_SG(self, value):
        """
        Validate the SG (Spherical Power or other related parameter) value.
        The value must be a positive float between 7 and 50 (inclusive).
        
        Parameters:
            value (str or float): The value to be checked for validity.
        
        Returns:
            bool: True if the value is a positive float between 7 and 50, False otherwise.
        """
        try:
            value = float(value)  # Try to convert the input value to a float.
            
            # Check if the value is between 7 and 50 (inclusive).
            if 7 <= value <= 50:
                return True
            else:
                return False
        except ValueError:
            return False  # If the conversion to float fails (invalid input), return False.

    def Check_vertex_distance(self, value):
        """
        Validate the BV (Back vertex distance) value.
        The value must be a positive float between 10 and 14 (inclusive).
        
        Parameters:
            value (str or float): The value to be checked for validity.
        
        Returns:
            bool: True if the value is a positive float between 10 and 14, False otherwise.
        """
        try:
            value = float(value)  # Try to convert the input value to a float.
            
            # Check if the value is between 10 and 14 (inclusive).
            if 10 <= value <= 14:
                return True
            else:
                return False
        except ValueError:
            return False  # If the conversion to float fails (invalid input), return False. 