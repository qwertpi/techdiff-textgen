echo 'Updating your packages'
sudo apt-get update && sudo apt-get upgrade -y
echo 'Installing Python, the Python Package Installer and software to download code from GitHub'
sudo apt-get install python3 python3-pip git -y
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
echo 'Downloading code from Github'
git clone https://github.com/qwertpi/techdiff-textgen.git
cd techdiff-textgen
echo 'Installing the requried python libaries'
pip3 install --user -U -r requirements.txt
sudo apt-get install libhdf5-serial-dev
echo 'Installing tools required for data download'
sudo apt-get install dos2unix ffmpeg`
echo 'Downloading training data'
bash data_download.bash
echo 'Done!'
