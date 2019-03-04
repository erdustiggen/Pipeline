import numpy as np
from scipy import signal


def processBfData(low_res_data, bfPars, R_mat_dict, use_median_filter, do_aliasing_correction, filter_b, process_packet, skip, kk):
	packet_data = low_res_data[:,:,:,process_packet*kk:(process_packet*kk)+process_packet]
	use_max_ROI = 0 # If both options are 0, interactively chose ROI. (?)
	use_trapezoid_ROI = 1

	# TODO: There is a switch condition here, find out if this is needed. For now, only carotid will be implemented
	max_ROI_depth = 0.032
	min_ROI_depth = 0.005

	# Color Doppler/vector Doppler settings
	drop_samples = 1 # For R1 estimation, avoid clutter filter edge effects
	power_threshold_after_hp = 15 # TODO: Remove hard coding

	# Specle tracking options
	use_corr_threshold = 1
	correlation_threshold = 0.1

	# Angle vectors
	tx_angles = bfPars.tx_vals
	rx_angles = bfPars.rx_vals

	# Filter specs
	pre_c_data = packet_data[:,:,rx_angles==0,:]
	recons_comp_data = pre_c_data.sum(axis=2, dtype=complex) # This changes the shape to a 3D matrix, think it still works, but need further testing

	rem_inds = np.array([4,8]) # TODO: Remove hard coding
	tx_angles = np.delete(tx_angles, rem_inds)
	rx_angles = np.delete(rx_angles, rem_inds)

	l = list(range(9))
	del l[8],l[4]
	packet_data = packet_data[:,:,l]

	low_res_R0_hp_mat = np.zeros([packet_data.shape[0], packet_data.shape[1], rx_angles.size])
	for ii in range(0,rx_angles.size):
		squeezed_arr = np.squeeze(packet_data[:,:,ii,:])
		transposed_arr = np.transpose(np.asfortranarray(squeezed_arr), (2,0,1))

		# Filtering
		filtered_arr = signal.lfilter(filter_b, 1, transposed_arr, axis=0)
		np.set_printoptions(linewidth=50,suppress=True)

		removed_arr = filtered_arr[filter_b.size-1:,:,:]
		temp = np.transpose(np.asfortranarray(removed_arr), (1,2,0))

		low_res_R0_hp_mat[:,:,ii] = np.mean(np.conj(temp)*temp, axis=2)

		# There is an eval statement in the Matlab code, ask about this
		R_mat_dict["R{0}".format(ii+1)] = np.mean(np.conj(temp[:,:,drop_samples:-2]) * temp[:,:,1+drop_samples:-1], axis=2)

	transposed_arr2 = (np.transpose(np.asfortranarray(recons_comp_data), (2, 0, 1)))
	iq_hp_comp = signal.lfilter(filter_b, 1, transposed_arr2, axis=0)
	iq_hp_comp = iq_hp_comp[filter_b.size-1:,:,:]
	iq_hp_comp = np.transpose( np.expand_dims(np.asfortranarray(iq_hp_comp), axis=3), (1,2,3,0) )
	max_iq_hp = np.max(np.abs(iq_hp_comp))
	max_iq = np.max(np.abs(recons_comp_data))

	r0_test = 10*np.log10((np.mean(np.abs(iq_hp_comp)**2,axis=3)))
	r0_test = np.squeeze(r0_test)
	r0_mask = np.zeros(iq_hp_comp.shape[:2])
	print("First r0_shape = ", r0_mask.shape)
	r0_mask = np.where(r0_test > power_threshold_after_hp, 1, 0)

	r1_test = np.mean(np.conj(iq_hp_comp[:,:,:,drop_samples:-1]) * iq_hp_comp[:,:,:,1+drop_samples:],3 )
	r1_test = np.squeeze(r1_test)

	nx = 5
	nz = 5
	my_filter = np.ones([nz,nx])
	n_thresh = 25
	r0_mask_conv = signal.convolve2d(r0_mask,my_filter,mode='same')
	r0_mask_conv = np.where(r0_mask_conv < n_thresh, 0, 1)
	r0_mask = r0_mask_conv
	r1_conv = signal.convolve2d(r1_test,my_filter,mode='same')
	r1_masked = r1_conv * r0_mask

	X,Z = np.meshgrid(bfPars.x_axis, bfPars.z_axis)

	if(use_trapezoid_ROI == 1):
		cfi_mask = np.ones(r0_mask.shape)

	cfi_mask_const = np.tan(np.max(np.abs(tx_angles)))
	cfi_mask_length = cfi_mask.shape[1]
	for zz in range(1,cfi_mask.shape[0]+1):
		n_zeros = np.ceil(zz*cfi_mask_const).astype(int)
		cfi_mask[zz-1,0:n_zeros] = 0
		cfi_mask[zz-1,cfi_mask_length-n_zeros:] = 0

	cfi_mask = np.where(Z < min_ROI_depth, 0, cfi_mask)
	r0_mask = r0_mask * cfi_mask

	# TODO: Remove hard coding, find out where R1 comes from
	r1_multi = np.zeros([184, 274, tx_angles.shape[0]]) * 1j
	for rr in range(0, tx_angles.shape[0]):
		r1_multi[:,:,rr] = R_mat_dict["R{0}".format(rr+1)]


	# Don't think mymask = R0Mask is necessary
	my_mask = r0_mask

	r1_mat = np.zeros([184,274,7])
	r1_mat = r1_mat + 0j
	print("R1 multi shape = ", r1_multi.shape)
	for aa in range(1,tx_angles.shape[0]+1):
		temp = r1_multi[:,:,aa-1]
		r1_mat[:,:,aa-1] = temp * r0_mask

	nx = 7
	nz = 7
	my_filter = (1.0/float(nx*nz) * np.ones([nx, nz]))

	# Spatial averaging
	r1_conv = np.resize(np.expand_dims(r1_conv,2),[184,274,7])
	for aa in range(0, tx_angles.size):
		r1_conv[:,:,aa] = signal.convolve2d(r1_mat[:,:,aa],my_filter,mode='same')

	r1_conv_orig = r1_conv
	print("Mask shape = ", my_mask.shape)
	r0_conv = np.zeros([np.where(my_mask == 1)[0].size, tx_angles.size])
	print("r0_conv shape = ", r0_conv.shape)
	temp_r1_conv = np.ones([24355,7])
	temp_r1_conv = temp_r1_conv*1j
	for angle_nr in range(0, tx_angles.size):
		r1_temp = r1_conv_orig[:,:,angle_nr]
		r1_temp = r1_temp.flatten(order='F')
		r1_temp_masked = r1_temp[my_mask.flatten(order='F') == 1]
		temp_r1_conv[:, angle_nr] = r1_temp_masked
		print(temp_r1_conv.shape)


	return 1
