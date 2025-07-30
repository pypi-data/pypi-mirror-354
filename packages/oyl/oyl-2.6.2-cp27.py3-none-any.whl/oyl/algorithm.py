import numpy as np
from scipy.interpolate import griddata
from scipy import stats

class PointTransformer2D:
    """
    给定数据的xy坐标之后可以做缩放、旋转、平移等变换
    """

    def __init__(self, x, y):
        """
        输入数据的xy坐标完成初始化
        这个输入可以是列表、数组
        对于不是一维的数组会重组成一维并记录下来形状，最后获取变化后的点的时候再重组回原来的形状
        """
        assert hasattr(x, "__iter__") and hasattr(y, "__iter__")
        x = np.array(x)
        if x.ndim > 1:
            self.shape = x.shape
            x = x.flatten()
            y = np.array(y).flatten()
        assert len(x) == len(y)
        self.vpts = np.vstack((x, y, np.ones_like(x)))
        self.transform = np.eye(3)

    def __relative_trasform(self, transform_matrix, center):
        self.move(-center)
        self.transform = transform_matrix @ self.transform
        self.move(center)

    def zoom(self, times=(1, 1), center=(0, 0)):
        """
        输入xy方向的缩放倍数和缩放的中心，可以完成缩放
        """
        sx, sy = times
        zoo_matrix = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        self.__relative_trasform(zoo_matrix, np.array(center))

    def rotate(self, theta, thete_unit="degree", direction="anticlockwise", center=(0, 0)):
        """
        输入旋转角度和单位以及顺逆时针和旋转中心完成旋转
        """
        theta = theta if direction != "clockwise" else 360 - theta
        ang = np.deg2rad(theta) if thete_unit != 'rad' else theta
        rot_matrix = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
        vec = np.array(center)
        self.__relative_trasform(rot_matrix, np.array(center))

    def move(self, vector=(0, 0)):
        """
        输入移动矢量可以完成移动
        """
        tx, ty = vector
        mov_matrix = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
        self.transform =  mov_matrix @ self.transform

    def get_points(self):
        """
        直接获取变换之后的点
        """
        pts = (self.transform @ self.vpts)[:2]
        if hasattr(self, "shape"):
            x, y = pts
            return x.reshape(self.shape), y.reshape(self.shape)
        return pts[:2]

def rotatie_circle(arr, x=np.arange(10, 41), y=np.arange(20, 36), center=(0, 0), radius=10, **kwargs):
    data = arr.copy()
    X, Y = np.meshgrid(x, y) if x.ndim < 2 and y.ndim < 2 else (x, y)
    x0, y0 = center
    distance = np.sqrt((X - x0) ** 2 + (Y - y0) ** 2)
    ind = distance <= radius
    ind_ext = distance <= radius * 1.414
    pts_ext = np.vstack((X[ind_ext], Y[ind_ext]))
    pts = np.vstack((X[ind], Y[ind]))
    transformer = PointTransformer2D(*pts_ext)
    transformer.rotate(center=center, **kwargs)
    interp_d = griddata(transformer.get_points().T, data[ind_ext], pts.T)
    data[ind] = interp_d
    return data

class DataCoef:

    def __init__(self, x, y, axis=None, degree_of_freedom=None, skipna=True):
        x, y = self.__check_xy_dim(x, y, axis)
        self.mean = np.nanmean if skipna else np.mean
        self.axis = axis
        self.mean_x = self.mean(x, axis=axis, keepdims=True)
        self.mean_y = self.mean(y, axis=axis, keepdims=True)
        anox, anoy = x - self.mean_x, y - self.mean_y
        self.std_x = np.sqrt(self.mean(anox**2,axis=axis,keepdims=True))
        self.std_y = np.sqrt(self.mean(anoy**2,axis=axis,keepdims=True))
        self.norm_x, self.norm_y = anox/self.std_x, anoy/self.std_y
        if axis is None:
            n = int(np.prod(y.shape))
        else:
            n = int(np.prod(np.array(y.shape).take(axis)))
        self.df = n - 2 if not degree_of_freedom else degree_of_freedom

    def __check_xy_dim(self, x, y, axis):
        err_mess = f"Please check the dimesion of x and y, {x.shape} and {y.shape} can't be caculated along axis {axis} !"
        if (x.ndim < 1) | (y.ndim < 1):
            raise RuntimeError(err_mess)
        if axis is None:
            if np.prod(x.shape) != np.prod(y.shape):
                raise RuntimeError(err_mess)
            return x, y
        if x.ndim < y.ndim:
            x = np.broadcast_to(x, y.shape)
        elif x.ndim < y.ndim:
            y = np.broadcast_to(y, x.shape)
        dimx, dimy = np.array(x.shape), np.array(y.shape)
        if np.prod(dimx.take(axis)) != np.prod(dimy.take(axis)):
            raise RuntimeError(err_mess)
        return x, y

    def coef(self):
        self.cc = np.clip(self.mean(self.norm_x * self.norm_y, axis=self.axis, keepdims=True), -1, 1)
        self.t = self.cc * np.sqrt(self.df)/np.sqrt(1 - np.clip(self.cc, -0.999, 0.999) ** 2)
        p = stats.t.cdf(np.abs(self.t), self.df)
        self.signific_level = 2 - 2 * p
        return self.cc, self.signific_level

    def linregress(self):
        if hasattr(self, "cc"):
            cc, signific_level = self.cc, self.t, self.signific_level
        else:
            cc, signific_level = self.coef()
        slope = cc * self.std_y/self.std_x
        intercept = self.mean_y - slope * self.mean_x
        return slope, intercept, cc, signific_level

def coef(x, y, axis=None, degree_of_freedom=None, skipna=True):
    """
    Calculate a correlation coefficient for two sets of measurements.

    Parameters
    ----------
    x, y : array_like
        Two sets of measurements. Both arrays should have the same length in specific dimesion.
    axis : int or tuple of int
        Along which dimesion to caculate correlation coefficient.
    degree_of_freedom : int
        Sometimes the t-test should be performed with effective degree of freedom.
    Returns
    -------
    result : 
        rvalue : float
            The correlation coefficient.
        pvalue : float
            The p-value for a hypothesis test whose null hypothesis is
            that the slope is zero, using Wald Test with t-distribution of
            the test statistic. 
    """
    solver = DataCoef(x, y, axis,degree_of_freedom, skipna)
    res = solver.coef()
    return [r.squeeze() for r in res]
    
def linregress(x, y, axis=None, degree_of_freedom=None, skipna=True):
    """
    Calculate a linear least-squares regression for two sets of measurements.

    Parameters
    ----------
    x, y : array_like
        Two sets of measurements. Both arrays should have the same length in specific dimesion.
    axis : int or tuple of int
        Along which dimesion to caculate a linear regression.
    degree_of_freedom : int
        Sometimes the t-test should be performed with effective degree of freedom.
    Returns
    -------
    result : 
        slope : float
            Slope of the regression line.
        intercept : float
            Intercept of the regression line.
        rvalue : float
            The Pearson correlation coefficient. The square of ``rvalue``
            is equal to the coefficient of determination.
        pvalue : float
            The p-value for a hypothesis test whose null hypothesis is
            that the slope is zero, using Wald Test with t-distribution of
            the test statistic. 
    """
    solver = DataCoef(x, y, axis, degree_of_freedom, skipna)
    res = solver.linregress()
    return [r.squeeze() for r in res]

status = {"high":"__gt__", "high_equal":"__ge__", ">":"__gt__", ">=":"__ge__",
          "low":"__lt__", "low_equal":"__le__", "<":"__lt__", "<=":"__le__"}
class SystemRecognition:

    def __init__(self):
        pass

    def recognize_path(self, arr, radius=1, center_status='high_equal', lat=None, lon=None, return_time_index=True, tolerance=None, min_event_sep=None, strategy='max'):
        assert arr.ndim == 3
        nt = len(arr)
        tolerance = np.inf if tolerance is None else tolerance
        min_event_sep = np.inf if min_event_sep is None else min_event_sep
        miss, tol = 0, 1
        res_history, time_indexs, paths, times = [], [], [], []
        for i in range(nt):
            his_len = len(res_history)
            res = self.select_grid_center(arr[i], radius, center_status, lat=lat, lon=lon, return_field=False, strategy=strategy)
            if res is None:
                if his_len > 0:
                    miss += 1
                    tol += 1
                    if miss > min_event_sep:
                        if his_len < 1:
                            warn_message = "No local extremum hapeends in the given time steps and no system recongnized."
                            warn(warn_message)
                            return None
                        else:
                            paths.append(np.vstack(res_history).T)
                            times.append(np.array(time_indexs))
                            res_history, time_indexs = [], []
                    continue
            elif his_len < 1:
                mode = "backward"
                if len(res[0]) < 2:
                    res = res[0][0], res[1][0]
                    mode = "forward"
                res_history.append(res)
                time_indexs.append(i)
            elif len(res[0]) > 1:
                if mode == "backward":
                    tol += 1
                    if tol > tolerance:
                        warn_message = "Run out of tolerance and no system recongnized."
                        warn(warn_message)
                        return None
                else:
                    distance = np.sum((np.vstack(res_history[-1]) - np.vstack(res)) ** 2, 0)
                    ind = np.argmin(distance)
                    res = res[0][ind], res[1][ind]
                res_history.append(res)
                time_indexs.append(i)
            else:
                if mode == "backward":
                    # print(f"{his_len = }")
                    for j in range(1, 1 + his_len):
                        last = res if j < 2 else res_history[1 - j]
                        distance = np.sum((np.vstack(res_history[-j]) - np.vstack(last)) ** 2, 0)
                        ind = np.argmin(distance)
                        # print(res_history[-j], end=' ')
                        res_history[-j] = res_history[-j][0][ind], res_history[-j][1][ind]
                    else:
                        mode = "forward"
                res_history.append((res[0][0], res[1][0]))
                time_indexs.append(i)
        paths.append(np.vstack(res_history).T)
        times.append(np.array(time_indexs))
        if return_time_index:
            return paths, times
        return paths

    @staticmethod
    def select_grid_center(arr, radius=1, center_status='high_equal', lat=None, lon=None, return_field=False, strategy='none'):
        assert arr.ndim == 2
        method = status.get(center_status, None)
        window_size = 2 * radius + 1
        if method is None:
            warn_message = f"center_status '{center_status}' was not recognized, defaulting to 'high'"
            warn(warn_message)
            method = "__ge__"
        window = np.lib.stride_tricks.sliding_window_view(arr, (window_size, window_size), axis=(-1,  -2))
        window_bool = getattr(window[..., radius:radius+1, radius:radius+1], method)(window)
        window_bool[..., radius, radius] = True
        ind = np.nonzero(window_bool.all((-1, -2)))
        if len(ind[0]) < 1:
            return None
        inds = ind[0] + radius, ind[1] + radius
        if (len(ind[0]) > 1) & (strategy != 'none'):
            func = np.argmax if strategy != 'min' else np.argmin
            idx = func(arr[inds])
            inds = inds[0][idx : idx + 1], inds[1][idx : idx + 1]
        if (lon is None) & (lat is None):
            result = list(inds)
        else:
            if (lat.ndim == 1) & (lon.ndim == 1):
                lon, lat = np.meshgrid(lon, lat)
            result = [lat[inds], lon[inds]]
        if return_field:
            result.append(window[ind])
        return tuple(result)
