from jchart import Chart
from jchart.config import Axes

from jchart.config import Axes, DataSet, rgba, Title

colors = [
    rgba(255, 99, 132, 0.8),
    rgba(54, 162, 235, 0.8),
    rgba(255, 206, 86, 1),
    rgba(75, 192, 192, 1),
    rgba(153, 102, 255, 1),
    rgba(255, 159, 64, 1)
]

def pallete():
    while True:
        for c in colors:
            yield c

class MetricBarChart(Chart):
    chart_type = 'bar'
    responsive = True

    def get_maximum(self, metric):
        if metric in ["brevity_penalty"]:
            return 1
        else:
            return 100


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



        self.scales = {
            'yAxes': [{"display": True, "ticks": {"min": 0, "max": self.get_maximum(metric)}}]
        }

        super().__init__()

    def get_datasets(self, **kwargs):
        return self.datasets

    def get_labels(self, *args, **kwargs):
        return self.labels

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
