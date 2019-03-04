import numpy as np

def init_R_matrices():
	R_mat_dict = {}
	for x in range (1, 8):
		R_mat_dict["R{0}".format(x)] = np.zeros([184, 274])
	return R_mat_dict
