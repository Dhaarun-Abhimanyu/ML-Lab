import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

g = sns.FacetGrid(tips, col="day", col_wrap=2, height=4)
g.map(sns.kdeplot, "total_bill", fill=True, color="teal")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("KDE of Total Bill per Day")
plt.show()
