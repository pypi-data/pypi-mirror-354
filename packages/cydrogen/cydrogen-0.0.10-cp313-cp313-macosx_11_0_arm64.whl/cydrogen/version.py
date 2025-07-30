"""
Module to expose more detailed version info for the installed `cydrogen`
"""
version = "0.0.10"
full_version = version
short_version = version.split('-dev')[0]
git_revision = "91b38942daf88b0e09c3077666831e3f767bacb0"
release = '-dev' not in version and '+' not in version

if not release:
    version = full_version