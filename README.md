# Innovaid2023

This repository contains the code used in the InnovAId 2023 Hackathon.
The jury bestowed the honor upon us of receiving 1st prize at the conclusion of the event.

## Topic

The topic we got to tackle during the hackathon concerned the automatic detection of depression, or depressive episodes, through the tracking of eyemovements.
An online platform tracks the gaze of a participant while the display shows several sets of 2 images.
One image could be a positive image, such as a happy face, cute animals or good food.
Another image could be a negative image, such as a dead animal, angry faces or war imagery.
Finally, neutral images were also present, such as a building, landscape or car.

The contrast between the emotional impact of each image is presumed to have a measurably different effect on a depressive participant, versus one that is not.
For example, a depressed participant may not have the same reaction to an image of a dead animal, or may have an exaggerated reaction to one of a shouting person.
The challenge was to see if it was possible to find this effect through available eye movement.

## Methods

Throughout the challenge we had extremely limited time to explore solutions, so we can keep this section relatively short.

### Data

The data consisted of several sessions, each with a unique ID.
Throughout the session, the eye position was measured roughly every few milliseconds.
With some early calibration, the eye position can be matched to a position on the display, including the image the participant is looking at.

All in all, the data consisted of 3102 sessions, each consisting of a few scenes.
The raw data had the following columns:

- Timestamp (ms)
- BPOGX and BPOGY (Absolute position on the display)
- RX and RY (Relative position on the display)
- Scene_Index (Each set of images is a new ID)
- Image (The image ID, images not included)
- Image_Position (Whether the image was left or right on the monitor)
- Image_Type (Whether the image was negative, neutral or positive)
- Image_Tags (A short description of the image)

The labels were based on the PSQ-9 and BDI questionnaires.
Each session had both scores available.
For simplicity's sake, and with consultation of the challenge provider, we focussed on purely the BDI measurements, which we then divided into 4 classes:

| BDI score | Category           | Class |
|-----------|--------------------|-------|
| 0 - 9     | None to Minimal    | 0     |
| 10 - 18   | Mild to Moderate   | 1     |
| 19 - 29   | Moderate to Severe | 2     |
| 30 - 63   | Severe             | 3     |

Given the limited time, we chose two avenues to explore.
One track explored the use of feature engineering.
That is, compressing the complex tracking data into simpler, measurable properties of a specific participant.
The other track aimed to see if the raw data directly provided to a neural network would give us the desired results.
The plan would be for the neural network to find it's own features that relate to the output measurement.

### Feature engineering

Because timeseries data is a complex type of data, that can signify a great many things, we decided to select a few easily measurable features to use with a random forest classifier.
Mainly, we measured the average velocity of the eyes, time spent looking at a given image, times switched between the left and right images and the total distance covered on the display.
These features have given us reasonable initial results, but other features may prove to be better predictors of the depression score.

#### Related files

- Code/notebooks/Classifier.ipynb
- Code/notebooks/get_variables.ipynb

### Neural Network

The other way, and the method we expect to perform the best, given enough time and resources, was a neural network.
These would get fed the raw timeseries data, and find their own features with which to predict a depression score.
Unfortunately, we didn't have the time or compute power to experiment a lot with this, so the only models we were able to train simply predicted that every participant had a moderate depression, seeing as that class was most represented in our dataset.

#### Related files

- Code/preprocess.py
- Code/innovaid/loader.py
- Code/notebooks/train_torch.py


## Future works

None in our team had experience with time series data, though we have some ideas that could be pursued, outside the confines of a hackathon.
Recently, transformer architectures have been making waves as a core building block of large language models.
Seeing as text is a variable length series, that is, each word is related to the prior word and subsequent word, and our data is a variable length timeseries, perhaps exploring such a model can bring the performance required.
This is, of course, assuming there is any biomarker present in eye movement that will map nicely to depression.