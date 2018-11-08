# my epic script for population counts to csv file conversion
import numpy as np
from scipy import optimize

# get derivatives
def derivatives(data_raw):
	# take differences in data, both timepoints and OD/cell count
	local_diff = np.diff(data_raw, n=1, axis=0)

	# calculate instantaneous derivative
	local_derivatives = np.true_divide(local_diff[:,1::], np.transpose([local_diff[:,0]])

	return local_derivatives



# get growth characteristics
def growth(data_raw):
	deriv = derivatives(data_raw)

	# calculate instantaneous growth rate by selecting maximum derivative
	local_instant_growth_rate = np.amax(deriv,0)

	# calculate time of growth, by selecting time at which reach max growth rate
	local_time_of_growth = data_raw[np.argmax(deriv,0),0]

	print(local_instant_growth_rate)
	print()
	print(local_time_of_growth)

	return local_time_of_growth



# normalize data to [0,1] interval
def normalize_data(data_raw):
	# subtract minimal value to set zero
	data_raw[:,1::] = np.subtract(data_raw[:,1::], [np.amin(data_raw[:,1::],0)])

	# normalize data to interval [0,1]
	data_raw[:,1::] = np.true_divide(data_raw[:,1::], [np.amax(data_raw[:,1::],0)])

	return 0



# take logarithm for FACS cell counts
def data_logarithm(data_raw):
	data_raw[:,1::] = np.log(data_raw[:,1::])
	return 0



# take exponent for fitten exponential curve
def data_exponent(data_raw):
	data_raw[:,1::] = np.exp(data_raw[:,1::])
	return 0



# fit exponential curve
def fit_exponential(x_data, y_data):
	# define function  to fit exponential
	def exp_func(t, a, b):
		return a*np.exp(b*t)

	local_params = scipy.optimize.curve_fit(func, x_data, y_data)[0]

	return local_params


# analyze data
def analyse_data(data_raw, normalize, take_log):
	# preprocess data
	if normalize == 1:
		normalize_data(data_raw)
	if take_log == 1:
		data_logarithm(data_raw)

	# get time of growth (maximum instantenious derivative)
	time_of_growth = growth(data_raw)

	# go back to linear y-axis (small values relatively unimportant)
	data_exponent(data_raw)

	# get the exponential fit
	nr_samples = data_raw.shape(1)
	nr_timepts = data_raw.shape(0)
	for i in range(1,nr_samples):
		# get the index of samples surrounding time of growth
		use_sample_min = min([0,time_of_growth(i)-4])
		use_sample_max = max([nr_timepts,time_of_growth(i)+2])
		use_samples = range(use_sample_min, use_sample_max)

		# fit an exponential curve to the data
		fit_param = fit_exponential(data_raw[:,0],data_raw[use_samples,i])
		print('sample ' + i + ' has params ' + fit_param);

	return 0
