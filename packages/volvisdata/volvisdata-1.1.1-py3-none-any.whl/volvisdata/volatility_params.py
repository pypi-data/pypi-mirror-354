"""
Key parameters for visualizer

"""

# Dictionary of default parameters
vol_params_dict = {
    'ticker':'^SPX',
    'ticker_label':None,
    'start_date':None,
    'wait':2,
    'minopts': 4,
    'mindays':None,
    'lastmins':None,
    'volume':None,
    'openint':None,
    'graphtype':'line',
    'surfacetype':'mesh',
    'smoothing':False,
    'smooth_type_svi':True,
    'scatter':True,
    'voltype':'last',
    'smoothopt':6,
    'notebook':False,
    'data_output':False,
    'show_graph':True,
    'r':0.005,
    'q':0,
    'epsilon':0.001,
    'method':'nr',
    'order':3,
    'spacegrain':100,
    'azim':-50,
    'elev':20,
    'fig_size':(15, 12),
    'rbffunc':'thin_plate',
    'colorscale':'Jet',
    'monthlies':True,
    'divisor':None,
    'divisor_SPX':25,
    'spot':None,
    'strike_limits':(0.5, 2.0),
    'put_strikes':None,
    'call_strikes':None,
    'opacity':0.8,
    'surf':True,
    'save_image':False,
    'image_folder':'images',
    'image_filename':'impvol',
    'image_dpi':50,
    'skew_months':12,
    'skew_direction':'downside',
    'discount_type': 'smooth',
    # Add SVI specific parameters
    'svi_compute_initial': True, # Whether to compute initial params or use the provided ones
    'svi_a_init': 0.04, # Initial value for SVI parameter a (overall level)
    'svi_b_init': 0.04, # Initial value for SVI parameter b (angle between asymptotes)
    'svi_rho_init': 0.0, # Initial value for SVI parameter rho (controls skew)
    'svi_m_init': 0.0, # Initial value for SVI parameter m (horizontal translation)
    'svi_sigma_init': 0.1, # Initial value for SVI parameter sigma (smoothness)
    'svi_max_iter': 1000, # Maximum iterations for SVI optimization
    'svi_tol': 1e-6, # Tolerance for SVI optimization convergence
    'svi_bounds': [
        (0.0, None),       # a: non-negative
        (0.0001, 0.5),     # b: positive but bounded
        (-0.9, 0.9),       # rho: slightly tighter than (-0.9999, 0.9999)
        (-0.5, 0.5),       # m: adding reasonable bounds
        (0.0001, 0.5)      # sigma: positive but bounded
    ],
    # 'svi_bounds': [
    #         (None, None),      # a: no bounds
    #         (0.0001, None),    # b: positive
    #         (-0.9999, 0.9999), # rho: between -1 and 1
    #         (None, None),      # m: no bounds
    #         (0.0001, None)     # sigma: positive
    #     ],

    'svi_reg_weight': 0.01,  # Regularization weight for SVI calibration
    'svi_interpolation_method': 'pchip',  # Options: 'linear', 'quadratic', 'cubic', 'pchip'
    'svi_term_reg_weight': 0.5,  # Weight for term structure regularization
    'svi_joint_calibration': True,  # Whether to use joint calibration

    # Dictionary of implied vol fields used in graph methods
    'vols_dict':{
        'bid':'Imp Vol - Bid',
        'mid':'Imp Vol - Mid',
        'ask':'Imp Vol - Ask',
        'last':'Imp Vol - Last'
        },

    # Dictionary of price fields used for filtering zero prices in
    # graph methods
    'prices_dict':{
        'bid':'Bid',
        'mid':'Mid',
        'ask':'Ask',
        'last':'Last Price'
        },

    # Dictionary of implied vol fields used in implied vol calculation
    'row_dict':{
        'Bid':'Imp Vol - Bid',
        'Mid':'Imp Vol - Mid',
        'Ask':'Imp Vol - Ask',
        'Last Price':'Imp Vol - Last'
        },

    # Dictionary of interpolation methods used in implied vol calculation
    'method_dict':{
        'nr':'implied_vol_newton_raphson',
        'bisection':'implied_vol_bisection',
        'naive':'implied_vol_naive'
        },

    # Dictionary mapping tenor buckets to number of days
    'ir_tenor_dict':{
        '1 Mo':30,
        '2 Mo':60,
        '3 Mo':90,
        '6 Mo':180,
        '1 Yr':365,
        '2 Yr':730,
        '3 Yr':1095,
        '5 Yr':1826,
        '7 Yr':2556,
        '10 Yr':3652,
        '20 Yr':7305,
        '30 Yr':10952
        },

    # Parameters to overwrite mpl_style defaults
    'mpl_line_params':{
        'axes.edgecolor':'black',
        'axes.titlepad':20,
        'axes.xmargin':0.05,
        'axes.ymargin':0.05,
        'axes.linewidth':2,
        'axes.facecolor':(0.8, 0.8, 0.9, 0.5),
        'xtick.major.pad':10,
        'ytick.major.pad':10,
        'lines.linewidth':3.0,
        'grid.color':'black',
        'grid.linestyle':':'
        },

    'mpl_3D_params':{
        'axes.facecolor':'w',
        'axes.labelcolor':'k',
        'axes.edgecolor':'w',
        'lines.linewidth':0.5,
        'xtick.labelbottom':True,
        'ytick.labelleft':True
        },

    }

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
    'Safari/537.36'
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 "
    "Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 "
    "Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
]
