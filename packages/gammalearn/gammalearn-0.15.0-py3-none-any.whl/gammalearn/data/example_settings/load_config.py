# Disable ruff linting for this file
# need to be fixed later
# ruff: noqa

import yaml

def load_config(config_file: str):
    """
    Load the configuration from the specified YAML file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: A dictionary containing the loaded configuration.
    """
    with open(config_file, 'r') as file:
        config_data = yaml.safe_load(file)

    # Load the callbacks
    callback_list = config_data.get('test_callbacks', [])
    config_data['test_callbacks'] = [getattr(callbacks, cb)() for cb in callback_list if hasattr(callbacks, cb)]

    # Load the event filters dynamically if they exist
    event_filters = config_data.get('event_filter', {})
    for filter_name, params in event_filters.items():
        if filter_name in globals():  # Assuming the filter functions are globally accessible
            event_filters[filter_name] = globals()[filter_name](**params)  # Initialize with params
        else:
            print(f"Warning: Filter {filter_name} not found in globals.")

    # Handle data module configuration
    data_module = config_data.get('data_module_test', {})
    module_name = data_module.get('module')
    if module_name:
        data_module['module'] = globals()[module_name]  # Dynamically load the module class

    return config_data

# Example usage:
config = load_config('experiments_settings_train_MC.yaml')
