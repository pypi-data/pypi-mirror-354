from setuptools import setup

setup(
    name='lektor-conference-template-functions',
    description='Minor functions added to templates for jinja2.',
    author='Nelson Brown',
    author_email='nelson.brown@faa.gov',
    url='https://atrdsymposium.org/',
    version='0.1.6',
    license='public domain',
    py_modules=['conference_template_functions'],
    entry_points={
        'lektor.plugins': [
            'conference-template-functions = conference_template_functions:ConferenceTemplatePlugin',
        ]
    }
)
