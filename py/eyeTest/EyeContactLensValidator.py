
class ContactLensValidator:
    """
    A class to handle conversion and validation of contact lens prescriptions.
    It can convert eyeglass prescriptions to contact lens prescriptions and vice versa.
    """
    def __init__(self):
        pass

    def convert_to_spheric(self, data: dict) -> dict:
        """
        Convert an eyeglass prescription to a spherical equivalent.

        Parameters:
            data (dict): A dictionary containing SPH, CYL, AX, and ADD values.

        Returns:
            dict: A dictionary with the converted spherical prescription.
        """
        # Get values from dictionary and handle possible empty values
        sphere = data.get('SPH', '0').strip()  # Strip to remove leading/trailing spaces
        cylinder = data.get('CY', '0').strip()
        axis = data.get('AX', '0').strip()
        vertex_distance = data.get('BV', '12').strip()
        add = data.get('ADD', '0').strip()

        # Ensure values are valid float strings (empty values are converted to 0)
        sphere = float(sphere) if sphere else 0
        cylinder = float(cylinder) if cylinder else 0
        axis = float(axis) if axis else 0
        vertex_distance = float(vertex_distance) if vertex_distance else 12
        add = float(add) if add else 0

        # Calculate the spherical equivalent if cylinder is not zero
        if abs(cylinder) != 0:
            total_sphere = self.spherical_equivalent(sphere, cylinder)
        else:
            total_sphere = sphere

        # Adjust sphere for contact lens if it's greater than ±4.00
        if abs(total_sphere) > 4:
            sphere_contact_lens = self.spheric_without_vertex_distance(total_sphere, vertex_distance)
        else:
            sphere_contact_lens = total_sphere

        # Round to nearest 0.25
        nearest_value = self.round_to_nearest_quarter(sphere_contact_lens)

        # Prepare result dictionary
        value = {"SPH": nearest_value, "ADD": add}
        value = self.format_result_to_quarter(value)

        value['Exact SPH'] = f"{sphere_contact_lens:+06.2f}"  # Format the SPH value
        value['AX'] = ""  # The AX value is not required for spherical lenses
        value["BV"] = vertex_distance
        return value

    def convert_to_toric(self, data: dict) -> dict:
    
        """
        Convert an eyeglass prescription to a toric contact lens prescription.

        Parameters:
            data (dict): A dictionary containing SPH, CYL, AX, and ADD values.

        Returns:
            dict: A dictionary with the converted toric contact lens prescription.
        """
        # Get values from dictionary and handle possible empty values
        sphere = data.get('SPH', '0').strip()  # Strip to remove leading/trailing spaces
        cylinder = data.get('CY', '0').strip()
        axis = data.get('AX', '0').strip()
        vertex_distance = data.get('BV', '12').strip()
        add = data.get('ADD', '0').strip()

        # Ensure values are valid float strings (empty values are converted to 0)
        sphere = float(sphere) if sphere else 0
        cylinder = float(cylinder) if cylinder else 0
        axis = float(axis) if axis else 0
        vertex_distance = float(vertex_distance) if vertex_distance else 12
        add = float(add) if add else 0



        # Calculate spherical power without vertex distance
        spher_power = self.spheric_without_vertex_distance(sphere, vertex_distance)
        cylinder_power = self.spheric_without_vertex_distance(sphere + cylinder, vertex_distance) - spher_power
        nerst_cylinder_power = self.round_to_nearest_quarter(cylinder_power)
        # Round to nearest 0.25
        nearest_spher_value = self.round_to_nearest_quarter(spher_power)

        # Prepare result dictionary
        value = {"SPH": nearest_spher_value, "CY": nerst_cylinder_power, "ADD": add}
        value = self.format_result_to_quarter(value)
        value['Exact SPH'] = f"{spher_power:+06.2f}"  # Format the SPH value
        value['Exact CY'] = f"{cylinder_power:+06.2f}"  # Format the CY value
        value['AX'] = f"{axis:.0f}"  # Format the AX value
        value["BV"] = vertex_distance
        return value
    
    def format_result_to_quarter(self, value: dict) -> dict:
        """
        Format the results in the dictionary to have the correct format.

        Parameters:
            value (dict): A dictionary containing SPH, CYL, and AX values.

        Returns:
            dict: The formatted values.
        """
        for key in value:
            value[key] = self.format_number_custom(value[key])

        return value

    def spheric_without_vertex_distance(self, sphere, vertex_distance):
        """
        Calculate the spherical power without vertex distance adjustment.

        Parameters:
            sphere (float): The sphere value of the prescription.
            vertex_distance (float): The vertex distance (usually 12mm).

        Returns:
            float: The spherical power adjusted for vertex distance.
        """
        return sphere / (1 - (vertex_distance / 1000) * sphere)

    def spherical_equivalent(self, sphere, cylinder):
        """
        Calculate the spherical equivalent for a given sphere and cylinder.

        Parameters:
            sphere (float): The sphere value of the prescription.
            cylinder (float): The cylinder value of the prescription.

        Returns:
            float: The spherical equivalent.
        """
        return round(sphere + (cylinder / 2), 2)

    def round_to_nearest_quarter(self, num):
        """
        Round a number to the nearest 0.25.

        Parameters:
            num (float): The number to round.

        Returns:
            float: The rounded number.
        """
        return round(num * 4) / 4

    def format_number_custom(self, value):
        """
        Format the number to be a multiple of 0.25 with a sign.

        Parameters:
            value (str): The number to format.

        Returns:
            str: The formatted number, or False if it's not a multiple of 0.25.
        """
        if self.is_multiple_of_quarter(value):
            try:
                value = float(value)
                return f"{value:+06.2f}"
            except ValueError:
                print(f"Error: '{value}' could not be converted to a float.")
                return False
        else:
            return False

    def is_multiple_of_quarter(self, value):
        """
        Check if a given value is divisible by 0.25.

        Parameters:
            value (str): The input value to check.

        Returns:
            bool: True if the value is divisible by 0.25, otherwise False.
        """
        try:
            value = float(value)
            return value % 0.25 == 0
        except ValueError:
            print(f"Error: '{value}' is not a valid number.")
            return False
