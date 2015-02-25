# fake setup 
PASS = ["foo.exe", "bar.exe", "really_long_filename.exe"]
FAILED = ["failed.exe"]
types = ["32-bit", "64-bit", "64-bit"]
arch64 = '64'
arch32 = '32'

# your code
def print_row(filename, status, file_type):
   

print_row('FileName', 'Status', 'Binary Type')

# for files in PASS:
#     log = types.pop()
#     if arch64 in log:
#         print_row(files, 'PASSED', '64-bit')
#     elif arch32 in log:
#         print_row(files, 'PASSED', '32-bit')
# print"\n"   

# for files in FAILED:
#         print_row(files, 'FAILED', '')

print "\n\n"