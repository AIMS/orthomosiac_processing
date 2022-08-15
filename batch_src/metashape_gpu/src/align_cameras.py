import datetime

# import Metashape
import os, sys, time

start_time = datetime.datetime.now()
step_start = start_time

def progress(label):
    now = datetime.datetime.now()
    step_time = now - step_start
    total_time = now - start_time
    print (f"{label} finished. Step took {step_time}. Total elapsed time = {total_time}")
    return now
image_folder = sys.argv[1]
output_folder = sys.argv[2]

doc = Metashape.Document()
doc.open(output_folder + '/project.psx', ignore_lock=True)
chunk = doc.chunk

chunk.alignCameras(adaptive_fitting=False)
doc.save()
step_start = progress("align cameras")

chunk.optimizeCameras(adaptive_fitting=True, fit_b2=True, fit_k4=True)
doc.save()
step_start = progress("optimize cameras")

