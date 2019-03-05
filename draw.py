import matplotlib
# Make MacOSX-compatible by specifying backend. 
# If on Windows, this import statement can be removed
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Draw():
    @staticmethod
    def get_box_coordinates(box):
        x_coords = [box.p1.x, box.p2.x, box.p3.x, box.p4.x, box.p1.x]
        y_coords = [box.p1.y, box.p2.y, box.p3.y, box.p4.y, box.p1.y]
        return x_coords, y_coords
        
    @staticmethod
    def show(gram_ls, title="Bounding Boxes"):
        # Set chart title.
        plt.title(title, fontsize=19)

        # Set x axis label.
        plt.xlabel("x-coordinates", fontsize=10)

        # Set y axis label.
        plt.ylabel("y-coordinates", fontsize=10)

        # Set size of tick labels.
        plt.tick_params(axis='both', which='major', labelsize=9)

        # plot
        for gram in gram_ls:
            x_ls, y_ls = Draw().get_box_coordinates(gram)
            # flip over x-axis to accomodate pixel origin being different
            # from graphing origin
            y_ls = [y*-1 for y in y_ls]
            plt.plot(x_ls, y_ls, linewidth=3)

        # Display the plot in the matplotlib's viewer.
        plt.show()

