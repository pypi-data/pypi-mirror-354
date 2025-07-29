
"""
Module to expose more detailed version info for the installed `scipy`
"""
version = "1.16.0rc2"
full_version = version
short_version = version.split('.dev')[0]
git_revision = "e0b3e3ff7842025c64b134de740680b8ba9951b9"
release = 'dev' not in version and '+' not in version

if not release:
    version = full_version
