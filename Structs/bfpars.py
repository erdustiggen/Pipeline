import numpy as np

class BfPars:
	f_demod = None
	band_pass_vec = None
	c = None
	tx_vals = None
	rx_vals = None
	PRF = None
	low_res_rx_apod_dop = None
	low_res_rx_apod_bmode = None
	low_res_rx_fnum_dop = None
	low_res_rx_fnum_bmode = None
	nr_edge_smoothing_elements_dop = None
	nr_edge_smoothing_elements_bmode = None
	probe = None
	x_axis = None
	z_axis = None
	my_mask_x = None
	my_mask_z = None

def initBfPars(init_file_path=""):
	'''
	args: Path to init file
	TODO: implement initializing from a file path
	'''
	bfPars = BfPars()
	bfPars.f_demod = 4750000.0
	bfPars.band_pass_vec = np.array([2000000.0,2200000.0,7300000.0,7400000.0])
	bfPars.c = 1540.0
	bfPars.tx_vals = np.array([-0.2618,-0.2618,-0.2618,-0.2618,0.2618,0.2618,0.2618,0.2618,0.2618])
	bfPars.rx_vals = np.array([-0.2618,-0.0611,0.1047,0.2618,0,-0.1047,0.0611,0.2618,0])
	bfPars.PRF =  6000
	bfPars.low_res_rx_apod_dop = 'hamming'
	bfPars.low_res_rx_apod_bmode =  'hamming'
	bfPars.low_res_rx_fnum_dop = 1.5
	bfPars.low_res_rx_fnum_bmode = 0.9
	bfPars.nr_edge_smoothing_elements_dop = 20
	bfPars.nr_edge_smoothing_elements_bmode = 20
	bfPars.probe = 'GE9L-D'
	bfPars.x_axis =  0 #spio.loadmat("MatlabVariables/bfParsxAxis.mat")['bfParsXAxis'][:,0]
	bfPars.z_axis =  0 #spio.loadmat("MatlabVariables/bfParszAxis.mat")['bfParsZAxis'][:,0]
	bfPars.my_mask_x =  0
	bfPars.my_mask_z =  0
	return bfPars
