#from AnyQt.QtCore import Qt
from AnyQt.QtGui import QImage, QPixmap, QPalette
from AnyQt.QtCore import QSize, Qt, QSettings
from Orange.data import Table
#from Orange.data import Domain, StringVariable, ContinuousVariable
from Orange.widgets import gui, settings
from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.widgetpreview import WidgetPreview
from orangecontrib.imageanalytics.widgets.utils.imagepreview import Preview
#from AnyQt.QtWidgets import (QSizePolicy, QGraphicsWidget)
from orangewidget.widget import Input
#from orangewidget.widget import Output
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

debug = None

class OWFactorAnalysisViewer(OWWidget):
    name = "Factor Analysis Viewer"
    description = "Performs and views factor analysis"
    icon = "icons/factor-analysis-viewer.svg"
    priority = 130
    keywords = "factoranalysis"

    class Inputs:
        data = Input("Data", Table)
        
    #class Outputs:
    #    data = Output("Data", Table)
        
    settingsHandler = settings.DomainContextHandler()
    n_components: int = settings.ContextSetting(2)
    auto_commit: bool = settings.ContextSetting(True)
    
    def __init__(self):
        self.dataset = None
        self.layout_control_area()
        self.layout_main_area()
        
    def layout_main_area(self):
        #self.box = gui.vBox(self.mainArea, True, margin=5)
        layout = self.mainArea.layout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        self.preview = Preview(self.mainArea)
        self.preview.setMinimumSize(800, 600)
        #self.layout().addWidget(self.preview)
        
    def layout_control_area(self):
        layout = self.controlArea.layout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)

        self.spin = gui.spin(self.controlArea, self, "n_components", 1, 100,
                 label="Number of components",
                 callback=self.on_components_changed
        )
        
        gui.auto_send(self.buttonsArea, self, "auto_commit")
        
    def on_components_changed(self):
        self.n_components = self.spin.value()
        self.updateGraph()
        
    def sizeHint(self):
        return QSize(800, 600)
    
    def _getCurrentPalette(self) -> QPalette:
        from orangecanvas import styles
        settings = QSettings()
        stylesheet = settings.value("stylesheet", "", type=str)
        styles.style_sheet(stylesheet)
        
        theme = settings.value("palette", "", type=str)
        if theme and theme in styles.colorthemes:
            palette = styles.colorthemes[theme]()
        else:
            palette = QPalette()
        
        return palette
        
    def updateGraph(self):
        global debug
        if self.dataset is None:
            print("No dataset")
            return
        
        dataset = self.dataset
        
        X = StandardScaler().fit_transform(dataset.X)
        feature_names = list(dataset.domain.attributes)
        
        n_comps = self.n_components

        methods = [
            ("PCA", PCA()),
            ("Unrotated FA", FactorAnalysis()),
            ("Varimax FA", FactorAnalysis(rotation="varimax")),
        ]
        fig, axes = plt.subplots(ncols=len(methods), figsize=(10, 8), sharey=True)
        fontcolor = 'black'
        labels = [f"Comp. {x+1}" for x in range(n_comps)]
        #labelvars = [ ContinuousVariable(x) for x in labels]
        #domain = Domain(labelvars, metas=[StringVariable('Method')])
        #data = []
        for ax, (method, fa) in zip(axes, methods):
            fa.set_params(n_components=n_comps)
            fa.fit(X)
        
            components = fa.components_.T
            #row = components.tolist()+[method]
            #data.append(row)
        
            vmax = np.abs(components).max()
            colormap = "RdBu_r"
            ax.imshow(components, cmap=colormap, vmax=vmax, vmin=-vmax)
            ax.set_yticks(np.arange(len(feature_names)))
            ax.set_yticklabels(feature_names, fontsize=12, color=fontcolor)
            ax.set_title(str(method), fontsize=18, color=fontcolor)
            
            ticks = [x for x in range(n_comps)]
            ax.set_xticks(ticks)
            
            ax.set_xticklabels(labels, fontsize=10, color=fontcolor)
            transparent = (0, 0, 0, 0)
            fig.patch.set_facecolor(transparent)
            debug = fig.patch
            
        #self.Outputs.data.send(Table.from_list(domain, data))
        fig.suptitle("Factors", fontsize=20)
        
        fig = ax.get_figure()
        canvas = fig.canvas
        canvas.draw()
        plt.close()
        
        width, height = canvas.get_width_height()
        qformat = QImage.Format_ARGB32
        buffer = canvas.buffer_rgba()
        im = QImage(buffer, width, height, qformat)
        im = im.scaledToWidth(width*2, Qt.TransformationMode.SmoothTransformation)
        pm = QPixmap(im)
        pm = pm.scaledToWidth(width*2)
        self.preview.setPixmap(pm)
        self.layout().update()
        
    @Inputs.data
    def set_data(self, dataset: Table):
        self.dataset = dataset
        self.features_num = len(dataset.domain.attributes)
        self.spin.setMaximum(self.features_num)
        self.updateGraph()
        
    @gui.deferred
    def commit(self):
        pass

if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWFactorAnalysisViewer).run(Table("iris"))
