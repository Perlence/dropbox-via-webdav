from setuptools import setup

setup(
    name='dropbox-via-webdav',
    description='Access your Dropbox via WebDAV interface.',
    version='0.1',
    author='Sviatoslav Abakumov',
    author_email='dust.harvesting@gmail.com',
    url='https://github.com/Perlence/dropbox-via-webdav/',
    platforms=['Windows', 'POSIX', 'Unix', 'MacOS X'],
    license='BSD',
    py_modules=['dropbox_dav_provider'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'arrow',
        'dropbox',
        'WsgiDAV',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
    ],
)
