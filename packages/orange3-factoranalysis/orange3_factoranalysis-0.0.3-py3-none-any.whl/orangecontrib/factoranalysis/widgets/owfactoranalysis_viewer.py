import io
import matplotlib.pyplot as plt
import numpy as np
from AnyQt.QtCore import QSize, Qt
from Orange.data import Table
from Orange.widgets import gui, settings
from Orange.widgets.widget import OWWidget
from orangewidget.widget import Input
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler


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
        self.features_num = 0
        self.layout_control_area()
        self.layout_main_area()
        
    def layout_main_area(self):
        layout = self.mainArea.layout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        
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
            
    def updateGraph(self):
        if self.dataset is None:
            self.error("No input")
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
        fontcolor = self.palette().windowText().color().name()
        labels = [f"Comp. {x+1}" for x in range(n_comps)]
        ax = None
        for ax, (method, fa) in zip(axes, methods):
            fa.set_params(n_components=n_comps)
            fa.fit(X)
        
            components = fa.components_.T        
            vmax = np.abs(components).max()
            colormap = "RdBu_r"
            ax.imshow(components, cmap=colormap, vmax=vmax, vmin=-vmax)
            ax.set_yticks(np.arange(len(feature_names)))
            ax.set_yticklabels(feature_names, fontsize=16, color=fontcolor)
            ax.set_title(str(method), fontsize=20, color=fontcolor)
            
            ticks = [x for x in range(n_comps)]
            ax.set_xticks(ticks)
            
            ax.set_xticklabels(labels, fontsize=10, color=fontcolor)
            transparent = (0, 0, 0, 0)
            fig.patch.set_facecolor(transparent)
            
        fig.suptitle("Factors", fontsize=20, color=fontcolor)
        if ax is None:
            return
        fig = ax.get_figure()
        svg_io = io.StringIO()
        fig.savefig(svg_io, format='svg')
        svg_data = svg_io.getvalue()
        plt.close()
        self._show_svg(svg_data)

        canvas = fig.canvas
        canvas.draw()
        plt.close()
        
    def _show_svg(self, svg_str):
        palette = self.palette()
        bg_color = palette.window().color().name()
        fg_color = palette.windowText().color().name()

        # Wrap the SVG string in HTML
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: {bg_color};
                    color: {fg_color};
                }}
                svg {{
                    width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            {svg_str}
        </body>
        </html>
        """
        self.webview.setHtml(html)

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
    from orangewidget.utils.widgetpreview import WidgetPreview
    from orangecontrib.factoranalysis.widgets.darkmode import apply_dark_theme
    WidgetPreview(OWFactorAnalysisViewer).run(Table("iris"))
