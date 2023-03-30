import subprocess
import re
import os

DEBUG_MODE = os.environ.get('DEBUG_MODE', False)

"""Run the command and return the output as a string."""
def run_command_and_get_output(command):
    # check if command is empty
    command_output = {}
    if not command:
        command_output["out_value"] = "No command to run"
        command_output["error"] = True
    _command = command.split()

    # execute the command 
    try:
        command_out_value_bytes = subprocess.run(_command, stdout=subprocess.PIPE, encoding='utf-8')

        DEBUG_MODE and print("command_out_value_bytes", command_out_value_bytes)

        command_out_value_string_cleaned = str(command_out_value_bytes.stdout)[:-1].strip()
        command_output["out_value"] = command_out_value_string_cleaned
        command_output["error"] = False
    except subprocess.CalledProcessError as e:
        print(e.output)
        command_output["out_value"] = "Error in running command %s - output value %s" % command % e.output
        command_output["error"] = True


    return command_output

def remove_characters_from_string(string):
    return re.sub('[^0-9.]', '', string)

def suppress_parsing_exception(func):
    def function_wrapper(x):
        try:
            return func(x)
        except Exception as e:
            return float("nan")
    return function_wrapper

@suppress_parsing_exception
def parseToFloat(value):
    _value = value.strip()
    _value = remove_characters_from_string(_value)
    return float(_value)

def getConversionToMBCoefficient(string):
    if "K" in string:
        return 0.001
    elif "M" in string:
        return 1
    elif "G" in string:
        return 1000
    else:
        return 1

