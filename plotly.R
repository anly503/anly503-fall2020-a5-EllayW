library(plotly)
library(dplyr)
library(tidyr)
df <- read.csv('plot-data.csv')

fig <-plot_ly(data = df, x = ~Month, 
               y = ~consumption,
               showlegend=FALSE,
                marker=list(color=~Month, showscale=FALSE),
                text = df$consumption,
                hoverinfo = 'text',
                mode = 'markers',
                transforms = list(
                  list(
                    type = 'filter',
                    target = 'house',
                    operation = '=',
                    value = 4
                  )
          )) 
fig <- fig %>% layout(showlegend=FALSE, 
                      paper_bgcolor = "rgb(240, 240, 240)", 
                      plot_bgcolor = "rgb(240, 240, 240)", 
                      title = "Monthly Consumption By Plot Type",
                      xaxis = list(side="right", showgrid=FALSE),
                      yaxis=list(showgrid=FALSE),
                      updatemenus = list(
                        list(
                          y = 1,
                          buttons = list(
                            
                            list(method = "restyle",
                                 args = list("type", "pie"),
                                 label = "Pie"),
                            
                            list(method = "restyle",
                                 args = list("type", "bar"),
                                 label = "Bar")))
                      ))

fig2 <- df %>% 
      tidyr::pivot_longer(c(house, Weekday, Month)) %>% 
      plot_ly(df, x = ~Weekday,
              y = ~consumption,
              color = ~appliance, 
              colors = "Accent")
fig2