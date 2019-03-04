import sys
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
# import tensorspline as ts # TODO: The tensorbeam, tensorspline mixup needs to be fixed
from scipy import signal
from scipy import interpolate
from math import pi
from numpy import info
import math
import time
import scipy.io as spio
from Structs import bfpars as bfp
from Structs import R_mat_functions as rmf
import processData as pdata



def main():
	bfPars = bfp.initBfPars() # TODO: Should be able to initialize bfPars with a file path

	# TODO: Implement beamforming section and remove loading data
	r_file_path = "/home/emil/NTNU/Master/Code/Pipeline/TempData/LowResBFdata_point1_1_r"
	i_file_path = "/home/emil/NTNU/Master/Code/Pipeline/TempData/LowResBFdata_point1_1_i"

	low_res_data_array = np.fromfile(r_file_path,np.float32,-1)+1j*np.fromfile(i_file_path,np.float32,-1)
	low_res_data = low_res_data_array.reshape(184, 274, 9, 270,order='F')
	print(low_res_data.shape)

	# Filling variables section, think this needs to be changed
	n_angles = bfPars.rx_vals.size
	application = 'carotid'
	process_packet = 270
	skip = 20
	nr_lr_frames = low_res_data.shape[3]
	max_num_process_packets = np.arange(start=process_packet/2,stop=(nr_lr_frames-process_packet/2)+1, step=skip).size
	start_packet = 0
	nr_packets = 1 # TODO: Find out how this can be altered
	use_median_filter = 1
	do_aliasing_correction = 1
	filter_b = spio.loadmat('TempData/b_filter.mat')['b'][0]


	R_mat_dict = rmf.init_R_matrices()


	#TODO: Find out what the function should return for the visualization part.
	for kk in range(0, nr_packets):
		returned_data = pdata.processBfData(low_res_data, bfPars, R_mat_dict, use_median_filter, do_aliasing_correction, filter_b, process_packet, skip, kk)


if __name__ == '__main__':
	main()
