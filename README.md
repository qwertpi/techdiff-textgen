# techdiff-textgen
An LSTM trained on all tech diff vidoes alongside all of Tom Scott's Amazing Places and Things you might not Know  
[Generation Demo](https://colab.research.google.com/drive/1opVwFa0oz7aWEe6iCSLUsL4mPiSUDeT9#forceEdit=true&sandboxMode=true)  
This is a fan project and is in no way affiliated or endorsed by Tom or any of Tech Diff but I will be making him aware of this repo in case he wishes for it to be taken down. Update: He says it can stay up  

Feedback and pull requests are very welcome  
Copyright © 2019  Rory Sharp All rights reserved.  
## Non legaly binding licence summary
You may:
* Modify
* Execute
* Distribute

You may not:
* Use commericaly
* Hold liable

You must:
* Use the same licence for moifications
* Give credit to me the original author in any uses or modifcations

## Prerequisites
### For One Liner
* Curl `apt-get install curl`
### For Manual Install
* [Python 3.6 or later](https://www.python.org/downloads/)
* Keras 2.2.5 or later `pip3 install keras`
* Numpy `pip3 install numpy`
* h5py `pip3 install h5py`
* logzero `pip3 install logzero`
* youtube-dl (data download only) `pip3 install youtube-dl`
* libhdf5 (only needed on some systems) `sudo apt-get install libhdf5-serial-dev`
* dos2unix (data download only) `sudo apt-get install dos2unix`
* ffmpeg (data download only) `sudo apt-get install ffmpeg`
* git-lfs
## One-liner install
`curl https://raw.githubusercontent.com/qwertpi/techdiff-textgen/master/install.bash | bash`
## Usage
0\. Download this repo  
### Training (Optional)
1\. Get the latest data by running the data_download script `bash data_download.bash` (I cannot be held liable for any consequences incurred by the violation of the youtube terms of service comitted by you autonomusly downlaoding subtitles from youtube using this script) or make do with the data provided in this repo (data is up to date as of 2019/10/20)  
2\. Run train.py (ensure to follow the instructions about changing imports if you are on a CPU only system), you may need to tweak the batch size depending on your hardware  
### Generating
3\. Run generate.py  
4\. You can enter any text (but bare in mind the model only knows certain words) and you will get a list of 8 possible next words in decending order of confidence. It can be fun to pick the most intresting of these and then put your sentence back into the model with this new word added.  
