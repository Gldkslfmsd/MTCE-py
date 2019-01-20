from jchart import Chart
from jchart.config import Axes
from .evaluators import METRICS_RANGES

from jchart.config import Axes, DataSet, rgba, Title

colors = [
    rgba(255, 99, 132, 0.8),
    rgba(54, 162, 235, 0.8),
    rgba(255, 206, 86, 1),
    rgba(75, 192, 192, 1),
    rgba(153, 102, 255, 1),
    rgba(255, 159, 64, 1)
]

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

def pallete():
    while True:
        for c in colors:
            yield c

class MetricBarChart(Chart):
    chart_type = 'bar'
    responsive = True

    def __init__(self, metric, dataset):


        #self.title = Title(display=True,text=metric,fontSize=15)

        mtsystem = [a for a,_,_ in dataset]


        checkpoint = sorted(list(set([b.name for _,b,_ in dataset])))

        data = { s:[None for _ in checkpoint] for s in mtsystem }

        for s,ch,d in dataset:
            data[s][checkpoint.index(ch.name)] = d

        self.datasets = [DataSet(label=s.name,data=data[s],backgroundColor=c) for s,c in zip(mtsystem,pallete()) ]
        self.labels = checkpoint

        self.title = metric



        min, max = METRICS_RANGES[metric]
        self.scales = {
            'yAxes': [{"display": True, "ticks": {"min": min, "max": max}}]
        }

        super().__init__()

    def get_datasets(self, **kwargs):
        return self.datasets

    def get_labels(self, *args, **kwargs):
        return self.labels




class SentLevelDiffChart(Chart):
    chart_type = 'line'
    responsive = True


    def __init__(self, diffs, metric, A, B):

        self.title = "Sentence-level %s differences" % metric

        negative = [d for d in diffs if d < 0]
        same = [d for d in diffs if d == 0]
        positive = [d for d in diffs if d > 0]

#        self.datasets = [DataSet(type="line",label="sdfsfds",data={"x":list(range(len(negative))), "y":negative})]

        neg_data = [{'y': v, 'x': i} for i,v in enumerate(negative)]
        same_data = [{'y': v, 'x': i+len(negative)} for i,v in enumerate(same)]
        pos_data = [{'y': v, 'x': i+len(negative)+len(same)} for i,v in enumerate(positive)]

        self.datasets = [DataSet(
                type='line',
                label='%s worse than %s' % (A,B),
                data=neg_data,
                color=RED,
            ),
        ]
        if len(same_data) > 0:
            self.datasets.append(
                DataSet(
                    type='line',
                    label='%s equal to %s' % (A,B),
                    data=same_data,
                    color=BLACK,
                )
            )
        self.datasets.append(
            DataSet(
                type='line',
                label='%s better than %s' % (A,B),
                data=pos_data,
                color=GREEN,
            )
        )

        self.scales = {
            'xAxes': [Axes(type='linear', position='bottom', ticks={"min":0, "max": len(diffs)})],
            'yAxes': [{"title":metric}]
        }

        super().__init__()


    def get_datasets(self, *args, **kwargs):
        return self.datasets


from jchart import Chart

class PriceChart(Chart):
    chart_type = 'line'

  #  scales = {
  #      'xAxes': [{"display": True, "ticks": {"min": 0, "max": 100}}]
  #  }


    def get_datasets(self, *a, **kw):

        data = [{'x': str(i), 'y': i} for i in range(100)]

        return [DataSet(type="line",data=data)]

   # def get_labels(self, *a, **kw):
   #     return "sdfsdf sf sf dsf sf sf sdf sdf sfdsf sfdsfds".split()


class RadarChart(Chart):
    chart_type = 'radar'

    def get_labels(self):
        return ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"]

    def get_datasets(self, **kwargs):
        return [DataSet(label="My First dataset",
                        color=(179, 181, 198),
                        data=[65, 59, 90, 81, 56, 55, 40]),
                DataSet(label="My Second dataset",
                        color=(255, 99, 132),
                        data=[28, 48, 40, 19, 96, 27, 100])
]

class _MetricBarChart(Chart):
    chart_type = 'bar'
    scales = {
        'yAxes': [{"display": True, "ticks": {"min": 0, "max": 100}}]
    }

    def __init__(self, *a, **kw):
        super().__init__()
        pass

    def get_datasets(self, **kwargs):
        data = [10, None, 29, 30, 5, 10, 22]


        d = DataSet(label='Bar Chart',
                        data=data,
                        borderWidth=1,
                        backgroundColor=colors,
borderColor=colors)


        print(d)

        return [d]*3

    def get_labels(self, **kwargs):
        return ["checkpoint1", "checkpoint2", "March", "April",
                    "May", "June", ]


"""
from jchart import Chart

class LineChart(Chart):
    chart_type = 'line'
    responsive = True
    scales = {
        'xAxes': [Axes(display=False)],
    }

    def get_datasets(self, **kwargs):
        return [{
            'label': "My Dataset",
            'data': [69, 30, 45, 60, 55]
        }]
"""




class TimeSeriesChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='linear', position='bottom')],
    }

    def get_datasets(self, *args, **kwargs):
#        data = [{'y': 0, 'x': '2017-01-02T00:00:00'},
#                {'y': 1, 'x': '2017-01-03T00:00:00'},
#                {'y': 4, 'x': '2017-01-04T00:00:00'}, {'y': 9, 'x': '2017-01-05T00:00:00'}, {'y': 16, 'x': '2017-01-06T00:00:00'}, {'y': 25, 'x': '2017-01-07T00:00:00'}, {'y': 36, 'x': '2017-01-08T00:00:00'}, {'y': 49, 'x': '2017-01-09T00:00:00'}, {'y': 64, 'x': '2017-01-10T00:00:00'}, {'y': 81, 'x': '2017-01-11T00:00:00'}, {'y': 100, 'x': '2017-01-12T00:00:00'}, {'y': 121, 'x': '2017-01-13T00:00:00'}, {'y': 144, 'x': '2017-01-14T00:00:00'}, {'y': 169, 'x': '2017-01-15T00:00:00'}, {'y': 196, 'x': '2017-01-16T00:00:00'}, {'y': 225, 'x': '2017-01-17T00:00:00'}, {'y': 256, 'x': '2017-01-18T00:00:00'}, {'y': 289, 'x': '2017-01-19T00:00:00'}, {'y': 324, 'x': '2017-01-20T00:00:00'}, {'y': 361, 'x': '2017-01-21T00:00:00'}, {'y': 400, 'x': '2017-01-22T00:00:00'}, {'y': 441, 'x': '2017-01-23T00:00:00'}, {'y': 484, 'x': '2017-01-24T00:00:00'}, {'y': 529, 'x': '2017-01-25T00:00:00'}, {'y': 576, 'x': '2017-01-26T00:00:00'}, {'y': 625, 'x': '2017-01-27T00:00:00'}, {'y': 676, 'x': '2017-01-28T00:00:00'}, {'y': 729, 'x': '2017-01-29T00:00:00'}, {'y': 784, 'x': '2017-01-30T00:00:00'}, {'y': 841, 'x': '2017-01-31T00:00:00'}, {'y': 900, 'x': '2017-02-01T00:00:00'}]
        data = [{'y':i, 'x':i} for i in range(3330)]

        return [DataSet(
            type='line',
            label='Time Series',
            data=data,
        )]
