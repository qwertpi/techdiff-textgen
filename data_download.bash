sudo -H pip3 install -U youtube-dl
sudo apt install dos2unix
mkdir transcript-download
cd transcript-download
youtube-dl -4 -i --write-sub --skip-download --sub-format vtt --sub-lang en https://www.youtube.com/playlist?list=PLiVN676w5O6U6ZSzsGE75anyr86_U_b1C
youtube-dl -4 -i --write-sub --skip-download --sub-format vtt --sub-lang en https://www.youtube.com/playlist?list=PL96C35uN7xGI9HGKHsArwxiOejecVyNem
youtube-dl -4 -i --write-sub --skip-download --sub-format vtt --sub-lang en https://www.youtube.com/playlist?list=PL96C35uN7xGK_y459BdHCtGeftqs5_nff
for i in *.vtt; do ffmpeg -hide_banner -v 16 -i "$i" "$i.srt" ; done
for i in *.srt; do sed -r '/^[0-9]+$/{N;d}' "$i" > "$i.txt"; done
for i in *.txt; do dos2unix -q "$i"; done
for i in *.txt; do echo $(cat "$i") > "$i.txt"; done
for i in *.txt.txt; do echo $(cat "$i") > "$i.txt"; done
cat *.txt.txt.txt > ../tech_diff.txt
cd ..
rm -r transcript-download
