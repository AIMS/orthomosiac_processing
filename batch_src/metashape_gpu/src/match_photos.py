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



def find_files(folder, types):
    return [entry.path for entry in os.scandir(folder) if (entry.is_file() and os.path.splitext(entry.name)[1].lower() in types)]

if len(sys.argv) < 3:
    print("Usage: general_workflow.py <image_folder> <output_folder>")
    sys.exit(1)

image_folder = sys.argv[1]
output_folder = sys.argv[2]

print(Metashape.app.Settings)
#Metashape.app.Settings.log_enabled = True
#Metashape.app.Settings.log_path = '/home/ssm-user/greg/log.log'

photos = find_files(image_folder, [".jpg", ".jpeg", ".tif", ".tiff"])
step_start = progress("find photos")

doc = Metashape.Document()
doc.save(output_folder + '/project.psx')
doc.read_only = False

chunk = doc.addChunk()

chunk.addPhotos(photos)
# doc.save()

print(str(len(chunk.cameras)) + " images loaded")
step_start = progress("add photos")

chunk.matchPhotos(keypoint_limit = 60000, tiepoint_limit = 6000, generic_preselection = True, reference_preselection =True, downscale=1)
doc.save()
step_start = progress("match photos")
