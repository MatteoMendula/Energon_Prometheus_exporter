import subprocess
import re

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

        command_out_value_string_cleaned = str(command_out_value_bytes.stdout)[:-1].strip()
        command_output["out_value"] = command_out_value_string_cleaned
        command_output["error"] = False
    except Exception as e:
        print("Exception", e.output)
        command_output["out_value"] = "Error in running command %s - output value %s" % command % e.output
        command_output["error"] = True

    return command_output

def run_command_and_grep_output(command1, string_to_grep):
    command_output = {}
    if not command1 or not string_to_grep:
        command_output["out_value"] = "No command to run"
        command_output["error"] = True
    _command1 = command1.split()
    _command2 = ["grep", string_to_grep]

    try:
        proc1 = subprocess.Popen(_command1, stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(_command2, stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
        out, err = proc2.communicate()
        command_output["out_value"] = str(out)[2:-1]
        command_output["error"] = False
    except Exception as e:
        print(e.output)
        command_output["out_value"] = "Error in running commands %s %s - output value %s" % _command1 % _command2 % e.output
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

def parse_micro_joules_string_watts_float(value):
    _value = parseToFloat(value)
    if _value == float("nan"):
        return value
    _value = float(_value)
    return _value / 1000000

def getConversionToMBCoefficient(string):
    if "K" in string:
        return 0.001
    elif "M" in string:
        return 1
    elif "G" in string:
        return 1000
    else:
        return 1

def clean_metric_name_to_prometheus_format(metric_name):
    # clean metric_name to be prometheus compatible
    return re.sub('[^0-9a-zA-Z]+', '_', metric_name)