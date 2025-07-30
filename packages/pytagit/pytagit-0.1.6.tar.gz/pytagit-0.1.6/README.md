![License](https://img.shields.io/badge/license-CC--BY--NC--4.0-blue.svg)

### PyTagit

**PyTagit** is a human-in-the-loop tool for large-scale image classification.  
Install and launch it with:

```bash
# install
pip install pytagit

# run the program
pytagit
```

If you use PyTagit, please cite us:

```
# citation
```

---

### Features

At startup, all images are unclassified. You can assign them via drag-and-drop:

![Main window](https://github.com/dros1986/pytagit/blob/main/res/main_window.png?raw=true)

Start by assigning a few examples per class. Then, apply:

- **Random Forest** or **k-NN** to classify the rest.
- Visit each class and click to mark correct predictions. Once clicked, the border will become red.
- Repeat the process to reclassify using the verified samples.

For accelerated labeling, use:

#### Interactive t-SNE

Draw a decision boundary directly on a 2D feature map to assign multiple samples:

![t-SNE](https://github.com/dros1986/pytagit/blob/main/res/interactive_tsne.png?raw=true)

#### Out-of-Distribution Detection

Useful for quality control scenarios: find samples close to a class using feature-based OOD:

![OOD](https://github.com/dros1986/pytagit/blob/main/res/visual_ood.png?raw=true)

To classify all samples, use Random Forest with a confidence threshold of 0.
