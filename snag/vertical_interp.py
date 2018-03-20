"""
code to interpolate input data on single column model levels
interpolation with height will be linear, expect for pressure, which should be linear in log(pressure)
model levels are eta height levels and are specified by a list from 0-1 and the elevation of the model top and bottom.
input should cover the range of heights and be in height.
the model has both
Jono Conway
"""

import numpy as np

# defaults

kill_interp = True  # disable auto-grid interpolation. Recommended set to True, as is bug in model. If kill_interp = True, the eta arrays are not actually used by the model, but are used to construct the input data
model_levels_nml = 85  # if kill_interp=True, this should match model_levels in the UM namelist SIZES
z_tom_nml = 85000.0  # if kill_interp=True, this should match z_top_of_model = 85000.00,
eta_th_nml = np.array([0.0000000E+00, 0.2352941E-03, 0.6274510E-03, 0.1176471E-02, 0.1882353E-02,
              0.2745098E-02, 0.3764706E-02, 0.4941176E-02, 0.6274510E-02, 0.7764705E-02,
              0.9411764E-02, 0.1121569E-01, 0.1317647E-01, 0.1529412E-01, 0.1756863E-01,
              0.2000000E-01, 0.2258823E-01, 0.2533333E-01, 0.2823529E-01, 0.3129411E-01,
              0.3450980E-01, 0.3788235E-01, 0.4141176E-01, 0.4509804E-01, 0.4894118E-01,
              0.5294117E-01, 0.5709804E-01, 0.6141176E-01, 0.6588235E-01, 0.7050980E-01,
              0.7529411E-01, 0.8023529E-01, 0.8533333E-01, 0.9058823E-01, 0.9600001E-01,
              0.1015687E+00, 0.1072942E+00, 0.1131767E+00, 0.1192161E+00, 0.1254127E+00,
              0.1317666E+00, 0.1382781E+00, 0.1449476E+00, 0.1517757E+00, 0.1587633E+00,
              0.1659115E+00, 0.1732221E+00, 0.1806969E+00, 0.1883390E+00, 0.1961518E+00,
              0.2041400E+00, 0.2123093E+00, 0.2206671E+00, 0.2292222E+00, 0.2379856E+00,
              0.2469709E+00, 0.2561942E+00, 0.2656752E+00, 0.2754372E+00, 0.2855080E+00,
              0.2959203E+00, 0.3067128E+00, 0.3179307E+00, 0.3296266E+00, 0.3418615E+00,
              0.3547061E+00, 0.3682416E+00, 0.3825613E+00, 0.3977717E+00, 0.4139944E+00,
              0.4313675E+00, 0.4500474E+00, 0.4702109E+00, 0.4920571E+00, 0.5158098E+00,
              0.5417201E+00, 0.5700686E+00, 0.6011688E+00, 0.6353697E+00, 0.6730590E+00,
              0.7146671E+00, 0.7606701E+00, 0.8115944E+00, 0.8680208E+00, 0.9305884E+00,
              0.1000000E+01])  # An array of length model_levels_nml + 1. If kill_interp=True,These should match the eta_theta in the vertical levels file.

eta_rho_nml = np.array([0.1176471E-03, 0.4313726E-03, 0.9019608E-03, 0.1529412E-02, 0.2313725E-02,
               0.3254902E-02, 0.4352941E-02, 0.5607843E-02, 0.7019607E-02, 0.8588235E-02,
               0.1031373E-01, 0.1219608E-01, 0.1423529E-01, 0.1643137E-01, 0.1878431E-01,
               0.2129412E-01, 0.2396078E-01, 0.2678431E-01, 0.2976470E-01, 0.3290196E-01,
               0.3619608E-01, 0.3964706E-01, 0.4325490E-01, 0.4701960E-01, 0.5094118E-01,
               0.5501961E-01, 0.5925490E-01, 0.6364705E-01, 0.6819607E-01, 0.7290196E-01,
               0.7776470E-01, 0.8278431E-01, 0.8796078E-01, 0.9329412E-01, 0.9878433E-01,
               0.1044314E+00, 0.1102354E+00, 0.1161964E+00, 0.1223144E+00, 0.1285897E+00,
               0.1350224E+00, 0.1416128E+00, 0.1483616E+00, 0.1552695E+00, 0.1623374E+00,
               0.1695668E+00, 0.1769595E+00, 0.1845180E+00, 0.1922454E+00, 0.2001459E+00,
               0.2082247E+00, 0.2164882E+00, 0.2249446E+00, 0.2336039E+00, 0.2424783E+00,
               0.2515826E+00, 0.2609347E+00, 0.2705562E+00, 0.2804726E+00, 0.2907141E+00,
               0.3013166E+00, 0.3123218E+00, 0.3237787E+00, 0.3357441E+00, 0.3482838E+00,
               0.3614739E+00, 0.3754014E+00, 0.3901665E+00, 0.4058831E+00, 0.4226810E+00,
               0.4407075E+00, 0.4601292E+00, 0.4811340E+00, 0.5039334E+00, 0.5287649E+00,
               0.5558944E+00, 0.5856187E+00, 0.6182693E+00, 0.6542144E+00, 0.6938630E+00,
               0.7376686E+00, 0.7861323E+00, 0.8398075E+00, 0.8993046E+00, 0.9652942E+00])


# an array of length model_levels_nml. If kill_interp=True, these should match the eta_rho in the vertical levels file.

# heights are given by eta * z_tom_nml. i.e. first eta_rho_nml = 0.1176471E-03 *85,000 = 10 m

VERTICAL_GRIDS = [
    'theta',
    'theta_without_surf',
    'rho',
    'rho_with_model_top'
]


def vert_interp(inp_array, var_name, inp_vert_levels, vertical_grid):
    """
    interpolate the input data to the staggered vertical levels required for the single column model.

    output required:
    theta-levels
        theta Initial potential temperature profile (theta-levels - 1) Real (rw,rl,ml) K - no surface value - surface set by tstari
        qi Initial specific humidity profile (theta-levels - 1) Real (rw,rl,wl) kg/kg - no surface value - surface set by tstari and surface type
        wi Initial vertical wind profile (theta-levels) Real (rw,rl,0:ml) m/s - surface value should be 0
        w_advi Initial w advective wind profile (theta-levels) Real (rw,rl,0:ml) m/s - surface value should be 0
    rho-levels
        ui Initial zonal wind profile (rho-levels) Real (rw,rl,ml) m/s
        vi Initial meridional wind profile (rho-levels) Real (rw,rl,ml) m/s
    rho-levels + model top
        p_in Pressure profile on rho-levels(rho-levels + 1) Real (rw,rl,1:ml+1) Pa - extra at top

    :param inp_array: array of input data with dimensions (time,level). if the file has only one dimension, the dimension is assumed to be the level.
    :param var_name: name of variable. options are 'p_in', 'theta', 'qi', 'wi', 'w_advi', 'ui', 'vi'
    :param inp_vert_levels: array containing vertical levels corresponding to length of level coordinate in inp_array
    :return: out_array: array of data with dimensions (time,level) formatted to SCM levels. Will return a 2D array, even if a 1D array is passed in.
    """

    # check model levels for consistency
    assert len(eta_rho_nml) == model_levels_nml
    assert len(eta_th_nml) == model_levels_nml + 1
    assert eta_th_nml[0] == 0.0
    assert eta_th_nml[-1] == 1.0

    # find out how many timesteps in input file
    if inp_array.ndim == 1:
        num_inp_timesteps = 1
    elif inp_array.ndim == 2:
        num_inp_timesteps = inp_array.shape[0]

    # set vertical levels needed.
    if var_name == 'p':
        inp_array = np.log(inp_array)  # convert to log pressure for interpolation

    if vertical_grid == 'rho':
        out_levels = eta_rho_nml * z_tom_nml
    elif vertical_grid == 'rho_with_model_top':
        out_levels = np.concatenate((eta_rho_nml, [1.0])) * z_tom_nml
    elif vertical_grid == 'theta':
        out_levels = eta_th_nml * z_tom_nml
    elif vertical_grid == 'theta_without_surf':
        out_levels = eta_th_nml[1:] * z_tom_nml
    else:
        raise ValueError('Unknown vertical grid: {}'.format(vertical_grid))

    out_array = np.empty((num_inp_timesteps, len(out_levels)))

    if inp_array.ndim == 1:
        out_array[0, :] = np.interp(out_levels, inp_vert_levels, inp_array[:])
    else:
        for i in range(num_inp_timesteps):
            out_array[i, :] = np.interp(out_levels, inp_vert_levels, inp_array[i, :])

    if var_name == 'p':  # convert back from log pressure
        out_array = np.exp(out_array)

    return out_levels, out_array


def calc_tendencies(obs_array, obs_dt_array):
    """
    calculate tendencies needed for observational forcing.
    tendencies are in units per day
    :param obs_array: array of input data with dimensions (time,level). Assumes the first data point is also the start time.
    :param obs_dt_array: array of datetimes corresponding to time dimension of scm_inp_array
    :return: tend_out: array of tendencies calculated for every observation input time except the inital time.
    """

    # calculate gradient excluding the inital point
    tend = np.gradient(obs_array, axis=0)

    # scale units to per day
    tstep_per_day = 86400.0 / (obs_dt_array[1] - obs_dt_array[0]).total_seconds()
    tend_per_day = tend * tstep_per_day

    return tend_per_day[1:,:]