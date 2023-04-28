import utils

cores_frequency = utils.run_command_and_grep_output("cat /proc/cpuinfo", "^[c]pu MHz")
print("cores_frequency", cores_frequency)

# import subprocess

# proc1 = subprocess.Popen(['pss', 'cax'], stdout=subprocess.PIPE)
# proc2 = subprocess.Popen(['grep', 'python'], stdin=proc1.stdout,
#                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
# out, err = proc2.communicate()
# print('out: {0}'.format(out))
# print('err: {0}'.format(err))