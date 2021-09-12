# Eyerony

## Inspiration 👁️
Have you ever wanted to delete all the pictures you took where you have your eyes closed? Well we did just the opposite! Place all your photos into the dropbox and **BOOM** all the photos with closed eyes come out! Have fun with all your bad photos!

## What it does 👀
Eyerony helps you choose the _best_ group photos possible. Simply upload all the photos to our website and our machine learning algorithm will select the photos with closed eyes. Never worry about which photo to post to Instagram again!

## How we built it 👁️‍🗨️
We built a Flask website that allows users to upload images, using Flask-reuploaded and Flask-dropzone. OpenCV finds the eyes in the images and pipes them into a convoluted neural network. The CNN detects whether the eyes are open or closed and photos with closed eyes are returned. 

## Challenges we ran into 👁
We were able to make the machine learning algorithm and website to upload images. However, we struggled to export the model and connect the two parts. Hosting the website was also difficult because we needed a non-static site host.

## Accomplishments that we're proud of  ¯\_(☯෴☯)_/¯ 
We are most proud of being able to connect the file uploading, OpenCV, DNN, and file downloading all together to create this website. We had a really fun time and just being able to create something together was super fun!

## What we learned 👁️👄👁️
We always wanted to try OpenCV and combine that with machine learning. I think this project allowed us to combine and develop a lot of both of our expertise in backend, frontend, and ML.

## What's next for Eyerony 🚀
We want to fine tune our CNN model so that it has a higher accuracy by normalizing our data from our training dataset more. We would also want to make a reverse mode for non-eyeronic people so they can get photos with opened eyes. 
