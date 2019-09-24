# BokehProject1
A project about interactive graphics and html in python with bokeh and flask. I created this project in a hackaton for another purpose (in a axial compresor, study the different correlations in each row for the deviation and losses) but I do not have the difussion rights for that project. That's why I uploaded it applied to another dataset, the Airbnb in NYC.

I found this tool useful when you have to compare numerical results in different scenarios (with a relationship between them) and you have to look for a correlation with its behaviour. It provides an interative tool to check very quickly different plots.

## Options
Given an excel:
- The x and y to plot can be choosen
- It can filter by one row
- If there is any identifier that relates the different plots, clicking in some points will show where are those points at in the other plots
- The plots are saved as html files so, they can be stored and opened later / sent by email

# Example
The right menu selects the filter, in this case it is applied on the appartment type.

Then, the x and y parameters to plot can be chose

In this case, the longitude and latitude have been represented.

Finally, several plots have been plotted. Thanks to the tools implemented in bokeh we can check what happen with the points that are not in the city centre for example. So if we select them from the longitude and latitude plot, they will be highlighted in the other plots. So we can see that there is no difference between the appartments that are far from the city centre. Their price is around 150$ but they are as rented as the others.
