from IPython import display
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.ion()

def plot(foxes, mean_foxes):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Foxes data')
    plt.xlabel('Day')
    plt.ylabel('Population')
    plt.plot(foxes, label='Current amount of foxes')
    plt.plot(mean_foxes, label='Mean amount of foxes')
    plt.ylim(ymin=0)
    plt.text(len(foxes)-1, foxes[-1], str(foxes[-1]))
    plt.text(len(mean_foxes)-1, mean_foxes[-1], str(mean_foxes[-1]))
    plt.legend()
    plt.savefig('foxes_graph.png')

    plt.show(block=False)
    plt.pause(.1)

#NOTE: you need to download tkinter separately
# sudo apt-get install python3-tk