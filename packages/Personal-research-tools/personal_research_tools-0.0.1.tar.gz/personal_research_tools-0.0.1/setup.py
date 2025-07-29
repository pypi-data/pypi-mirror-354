import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="Personal_research_tools", 
    version="0.0.1", 
    author="Anthony R. Osborne", 
    author_email="anthony.r.osborne@pm.me", 
    packages=["inversion_tools"], 
    description="A package containing all my research tools not for anyone else", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/Anthony904175/personal_research_tools.git", 
    license='GNU3.0', 
    python_requires='>=3.8', 
    install_requires=[] 
) 
