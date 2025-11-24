# BAH-FPS code. 

This is a Python application that samples molecular configurations using the BAH and FPS algorithms.

## Project Structure

```
BAH_FPS
├── src
│   └── BAH.py
    └── FPS.py 
    └── functions.py                
├── requirements.txt
└── README.md
```

## How to install the Application

1. Make sure you have Python installed on your machine.
2. Navigate to the project directory.
3. Run the application using the following command:

   ```
   pip install -r requirements.txt
   pip install .
   ```
## How to run the Application
The sample executable script is BAH_and_FPS.py. Please add the xsf_directory folder path and options such as divs (number of bins in BAH algorithm),
FPS_structures (number of structure to be extracted by FPS) and ncpus (no of threads in parallel processing).
The structure input files must be in XCrySDen Structure file (.xsf) format and should be located in xsf_directory.
Run the code by following command.
``` python BAH_and_FPS.py ```

## Dependencies

This project's dependencies are given in the ```requirements.txt``` file.

## Citations
If you find this code helpful in your research, please cite the following articles:
1. Parent paper;```Gutal, A., & Paranjothy, M. (2025). The Journal of Chemical Physics, 163(15). ```
2. Bin and Hash Algorithm:```Paleico, M. L., & Behler, J. (2021), Machine Learning: Science and Technology, 2(3), 037001.```
3. Furthest Point Sampling:```Cersonsky, R. K., Helfrecht, B. A., Engel, E. A., Kliavinek, S., & Ceriotti, M. (2021), Machine Learning: Science and Technology, 2(3), 035038. ```
