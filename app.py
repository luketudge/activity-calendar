import random

import pandas
import plotnine
import streamlit


BACKGROUND_FILL = 'black'
COLOR_PALETTE = 'YlGn'

WEEKDAYS = [
    'Sat',
    'Fri',
    'Thu',
    'Wed',
    'Tue',
    'Mon',
    'Sun'
]

WEEKDAYS_DISPLAYED = [
    'Mon',
    'Wed',
    'Fri',
]


def days_to_counts(days):
    """Convert iterable of integer day numbers to counts of weekday and week.
    
    argument days: iterable of int
    
    returns: pandas.DataFrame with columns:
        week: int
        weekday: pandas.Categorical
        count: int
    """

    counts = pandas.DataFrame({
        'week': [d // 7 for d in days],
        'weekday': pandas.Categorical(
            [WEEKDAYS[d % 7] for d in days],
            categories=WEEKDAYS,
            ordered=True
        )
    })

    counts = counts[['week', 'weekday']].value_counts().reset_index(name='count')

    return counts


streamlit.title('example calendar display')

seed = streamlit.sidebar.number_input(
    'random seed',
    min_value=0
)

random.seed(seed)

n = streamlit.sidebar.number_input(
    'number of hits',
    min_value=2,
    value=28
)

tile_size = streamlit.sidebar.slider(
    'size of tiles',
    min_value=0.1,
    max_value=1.0,
    value=0.9
)

data = days_to_counts(random.choices(range(365), k=n))

streamlit.markdown('''
uses plotnine to produce a very basic imitation of GitHub's activity calendar
''')

tile_style = plotnine.aes(
    width=tile_size,
    height=tile_size
)

fig = (
    plotnine.ggplot(data)
    + plotnine.aes(
        x='week',
        y='weekday',
        fill='factor(count)'
    )
    + plotnine.theme_void()
    + plotnine.theme(
        axis_text_y=plotnine.element_text()
    )
    + plotnine.coord_fixed()
    + plotnine.scale_y_discrete(
        breaks=WEEKDAYS_DISPLAYED
    )
    + plotnine.scale_fill_brewer(
        palette=COLOR_PALETTE,
        direction=-1
    )
    + plotnine.geom_tile(
        mapping=tile_style,
        data=days_to_counts(range(365)),
        fill=BACKGROUND_FILL,
        show_legend=False
    )
    + plotnine.geom_tile(
        mapping=tile_style,
        show_legend=False
    )
)

streamlit.pyplot(fig.draw())
