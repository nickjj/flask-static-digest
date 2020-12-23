from setuptools import setup


setup(
    name="Flask-Static-Digest",
    version="0.2.1",
    author="Nick Janetakis",
    author_email="nick.janetakis@gmail.com",
    url="https://github.com/nickjj/flask-static-digest",
    description="Flask extension for md5 tagging and gzipping static files.",
    license="MIT",
    package_data={"Flask-Static-Digest": ["VERSION"]},
    packages=["flask_static_digest"],
    platforms="any",
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=[
        "Flask>=1.0"
    ],
    entry_points={
        "flask.commands": [
            "digest=flask_static_digest.cli:digest"
        ],
    },
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Compression"
    ]
)
