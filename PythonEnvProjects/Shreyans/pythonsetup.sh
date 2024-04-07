/bin/bash

# NgMNO9VAglGP3TYlTXUq
# Python update and upgrade 
sudo apt-get -y update  && sudo apt-get -y upgrade 

# Python Installation on the env
sudo apt-get install -y python3

# pip installation 
sudo apt-get install -y python3-pip

# Additional Tools
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# python virtual environment
sudo apt install -y python3.10-venv

# Create a virtual environment
sudo python3 -m venv venv

# Activate the virtual environment.
source venv/bin/activate

# Install the packages you need.
# pip3 install <package-name>

# Deactivate the virtual environment.
# deactivate

# You can use the -i option with the pip3 install command to install packages into a specific virtual environment. For example:
# pip3 install -i venv <package-name>

# Install Jupyter Notebook
# sudo pip3 install jupyter
# jupyter notebook


# # JupyterLab
# pip install jupyterlab
# jupyter lab

# # Jupyter Notebook
# pip install notebook
# jupyter notebook

# # Voila
# pip install voila
# voila
# brew install jupyterlab
