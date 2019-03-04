import pytest
import numpy as np

from Pipeline.Structs import bfpars


def test_bfpars_init(init_file_path = ""):

	# Arrange
	bfPars = bfpars.BfPars()
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

	# Act
	bfPars_func = bfpars.initBfPars()

	# Assert
	assert bfPars.f_demod == bfPars_func.f_demod
	np.testing.assert_array_almost_equal(bfPars.band_pass_vec, bfPars_func.band_pass_vec)
	assert bfPars.c == bfPars_func.c
	np.testing.assert_array_almost_equal(bfPars.tx_vals, bfPars_func.tx_vals,5)
	np.testing.assert_array_almost_equal(bfPars.rx_vals, bfPars_func.rx_vals,5)
	assert bfPars.PRF == bfPars_func.PRF
	assert bfPars.low_res_rx_apod_dop == bfPars_func.low_res_rx_apod_dop
	assert bfPars.low_res_rx_apod_bmode == bfPars_func.low_res_rx_apod_bmode
	assert bfPars.low_res_rx_fnum_dop == bfPars_func.low_res_rx_fnum_dop
	assert bfPars.low_res_rx_fnum_bmode == bfPars_func.low_res_rx_fnum_bmode
	assert bfPars.nr_edge_smoothing_elements_dop == bfPars_func.nr_edge_smoothing_elements_dop
	assert bfPars.nr_edge_smoothing_elements_bmode == bfPars_func.nr_edge_smoothing_elements_bmode
	assert bfPars.probe == bfPars_func.probe
	assert bfPars.x_axis == bfPars_func.x_axis
	assert bfPars.z_axis == bfPars_func.z_axis
	assert bfPars.my_mask_x == bfPars_func.my_mask_x
	assert bfPars.my_mask_z == bfPars_func.my_mask_z
