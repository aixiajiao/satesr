# satesr
A toolbox aimed at increasing the usage scenarios and utilization of free and open source satellite maps using super-resolution.

set up the environment:

python setup.py 

Achieved functions (see demo.ipynb):

1. Download Bing Aerial maps with coordinates and a definable map radius.
2. Implementation of Real-ESRGAN model.
3. A SR model optimised for satellite imagery. 


The aboved functions have been tested on Linux/Windows/MacOS.
GPU acceleration is only avliable for CUDA enabled devices.

To do list:
1. Use generic models(e.g. YOlO, Unet) to test the SR performance.
2. Further refining the model, the current model is trained using a single RTXA4000 with ~50 high-res photos with minimal train pipeline.
3. add other satellite image sources.
4. add other super-resolution models.

acknowledgment:
sr model developed from https://github.com/xinntao/Real-ESRGAN
aerial photos to train the model: https://arxiv.org/abs/1807.09532