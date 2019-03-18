import math
from operator import itemgetter

# imports for Parallelograms
import numpy as np
import matplotlib
import heapq
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'

    def __repr__(self):
        return "Point(%d, %d)" % (self.x, self.y)

class Parallelogram:
    def __init__(self, coords_ls, m=None, b=None):
        """
        :param `coords_ls` <list>: list of points that form the parallelogram.
            If only 2 points in the list, they are assumed to be the top-left and
                bottom-right coordinates of a parallelogram with right angles.
                Required: m and b (coefficents of equation for top border: y=mx+b).
            If 4 Points in the list, they are assumed to be the 4 corners of the shape.
        :param `m` <float>: slope of top border (y=mx+b).
        :param `b` <float>: when x = 0.

        Resulting calculations:
            self.p1 : top-left corner of bounding box.
            self.p2: top-right corner of bounding box.
            self.p3: bottom-right corner of bounding box.
            self.p4 : bottom-left corner of bounding box.
        """
        num_points = len(coords_ls)

        self.p1 = coords_ls[0]
        self.p2 = None
        self.p3 = coords_ls[1]
        self.p4 = None

        if num_points == 2:
            if m and b:
                # TODO: Need more accurate and robust calculations
                self.p2 = Point(self.p3.x, self.p1.y)
                self.p4 = Point(self.p1.x, self.p3.y)
            else:
                # TODO: Need more accurate and robust calculations
                # currently just a quick-and-dirty implementation
                self.p2 = Point(self.p3.x, self.p1.y)
                self.p4 = Point(self.p1.x, self.p3.y)
            
        elif num_points == 4:
            self.p2 = coords_ls[1]
            self.p3 = coords_ls[2]
            self.p4 = coords_ls[3]
        else:
            raise ValueError(f"Object takes a list with either 2 points or 4 points. {num_points} points were given")
        # get the point closest to the origin; that one will be the top-left corner point

    def get_width(self):
        # TODO: need more robust distance calculation
        return self.p2.x - self.p1.x
    
    def get_height(self):
        # TODO: need more robust distance calculation
        return self.p4.y - self.p1.y
    
    @staticmethod
    def __sort_by_distance(coords_ls):
        p0 = Point(0, 0) # origin for distance calculation
        dist_ls = [(p, p.distance(p0)) for p in coords_ls]
        return sorted(dist_ls,key=itemgetter(0))

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3 and self.p4 == other.p4

    def __str__(self):
        return f"({self.p1}, {self.p2}, {self.p3}, {self.p4})"

class Parallelograms:
    bandwidth_grid = None
    
    def __init__(self, initial_list=[], meta_list=[]):
        self.list = initial_list
        self.meta_list = meta_list
        self.left_plot, self.right_plot, self.top_plot, self.bot_plot = None, None, None, None
        self.left_pixel_align, self.right_pixel_align = None, None
        self.top_pixel_align, self.bot_pixel_align = None, None
        self.plot_dict = {}
    
    def append(self, para, meta=None):
        self.list.append(para)
        if meta:
            self.meta_list.append(meta)
    
    def __str__(self):
        str_ls = [item.__str__() for item in self.list]
        return "\n".join(str_ls)
    
    def set_bandwidth(self, X, manual_num=None):
        bandwidth = manual_num
        if manual_num is None:
            # calculate bandwith using 10-fold cross-validation
            grid = self.set_grid()
            grid.fit(X)
            bandwidth = grid.best_params_['bandwidth']
        return bandwidth

    def set_grid(self, reset=False):
        if not Parallelograms.bandwidth_grid or reset:
            Parallelograms.bandwidth_grid = GridSearchCV(KernelDensity(kernel='tophat'),
                {'bandwidth': np.linspace(0.1, 1.0, 100)},
                cv=8) # 10-fold cross-validation
        return Parallelograms.bandwidth_grid
                
    def get_pixel_intervals(self, x_range, scale=1.0):
        start = 0
        end = max(x_range)
        num_samples = (end - start)*(1/scale)
        return np.linspace(start, end, num_samples)[:, np.newaxis]

    def get_highest_density_pixels(self, log_dens):
        densities = np.exp(log_dens)
        dict_indents = {}
        for i in range(len(densities)):
            density = densities[i]
            if not math.isinf(density):
                if density in dict_indents:
                    dict_indents[density].append(i)
                else:
                    dict_indents[density] = [i]

        # unsorted_ls = [(density, x_left) for density, x_left in dict_indents.items()]
        # sorted_tups = sorted(unsorted_ls, key=lambda x: x[0])
        # print("*"*60)
        # for density, x_left in sorted_tups:
        #     if density > 0.1:
        #         print(density, x_left)
        # print("*"*60)

        max_density = max(dict_indents, key=float)
        
        # print(f"max_density: {max_density}")
        # print(dict_indents[max_density])

        return dict_indents[max_density], max_density

    def calculate_alignment(self, samples_ls, scale=1.0, plot=None):
        X = np.array(samples_ls)[:, np.newaxis]
        X_plot = self.get_pixel_intervals(samples_ls, scale)

        tophat_bandwidth = self.set_bandwidth(X)
        kde = KernelDensity(kernel='tophat', bandwidth=tophat_bandwidth).fit(X)
        log_dens = kde.score_samples(X_plot)
        pixels, max_density = self.get_highest_density_pixels(log_dens)

        # in case of plotting
        if plot:
            if plot not in self.plot_dict:
                self.plot_dict[plot] = {}
            self.plot_dict[plot]["X_plot"] = X_plot
            self.plot_dict[plot]["densities"] = np.exp(log_dens)
            
        return pixels, max_density

    def calculate_alignment_range(self, densities):
        density_deltas = np.append([0], np.diff(densities))
        density_deltas = abs(density_deltas)
        
        # get indexes of two largest deltas
        largest_index = heapq.nlargest(2, range(len(density_deltas)), density_deltas.__getitem__)
        # largest_2 = heapq.nlargest(2, enumerate(density_deltas), key=lambda x: x[1])
        
        start_index = largest_index[0]
        end_index = largest_index[1]

        if start_index > end_index:
            start_index = largest_index[1]
            end_index = largest_index[0]
        
        return start_index, end_index

    def get_left_alignment(self, scale=1.0):
        scale = float(scale) if not isinstance(scale, float) else scale
        lefts = [gram.p1.x*scale for gram in self.list]

        likeliest_ls, max_density = self.calculate_alignment(samples_ls=lefts, scale=scale, plot="left")
        self.left_pixel_align = min(likeliest_ls)
        return self.left_pixel_align, max_density
    
    def get_right_alignment(self, scale=1.0):
        """
        Calculate right alignment of text. Since English documents are usually not right-justified, 
        the variance of density peaks here will be much larger than get_left_alignment's KDE peaks.
        As a result, this method will be using calculate_alignment_range() to help determine 
        full breadth of KDE peaks.
        """
        scale = float(scale) if not isinstance(scale, float) else scale
        rightmost = 2493
        right_diffs = [(rightmost-gram.p3.x)*scale for gram in self.list]
        
        # # right_diff_align, max_density = self.calculate_alignment(samples_ls=right_diffs, scale=scale, plot="right")
        # # self.right_pixel_align = [rightmost-diff for diff in right_diff_align]
        # self.right_pixel_align, max_density = self.calculate_alignment(samples_ls=right_diffs, scale=scale, plot="right")

        self.right_pixel_align, max_density = self.calculate_alignment(samples_ls=right_diffs, scale=scale, plot="right")
        densities = self.plot_dict["right"]["densities"]
        start, end = self.calculate_alignment_range(densities)
        # # find weighted average
        # range_ls = list(range(start, end+1))
        # weighted_avg = 0.0
        # for pixel in range_ls:
        #     density = densities[pixel]
        #     weighted_avg += pixel*density
        
        # weighted_avg = weighted_avg/len(range_ls)
        # self.right_pixel_align = rightmost-weighted_avg

        avg = math.ceil((start + end)/2)
        self.right_pixel_align = rightmost-avg
        return self.right_pixel_align, max_density

    def get_top_alignment(self, scale=1.0):
        right_margin = self.right_pixel_align
        left_margin = self.left_pixel_align

        midpoint = left_margin + (right_margin-left_margin)/2.0
        num_pages = max(self.meta_list)
        tops = [-1]*num_pages
        top_y = [5000]*num_pages
        for i in range(len(self.list)):
            idx_num = self.meta_list[i]-1
            gram = self.list[i]
            if (tops[idx_num] == -1) and (gram.p1.y < top_y[idx_num]) and (gram.p1.x < midpoint < gram.p3.x):
                tops[idx_num] = gram.p1.y*scale

        likelist_ls, max_density = self.calculate_alignment(samples_ls=tops, scale=scale, plot="top")
        self.top_pixel_align = min(likelist_ls)
        return self.top_pixel_align, max_density

    def get_bot_alignment(self, scale=1.0):
        right_margin = self.right_pixel_align
        left_margin = self.left_pixel_align

        midpoint = left_margin + (right_margin-left_margin)/2.0
        num_pages = max(self.meta_list)
        bots = [-1]*num_pages
        size_min = midpoint
        for i in range(len(self.list)):
            idx_num = self.meta_list[i]-1
            gram = self.list[i]
            scaled_y = gram.p3.y*scale
            if (scaled_y > bots[idx_num]) and (gram.p1.x < midpoint < gram.p3.x) and (gram.get_width() > size_min): 
                bots[idx_num] = scaled_y

        likelist_ls, max_density = self.calculate_alignment(samples_ls=bots, scale=scale, plot="bot")
        self.bot_pixel_align = max(likelist_ls)
        return self.bot_pixel_align, max_density
