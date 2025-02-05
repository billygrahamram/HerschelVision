

# Herschel Vision
Herschel vision is a graphical user interface application to help you prepare your proximal hyperspectral data for machine learning and deep learning analysis pipelines. This is an open-source application and has been established to be supported by the hyperspectral research community.

# Installation
It is recommend to set up a virtual environment for installing HerschelVision (HV). This will help in dependency compatibility. Using your terminal navigate to the directory you want to install HV. In the repository page click on the dropdown menu called `code`, select local, select https and then copy the github link to the repository.<br>

### Prerequisite
1. Python 3.10 or above
2. Git

### Installation Steps (Mac)

1. In the terminal paste the following command to download the HV repository locally.
    > git clone https://github.com/billygrahamram/HerschelVision.git
2. Change directory to newly cloned repository.
    > cd HerschelVision
3. Create a virtual environement.
    > python -m venv .venv
4. Activate the virtual environment.
    > source .venv/bin/activate
5. Install the required dependencies.
    > pip install -r requirements.txt
6. Change directory to src.
    > cd src
7. Run the script file.
    > python main.py


### Installation Steps (Windows)

1. In the terminal paste the following command to download the HV repository locally.
    > git clone https://github.com/billygrahamram/HerschelVision.git
2. Change directory to newly cloned repository.
    > cd HerschelVision
3. Create a virtual environement.
    > python -m venv .venv
4. Activate the virtual environment.
    > .venv\Scripts\activate
5. Install the required dependencies.
    > pip install -r requirements.txt
6. Change directory to src.
    > cd src
7. Run the script file.
    > python main.py

# Working Examples
Video tutorial series coming soon!

# Cite
If you find HV application and code useful. Kindly cite the following papers in your research:
1. Ram, B. G., Mettler, J., Howatt, K., Ostlie, M., & Sun, X. (2024). WeedCube: Proximal hyperspectral image dataset of crops and weeds for machine learning applications. Data in Brief, 56, 110837. https://doi.org/10.1016/j.dib.2024.110837

2. Ram, Billy; Sun, Xin; Howatt, Kirk; Ostlie, Michael; Mettler, Joseph (2024). Proximal Hyperspectral Image Dataset of Various Crops and Weeds for Classification via Machine Learning and Deep Learning Techniques. Ag Data Commons. Media. https://doi.org/10.15482/USDA.ADC/25306255.v1

3. Citation for application paper coming soon.


## Future Updates
1. Batch processing of images.
2. Segment Anything based image segmentation.
3. Support for morphological operations.
3. Wrapping OS specific executable files.