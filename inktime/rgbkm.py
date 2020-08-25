# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_rgbkm.ipynb (unless otherwise specified).

__all__ = ['reflectance']

# Cell
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2

import scipy.optimize as optimize


def reflectance(K, S, D, Rg):
    '''Calculates reflectance for single colorant Kubelka-Munk model.

    Based on Nobbs (1997) formulation with modified Saunderson expression for infinite reflectance.
    Function works for single channel, 3 RGB channels, and spectral data/images with muliple wavelength channels.


    Parameters:
    -----------
        K: tuple-like (n channels)
            Colorant absorption coefficients for wavelength or RGB channels
        S: tuple-like (n channels)
            Colorant scattering coefficients for wavelength or RGB channels
        D: array ( height x width)
            Colorant thickness image
        Rg: array (height x width x n) or rgb tuple with shape (3,)
            Background reflectance image or background color

    Returns:
    --------
        refl: array (height x width x n)
            n-channel reflectance image

    '''

    Rg = np.array(Rg)
    shape = Rg.shape


    # create uniform background image if Rg is rgb tuple

    if len(shape) == 1: # understood as rgb tuple

        h, w = D.shape

        Rg_img = np.ones([h, w, 3])
        Rg_img[:,:] = Rg
        Rg = Rg_img

        shape = Rg.shape

        #print('created uniform rgb background image Rg with shape: {}'.format(shape))


    n_channels = shape[-1]

    K = np.array(K).reshape(1, n_channels)
    S = np.array(S).reshape(1, n_channels)

    D = np.array(D).reshape(-1, 1)
    Rg = Rg.reshape(-1, n_channels)

    # need to return infinity for K =< 0 or S < 0 in optimization code
    #pos_S = S >= 0
    #pos_K = K > 0 # also non-zero
    #ok = pos_S & pos_K

    #Rinf = np.zeros([1, n_channels])
    Rinf = (S/K) / ((S/K) + 1 + np.sqrt(1 + 2 * (S/K)))
    #Rinf[ok] = (S[ok]/K[ok]) / ((S[ok]/K[ok]) + 1 + np.sqrt(1 + 2 * (S[ok]/K[ok])))
    #Rinf[~ok] = np.infty

    Z = D * np.sqrt(K * (K + 2 * S))

    Z = np.clip(Z, a_min=0, a_max=50)

    beta = np.exp(2 * Z) - 1
    alpha = (1 - Rinf**2) / (1 - Rg * Rinf)

    refl = (alpha * Rg + beta * Rinf) / (alpha + beta)
    refl = refl.reshape(shape)

    return refl