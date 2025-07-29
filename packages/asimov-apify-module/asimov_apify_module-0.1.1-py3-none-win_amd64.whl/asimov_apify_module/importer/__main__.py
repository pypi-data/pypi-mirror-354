import os, sys

argv = [os.path.join(os.path.dirname(__file__), "asimov-apify-importer.exe"), *sys.argv[1:]]
if os.name == 'posix':
    os.execv(argv[0], argv)
else:
    import subprocess; sys.exit(subprocess.call(argv))
