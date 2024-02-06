Procedure:
1. Generate noise values using noise_values.py.
2. Generate trial parameters using multi_trial.py.
3. Generate noise_gabor values using gabor_values.py (based on the generated parameters).
4. Create directories and generate images using image_generator.py (you may need to change some parameters and call the functions separately).
5. Repeat step 2 to step 4 if you have multiple blocks (previously generated parameters and noise_gabor values will be overwritten, so remember to save them in a safe place).
6. Run the experiment using piloting_rev.py.

Note. All images with the same number share the same noise background.
