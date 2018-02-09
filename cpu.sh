#! /bin/bash

DEBIAN_FRONTEND=noninteractive

sudo rm /etc/apt/apt.conf.d/*.*
sudo apt update
mkdir downloads
cd downloads
wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
bash Anaconda3-5.0.1-Linux-x86_64.sh -b
echo 'export PATH=~/anaconda3/bin:$PATH' >> ~/.bashrc
export PATH=~/anaconda3/bin:$PATH
source ~/.bashrc
conda env update
jupyter notebook --generate-config
echo "c.NotebookApp.ip = '*'" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py
sudo ufw allow 8888/tcp
sudo apt -y install qtdeclarative5-dev qml-module-qtquick-controls
sudo apt update
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension --sys-prefix
conda install -c anaconda scikit-learn
conda install -c conda-forge xgboost
conda install -c glemaitre imbalanced-learn
sudo reboot