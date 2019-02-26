import matplotlib.pyplot as plt

from src.parallelogram import *

def Draw():
    @staticmethod
    def get_box_coordinates(box: Parallelogram):
        x_coords = [box.p1.x, box.p2.x, box.p3.x, box.p4.x, box.p1.x]
        y_coords = [box.p1.y, box.p2.y, box.p3.y, box.p4.y, box.p1.y]
        return x_coords, y_coords
        
    @staticmethod
    def show():
        # Set chart title.
        plt.title("Bounding Boxes", fontsize=19)

        # Set x axis label.
        plt.xlabel("x-coordinates", fontsize=10)

        # Set y axis label.
        plt.ylabel("y-coordinates", fontsize=10)

        # Set size of tick labels.
        plt.tick_params(axis='both', which='major', labelsize=9)

        # Display the plot in the matplotlib's viewer.
        plt.show()

if __name__ == '__main__':
    points = [Point(0, 0), Point(5,10)]
    print(points[0] + points[1])
    # Parallelogram(points)
    #################################
    # p1 = Point(0, 0)
    # p2 = Point(5, 5)
    # p3 = Point(6, 10)

    # boxes = [(p1, p2, None), (p1, p3, "black")]
    # for box in boxes:
    #     x_coords, y_coords = BoundingBox(box[0], box[1]).get_box_coordinates()
    #     # Plot the number in the list and set the line thickness.
    #     plt.plot(x_coords, y_coords, linewidth=3, color=box[2])
    
    # draw()

