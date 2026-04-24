
## Stochastic-Modeling-for-Hospital-Systems

## Project Overview
This project implements **Fractal Image Compression** using the **Iterated Function System (IFS)** approach. The goal is to compress images by mapping larger domain blocks to smaller range blocks and storing transformations instead of pixel data.

## Features
- Basic image preprocessing  
- Domain–range block creation  
- Affine transformation matching  
- Fractal encoding and decoding  
- PSNR‐based quality analysis  

## Deliverables
- **Report (10–12 pages)**  
- **Source code** for fractal encoding & decoding  
- **Results** with reconstructed images  

## How to Run
1. Install Python dependencies:  
   ```bash
   pip install pillow numpy matplotlib
   ```
2. Run the main script:  
   ```bash
   python fractal_compression.py
   ```

## Output
- Reconstructed image  
- Compression ratio  
- PSNR score  

## Folder Structure
```
├── README.md
├── report/
├── images/
├── src/
│   ├── fractal_compression.py
│   └── utils.py
```

## Conclusion
The project demonstrates efficient image compression using fractal mathematics and affine transformations.
