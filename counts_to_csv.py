# my epic script for population counts to csv file conversion
import numpy as np
import scipy
from scipy import optimize
import matplotlib.pyplot as plt

# get derivatives
def derivatives(data_raw):
    # take differences in data, both timepoints and OD/cell count
    local_diff = np.diff(data_raw, n=1, axis=0)

    # calculate instantaneous derivative
    local_derivatives = np.true_divide(local_diff[:,1::], np.transpose([local_diff[:,0]]))

    return local_derivatives


# get growth characteristics
def growth(data_raw):
    deriv = derivatives(data_raw)
    
    # calculate instantaneous growth rate by selecting maximum derivative
    local_instant_growth_rate = np.amax(deriv[1::,:],0)

    # calculate time of growth, by selecting time at which reach max growth rate
    local_time_of_growth = data_raw[np.argmax(deriv[1::,:],0)+1,0]

    return np.argmax(deriv[1::,:],0)


# normalize data to [0,1] interval
def normalize_data(data_raw):
    # subtract minimal value to set zero
    data_raw[:,1::] = np.subtract(data_raw[:,1::], [np.amin(data_raw[:,1::],0)])

    # normalize data to interval [0,1]
    data_raw[:,1::] = np.true_divide(data_raw[:,1::], [np.amax(data_raw[:,1::],0)])


# take logarithm for FACS cell counts
def data_logarithm(data_raw):
    data_raw[:,1::] = np.log(data_raw[:,1::]+1)


# take exponent for fitten exponential curve
def data_exponent(data_raw):
    data_raw[:,1::] = np.exp(data_raw[:,1::])


# fit exponential curve
def fit_exponential(x_data, y_data):
    # define function  to fit exponential
    def exp_func(x, a, b):
        return (a*np.exp(b*x))

    local_params = scipy.optimize.curve_fit(exp_func, x_data, y_data, p0=[10**4,0.01])
    return local_params


# get boundaries for growth interval
def get_usable_samples(x_data, y_data, use_samples, tolerance):
    max_growth = 0
    for i in range(1,len(x_data)):
        cur_growth = (np.log(y_data[i]) - np.log(y_data[i-1]))/(x_data[i] - x_data[i-1])
        if cur_growth > max_growth:
            max_growth = cur_growth
            
    imin = 1
    cur_growth=0
    cur_growth = (np.log(y_data[imin]) - np.log(y_data[imin-1]))/(x_data[imin] - x_data[imin-1])
    while cur_growth < tolerance*max_growth:
        use_samples[0]+=1
        imin += 1
        cur_growth = (np.log(y_data[imin]) - np.log(y_data[imin-1]))/(x_data[imin] - x_data[imin-1])
        
    imax = len(x_data)-1
    cur_growth=0
    cur_growth = (np.log(y_data[imax]) - np.log(y_data[imax-1]))/(x_data[imax] - x_data[imax-1])
    while cur_growth < tolerance*max_growth:
        use_samples[1]-=1
        imax -= 1
        cur_growth = (np.log(y_data[imax]) - np.log(y_data[imax-1]))/(x_data[imax] - x_data[imax-1])
        
    return range(use_samples[0],use_samples[1])

def plot_curves(data_raw):    
    # get the exponential fit
    nr_samples = data_raw.shape[1]
    for i in range(0,nr_samples-1):
            plt.semilogy(data_raw[:,0],  data_raw[:,i+1], 'o--')
    
# analyze data
def analyse_data(data_raw, sample_nr, normalize, take_log, tolerance):    
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
    nr_samples = data_raw.shape[1]
    nr_timepts = data_raw.shape[0]
    i = sample_nr;
    for i in range(0,nr_samples-1):
        # get the index of samples surrounding time of growth
        use_sample_min = max([0,time_of_growth[i]-4])
        use_sample_max = min([nr_timepts,time_of_growth[i]+4])
        use_samples = range(use_sample_min, use_sample_max)

        # fit an exponential curve to the data
        x_val = data_raw[use_samples,0] - np.amin(data_raw[use_samples,0])
        y_val = data_raw[use_samples,i+1]# - np.amin(data_raw[use_samples,i])
        
        use_samples=get_usable_samples(x_val, y_val, [min(use_samples), max(use_samples)+1], tolerance)
        
        # fit an exponential curve to the data
        x_val = data_raw[use_samples,0] - np.amin(data_raw[use_samples,0])
        y_val = data_raw[use_samples,i+1]# - np.amin(data_raw[use_samples,i])
        
        if i == sample_nr:
            plt.semilogy(data_raw[:,0],  data_raw[:,i+1], 'o--')
            plt.semilogy(data_raw[use_samples,0], y_val, 'o--')
        fit_param = fit_exponential(x_val,y_val)
        
        if i == sample_nr:
            plt.semilogy(data_raw[use_samples,0], fit_param[0][0] * np.exp(fit_param[0][1] * x_val))

            print('growth rate: '+str(fit_param[0][1]))