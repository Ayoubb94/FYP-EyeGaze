#from sklearn import svm
import os
import msgpack


def pupils():
	with open(os.path.expanduser("~/Documents/Imperial/4th_year/FYP/EyeGazeData/pupil_data"), "rb") as fh:
	   pupil_data = msgpack.unpack(fh, encoding="utf-8")

	#print(pupil_data)
	print(type(pupil_data))
	for key, val in pupil_data.items():
		print(key, len(val))
	print(len(pupil_data))


def eyegaze():
	with open(os.path.expanduser("~/Documents/Imperial/4th_year/FYP/EyeGazeData/gaze_small/ruohan_1_gaze"), "rb") as fh:
	   ruohan_1_gaze = msgpack.unpack(fh, encoding="utf-8")


if __name__ == "__main__":
	pupils()
	#eyegaze()