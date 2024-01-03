from pydolphinscheduler.core.parameter import ParameterHelper, ParameterType
from http.py import Http  # Replace 'your_module_path' with the actual path or import structure

def test_http_params_conversion():
    # Create a sample http_params dictionary
    http_params_dict = {
        "prop1": "value1",
        "prop2": "value2",
        "prop3": "value3"
    }

    # Create an instance of the Http class with http_params as a dictionary
    http_instance = Http(
        name="test_http",
        url="http://www.example.com",
        http_method="GET",
        http_params=http_params_dict
    )

    # Print the initialized http_params attribute (should be converted to the desired format)
    print("Converted http_params:", http_instance.http_params)

    # Add any assertions or additional tests as required based on your project's logic
    assert isinstance(http_instance.http_params, list)
    assert len(http_instance.http_params) == len(http_params_dict)

    # Add more assertions if necessary to validate the content or structure of the converted parameters
    # For instance, check if certain properties exist or match expected values in the converted list format
    # assert some_condition, "Assertion failed: Custom message if condition is not met"

if __name__ == "__main__":
    test_http_params_conversion()
