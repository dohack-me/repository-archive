sudo docker build -t challenge1 .
sudo docker run --rm -it --entrypoint=which challenge1 firefox
# /usr/bin/firefox
sudo docker run --rm -it --entrypoint=which challenge1 geckodriver
# /usr/local/bin/geckodriver
sudo docker run -d -p 5000:5000 challenge1