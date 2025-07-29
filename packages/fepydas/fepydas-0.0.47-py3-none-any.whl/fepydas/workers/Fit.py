#!/usr/bin/python3
import numpy
from multiprocessing.pool import Pool
import pickle
from inspect import getsource
from datetime import datetime
from lmfit import Parameters, minimize, fit_report
from fepydas.libs.fit_functions import (
    BiExponential,
    BiExponentialTail,
    Exponential,
    Gaussian,
    Lorentzian,
    Linear,
    TriExponential,
    Quadratic,
)
from fepydas.datatypes.Data import Transformation
from scipy.signal import convolve


class Fit:
    """
    A class for fitting data using various fitting functions.
    """

    def __init__(self, function):
        """
        Initializes a Fit instance.

        Args:
            function: The fitting function to use.

        Returns:
            None
        """
        self.function = function

    def saveBinary(self, filename):
        """
        Saves the fit object to a binary file using pickle.

        Args:
            filename (str): The path to the file where the fit object will be saved.

        Returns:
            None
        """
        f = open(filename, "bw")
        pickle.dump(self, f)
        f.close()

    def toTransformation(self):
        """
        Converts the fit results to a Transformation object.

        Returns:
            Transformation: The transformation based on the fit results.
        """
        return Transformation(self.function, self.result.params.valuesdict())

    def initializeParameters(self, parameters: Parameters):
        """
        Initializes the parameters for the fit.

        Args:
            parameters (Parameters): The parameters to initialize.

        Returns:
            None
        """
        self.parameters = parameters

    def residual(self, params, x, data=None, eps=None):
        """
        Calculates the residuals between the fit and the data.

        Args:
            params: The parameters for the fit.
            x (numpy.ndarray): The x values.
            data (optional): The data values to fit. Defaults to None.
            eps (optional): The error values. Defaults to None.

        Returns:
            numpy.ndarray: The calculated residuals.
        """
        parvals = params.valuesdict()
        if eps is not None:
            return (data - self.function(x, **parvals)) * eps
        else:
            return data - self.function(x, **parvals)

    def residualLog(self, params, x, data=None, eps=None):
        """
        Calculates the log residuals between the fit and the data.

        Args:
            params: The parameters for the fit.
            x (numpy.ndarray): The x values.
            data (optional): The data values to fit. Defaults to None.
            eps (optional): The error values. Defaults to None.

        Returns:
            numpy.ndarray: The calculated log residuals.
        """
        parvals = params.valuesdict()
        vals = self.function(x, **parvals)
        vals = numpy.maximum(vals, numpy.full_like(vals, 1e-9))
        if eps is not None:
            return (numpy.log(data) - numpy.log(vals)) * eps
        else:
            return numpy.log(data) - numpy.log(vals)

    def convolve(self, signal, ref):
        """
        Convolves the signal with a reference function.

        Args:
            signal (numpy.ndarray): The signal to convolve.
            ref (numpy.ndarray): The reference function.

        Returns:
            numpy.ndarray: The convolved signal.
        """
        return convolve(signal, ref, mode="full")[: len(signal)]

    def convolutedResidual(self, params, x, data=None, irf=None):
        """
        Calculates the residuals for a convoluted fit.

        Args:
            params: The parameters for the fit.
            x (numpy.ndarray): The x values.
            data (optional): The data values to fit. Defaults to None.
            irf (optional): The instrument response function. Defaults to None.

        Returns:
            numpy.ndarray: The calculated convoluted residuals.
        """
        parvals = params.valuesdict()
        return data - self.convolve(self.function(x, **parvals), irf)

    def fit(self, x, y, eps=None, nan_policy="raise", log=False):
        """
        Fits the data using the specified fitting method.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.
            eps (optional): The error values. Defaults to None.
            nan_policy (str, optional): The policy for handling NaN values. Defaults to "raise".
            log (bool, optional): If True, uses log fitting. Defaults to False.

        Returns:
            The result of the fitting process.
        """
        if log:
            self.result = minimize(
                self.residualLog,
                self.parameters,
                args=(x, y, eps),
                method="leastsq",
                nan_policy=nan_policy,
            )
        else:
            self.result = minimize(
                self.residual,
                self.parameters,
                args=(x, y, eps),
                method="leastsq",
                nan_policy=nan_policy,
            )
        return self.result

    def fitSpectrum(self, spectrum):
        """
        Fits a spectrum using the fitting method.

        Args:
            spectrum: The spectrum to fit.

        Returns:
            The result of the fitting process.
        """
        return self.fit(spectrum.axis.values, spectrum.data.values)

    def batchFit(self, x, y):
        """
        Fits a batch of data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.

        Returns:
            None
        """
        print("BatchFit", x.shape, y.shape)
        args = {}
        for i in range(y.shape[0]):
            args[i] = [x, y[i]]
        self.executeBatchFit(self.fit, args)

    def convolutedFit(self, x, y, irf):
        """
        Fits the data using a convoluted fitting method.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.
            irf (numpy.ndarray): The instrument response function.

        Returns:
            The result of the fitting process.
        """
        self.result = minimize(
            self.convolutedResidual, self.parameters, args=(x, y, irf)
        )
        return self.result

    def convolutedBatchFit(self, x, y, irf):
        """
        Fits a batch of data using a convoluted fitting method.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.
            irf (numpy.ndarray): The instrument response function.

        Returns:
            None
        """
        args = {}
        for i in range(y.shape[0]):
            args[i] = [x, y[i], irf]
        self.executeBatchFit(self.convolutedFit, args)

    def executeBatchFit(self, func, args):
        """
        Executes batch fitting using multiprocessing.

        Args:
            func: The fitting function to execute.
            args (dict): The arguments for the fitting function.

        Returns:
            None
        """
        pool = Pool()
        jobs = {}
        for key in args.keys():
            jobs[key] = pool.apply_async(func, args[key])
        results = {}
        for key in args.keys():
            results[key] = jobs[key].get(1000)
        self.results = results

    def batchEvaluate(self, x):
        """
        Evaluates the fitted model for a batch of x values.

        Args:
            x (numpy.ndarray): The x values to evaluate.

        Returns:
            numpy.ndarray: The evaluated data.
        """
        data = numpy.ndarray(shape=(len(self.results.keys()), len(x)))
        for key in self.results.keys():
            pars = self.results[key].params.valuesdict()
            data[key, :] = self.function(x, **pars)
        return data

    def batchEvaluateConvolution(self, x, irf):
        """
        Evaluates the fitted model for a batch of x values with convolution.

        Args:
            x (numpy.ndarray): The x values to evaluate.
            irf (numpy.ndarray): The instrument response function.

        Returns:
            numpy.ndarray: The evaluated convolved data.
        """
        data = self.batchEvaluate(x)
        for i in range(data.shape[0]):
            data[i, :] = self.convolve(data[i, :], irf)
        return data

    def evaluate(self, x):
        """
        Evaluates the fitted model for the given x values.

        Args:
            x (numpy.ndarray): The x values to evaluate.

        Returns:
            numpy.ndarray: The evaluated data based on the fitted parameters.
        """
        parvals = self.result.params.valuesdict()
        return self.function(x, **parvals)

    def evaluateInput(self, x):
        """
        Evaluates the model using the input parameters.

        Args:
            x (numpy.ndarray): The x values to evaluate.

        Returns:
            numpy.ndarray: The evaluated data based on the input parameters.
        """
        parvals = self.parameters.valuesdict()
        return self.function(x, **parvals)

    def evaluateConvolution(self, x, irf):
        """
        Evaluates the convolution of the fitted model with the IRF.

        Args:
            x (numpy.ndarray): The x values to evaluate.
            irf (numpy.ndarray): The instrument response function.

        Returns:
            numpy.ndarray: The convolved data.
        """
        return self.convolve(self.evaluate(x), irf)

    def startReport(self, filename):
        """
        Starts a report for the fitting process.

        Args:
            filename (str): The path to the file where the report will be saved.

        Returns:
            file object: The opened file object for writing the report.
        """
        f = open(filename, "w")
        f.write("Generated by Fit: {0}\n".format(self.__class__.__name__))
        f.write("Time: {0}\n".format(datetime.now()))
        f.write("Model: {0}\n".format(self.function.__name__))
        f.write("{0}\n".format("\n".join(getsource(self.function).split("\n")[1:-1])))
        f.write("Input Parameters: \n")
        for p in self.parameters.keys():
            f.write(
                "  {0}:\t{1}\t[{2}:{3}]\n".format(
                    p,
                    self.parameters[p].value,
                    self.parameters[p].min,
                    self.parameters[p].max,
                )
            )
        f.write("---\n")
        return f

    def saveReport(self, filename):
        """
        Saves the fitting report to a file.

        Args:
            filename (str): The path to the file where the report will be saved.

        Returns:
            None
        """
        f = self.startReport(filename)
        params = self.parameters.keys()
        f.write("Parameter\tValue\tError\n")
        for p in params:
            f.write(
                "{0}\t{1}\t{2}\n".format(
                    p, self.result.params[p].value, self.result.params[p].stderr
                )
            )
        f.write(
            "\nnfev\t{0}\tchisqr\t{1}\tredchi\t{2}\n".format(
                self.result.nfev, self.result.chisqr, self.result.redchi
            )
        )
        f.close()

    def batchSaveReport(self, filename, labels):
        """
        Saves a batch report of fitting results to a file.

        Args:
            filename (str): The path to the file where the report will be saved.
            labels (list): The labels for the datasets in the report.

        Returns:
            None
        """
        f = self.startReport(filename)
        keys = self.results.keys()
        params = self.parameters.keys()
        f.write("Dataset")
        for p in params:
            f.write("\t{0}\t{0}Error".format(p))
        f.write("\tnfev\tchisqr\tredchi")
        f.write("\n")
        for k in keys:
            f.write("{0}".format(labels[k]))
            for p in params:
                f.write(
                    "\t{0}\t{1}".format(
                        self.results[k].params[p].value,
                        self.results[k].params[p].stderr,
                    )
                )
            f.write(
                "\t{0}\t{1}\t{2}".format(
                    self.results[k].nfev, self.results[k].chisqr, self.results[k].redchi
                )
            )
            f.write("\n")
        f.close()

    def initializeAutoFromSpectrum(self, spectrum):
        """
        Initializes the fitting parameters automatically from a spectrum.

        Args:
            spectrum: The spectrum object to initialize from.

        Returns:
            None
        """
        self.initializeAuto(spectrum.axis.values, spectrum.data.values)

    def saveLMfitReport(self, filepath):
        """
        Saves the fit report generated by the lmfit result object to a file.

        Args:
            filepath: The file path where the fit report will be written.

        Returns:
            None
        """
        with open(filepath, "w") as f:
            f.write(fit_report(self.result))


class LorentzianFit(Fit):
    """
    A class for fitting data using a Lorentzian function.
    """

    def __init__(self):
        """
        Initializes a LorentzianFit instance.

        Returns:
            None
        """
        super().__init__(Lorentzian)


class SpectralLine(LorentzianFit):
    """
    A class for fitting spectral lines using a Lorentzian function.
    """

    def __init__(self):
        """
        Initializes a SpectralLine instance.

        Returns:
            None
        """
        super().__init__()

    def initializeAuto(self, x, y):
        """
        Initializes fitting parameters automatically based on provided x and y data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.

        Returns:
            None
        """
        bg = (y[0] + y[-1]) / 2
        I = numpy.max(y) - bg
        x0 = x[numpy.argmax(y)]
        idx = numpy.where(y > bg + I / 2)[0]
        fwhm = numpy.abs(x[idx[-1]] - x[idx[0]])
        params = Parameters()
        params.add("bg", value=bg)
        params.add("I", value=I)
        params.add("x0", value=x0)
        params.add("fwhm", value=fwhm)
        self.initializeParameters(params)


class GaussianFit(Fit):
    """
    A class for fitting data using a Gaussian function.
    """

    def __init__(self):
        """
        Initializes a GaussianFit instance.

        Returns:
            None
        """
        super().__init__(Gaussian)

    def initializeAuto(self, x, y):
        """
        Initializes fitting parameters automatically based on provided x and y data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.

        Returns:
            None
        """
        bg = (y[0] + y[-1]) / 2
        I = numpy.max(y) - bg
        x0 = x[numpy.argmax(y)]
        idx = numpy.where(y > bg + I / 2)[0]
        fwhm = numpy.abs(x[idx[-1]] - x[idx[0]])
        params = Parameters()
        params.add("bg", value=bg)
        params.add("I", value=I)
        params.add("x0", value=x0)
        params.add("fwhm", value=fwhm + x0 / 1000)
        self.initializeParameters(params)


class LimitedGaussianFit(GaussianFit):
    """
    A class for fitting data using a limited Gaussian function.
    """

    def __init__(self):
        """
        Initializes a LimitedGaussianFit instance.

        Returns:
            None
        """
        super().__init__()

    def initializeAutoLimited(self, x, y, center, range, thresh=1):
        """
        Initializes fitting parameters for a limited Gaussian fit based on provided x and y data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.
            center (float): The center value for the fit.
            range (float): The range around the center to consider for fitting.
            thresh (float, optional): The threshold for peak detection. Defaults to 1.

        Returns:
            tuple: A tuple containing the x and y values used for fitting, or False if fitting is not possible.
        """
        if (len(numpy.where(y == numpy.max(y))[0])) > 1:
            return False, False
        lowerIdx = (numpy.abs(x - (center - range))).argmin()
        higherIdx = (numpy.abs(x - (center + range))).argmin()
        if numpy.abs(higherIdx - lowerIdx) < 15:
            return False, False
        if higherIdx < lowerIdx:
            t = lowerIdx
            lowerIdx = higherIdx
            higherIdx = t
        x = x[lowerIdx:higherIdx]
        y = y[lowerIdx:higherIdx]
        if numpy.amax(y) <= thresh:
            return False, False
        self.initializeAuto(x, y)
        return x, y


class LinearFit(Fit):
    """
    A class for fitting data using a linear function.
    """

    def __init__(self):
        """
        Initializes a LinearFit instance.

        Returns:
            None
        """
        super().__init__(Linear)


class CalibrationFit(LinearFit):
    """
    A class for fitting calibration data using a linear function.
    """

    def __init__(self):
        """
        Initializes a CalibrationFit instance.

        Returns:
            None
        """
        super().__init__()

    def initializeAuto(self):
        """
        Initializes fitting parameters automatically for calibration.

        Returns:
            None
        """
        params = Parameters()
        params.add("a", value=1)
        params.add("b", value=0)
        self.initializeParameters(params)


class QuadraticFit(Fit):
    """
    A class for fitting data using a quadratic function.
    """

    def __init__(self):
        """
        Initializes a QuadraticFit instance.

        Returns:
            None
        """
        super().__init__(Quadratic)


class QuadraticCalibrationFit(QuadraticFit):
    """
    A class for fitting calibration data using a quadratic function.
    """

    def __init__(self):
        """
        Initializes a QuadraticCalibrationFit instance.

        Returns:
            None
        """
        super().__init__()

    def initializeAuto(self):
        """
        Initializes fitting parameters automatically for quadratic calibration.

        Returns:
            None
        """
        params = Parameters()
        params.add("a", value=0)
        params.add("b", value=1)
        params.add("c", value=0)
        self.initializeParameters(params)


class AutomaticCalibration(QuadraticCalibrationFit):
    """
    A class for performing automatic calibration based on a spectrum and reference data.
    """

    def __init__(self, spectrum, references, threshold=10, width=10):
        """
        Initializes an AutomaticCalibration instance.

        Args:
            spectrum (Spectrum): The spectrum to calibrate.
            references (numpy.ndarray): The reference values for calibration.
            threshold (float, optional): The threshold for peak detection. Defaults to 10.
            width (int, optional): The width for peak detection. Defaults to 10.

        Returns:
            None
        """
        super().__init__()
        peaks = spectrum.identifyPeaks(threshold=threshold, width=width)
        SpectralFit = SpectralLine()
        peakVals = []
        peakErrs = []
        for peak in peaks:
            x, y = (
                spectrum.axis.values[peak[0] : peak[1]],
                spectrum.data.values[peak[0] : peak[1]],
            )
            SpectralFit.initializeAuto(x, y)
            SpectralFit.fit(x, y)
            peakVals.append(SpectralFit.result.params["x0"].value)
            peakErrs.append(SpectralFit.result.params["x0"].stderr)
        references = numpy.array(references, dtype=numpy.float64)
        peakVals = numpy.array(peakVals, dtype=numpy.float64)
        peakErrs = numpy.array(peakErrs, dtype=numpy.float64)
        idx = numpy.where(~numpy.isnan(references))[0]
        print("Calibration with ", references, peakVals, idx)
        self.initializeAuto()
        self.fit(peakVals[idx], references[idx])


class ExponentialFit(Fit):
    """
    A class for fitting data using an exponential function.
    """

    def __init__(self):
        """
        Initializes an ExponentialFit instance.

        Returns:
            None
        """
        super().__init__(Exponential)

    def initialize(self, bg, I, x0, tau, rise):
        """
        Initializes the parameters for the exponential fit.

        Args:
            bg (float): The background level.
            I (float): The peak intensity.
            x0 (float): The position of the peak.
            tau (float): The decay constant.
            rise (float): The rise time.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=bg)
        params.add("I", value=I, min=0)
        params.add("x0", value=x0)
        params.add("tau", value=tau, min=0)
        params.add("rise", value=rise, min=0)
        self.initializeParameters(params)

    def initializeAuto(self, x, y):
        """
        Initializes fitting parameters automatically based on provided x and y data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=y[0])
        params.add("I", value=numpy.max(y) - y[0], min=0)
        # params.add("I_rise",value=numpy.max(y)-y[0],min=0)
        params.add("x0", value=x[numpy.argmax(y)])
        params.add("tau", value=1, min=0)
        params.add("rise", value=0.001, min=0)
        self.initializeParameters(params)


class BiExponentialFit(Fit):
    """
    A class for fitting data using a bi-exponential function.
    """

    def __init__(self):
        """
        Initializes a BiExponentialFit instance.

        Returns:
            None
        """
        super().__init__(BiExponential)

    def initializeAuto(self, x, y):
        """
        Initializes fitting parameters automatically based on provided x and y data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=y[0])
        params.add("I_1", value=(numpy.max(y) - y[0]) / 2, min=0)
        params.add("I_2", value=(numpy.max(y) - y[0]) / 2, min=0)
        params.add("x0", value=x[numpy.argmax(y)])
        params.add("tau_1", value=5, min=0)
        params.add("tau_2", value=50, min=0)
        params.add("rise", value=0.001, min=0)
        self.initializeParameters(params)

    def initialize(self, I_1, I_2, tau_1, tau_2, x0=0, rise=0.001):
        """
        Initializes the parameters for the bi-exponential fit.

        Args:
            I_1 (float): The intensity of the first exponential.
            I_2 (float): The intensity of the second exponential.
            tau_1 (float): The decay constant for the first exponential.
            tau_2 (float): The decay constant for the second exponential.
            x0 (float, optional): The position of the peak. Defaults to 0.
            rise (float, optional): The rise time. Defaults to 0.001.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=0)
        params.add("I_1", value=I_1, min=0)
        params.add("I_2", value=I_2, min=0)
        params.add("x0", value=x0)
        params.add("tau_1", value=tau_1, min=0)
        params.add("tau_2", value=tau_2, min=0)
        params.add("rise", value=rise, min=0)
        self.initializeParameters(params)


class TriExponentialFit(Fit):
    """
    A class for fitting data using a tri-exponential function.
    """

    def __init__(self):
        """
        Initializes a TriExponentialFit instance.

        Returns:
            None
        """
        super().__init__(TriExponential)

    def initializeAuto(self, x, y):
        """
        Initializes fitting parameters automatically based on provided x and y data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=y[0])
        params.add("I_1", value=(numpy.max(y) - y[0]) / 3, min=0)
        params.add("I_2", value=(numpy.max(y) - y[0]) / 3, min=0)
        params.add("I_3", value=(numpy.max(y) - y[0]) / 3, min=0)
        params.add("x0", value=x[numpy.argmax(y)])
        params.add("tau_1", value=5, min=0)
        params.add("tau_2", value=50, min=0)
        params.add("tau_3", value=500, min=0)
        params.add("rise", value=0.001, min=0)
        self.initializeParameters(params)

    def initialize(self, I_1, I_2, I_3, tau_1, tau_2, tau_3, x0=0, rise=0.001):
        """
        Initializes the parameters for the tri-exponential fit.

        Args:
            I_1 (float): The intensity of the first exponential.
            I_2 (float): The intensity of the second exponential.
            I_3 (float): The intensity of the third exponential.
            tau_1 (float): The decay constant for the first exponential.
            tau_2 (float): The decay constant for the second exponential.
            tau_3 (float): The decay constant for the third exponential.
            x0 (float, optional): The position of the peak. Defaults to 0.
            rise (float, optional): The rise time. Defaults to 0.001.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=0)
        params.add("I_1", value=I_1, min=0)
        params.add("I_2", value=I_2, min=0)
        params.add("I_3", value=I_3, min=0)
        params.add("x0", value=x0)
        params.add("tau_1", value=tau_1, min=0)
        params.add("tau_2", value=tau_2, min=0)
        params.add("tau_3", value=tau_3, min=0)
        params.add("rise", value=rise, min=0)
        self.initializeParameters(params)


class BiExponentialTailFit(Fit):
    """
    A class for fitting data using a bi-exponential tail function.
    """

    def __init__(self):
        """
        Initializes a BiExponentialTailFit instance.

        Returns:
            None
        """
        super().__init__(BiExponentialTail)

    def initializeAuto(self, x, y):
        """
        Initializes fitting parameters automatically based on provided x and y data.

        Args:
            x (numpy.ndarray): The x values for fitting.
            y (numpy.ndarray): The y values for fitting.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=y[-1])
        params.add("I_1", value=(numpy.max(y) - y[-1]) / 2, min=0)
        params.add("I_2", value=(numpy.max(y) - y[-1]) / 2, min=0)
        params.add("tau_1", value=5, min=0)
        params.add("tau_2", value=50, min=0)
        self.initializeParameters(params)

    def initialize(self, I_1, I_2, tau_1, tau_2):
        """
        Initializes the parameters for the bi-exponential tail fit.

        Args:
            I_1 (float): The intensity of the first exponential.
            I_2 (float): The intensity of the second exponential.
            tau_1 (float): The decay constant for the first exponential.
            tau_2 (float): The decay constant for the second exponential.

        Returns:
            None
        """
        params = Parameters()
        params.add("bg", value=0)
        params.add("I_1", value=I_1, min=0)
        params.add("I_2", value=I_2, min=0)
        params.add("tau_1", value=tau_1, min=0)
        params.add("tau_2", value=tau_2, min=0)
        self.initializeParameters(params)
