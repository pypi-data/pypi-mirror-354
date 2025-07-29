import numpy as np

#from sklearn.decomposition import FactorAnalysis
from factor_analyzer import FactorAnalyzer

from AnyQt.QtCore import Qt, QRectF
from AnyQt.QtGui import QColor, QBrush, QStandardItemModel, QStandardItem
from AnyQt.QtWidgets import QTableView, QSizePolicy, QGridLayout,QHeaderView

from Orange.data import Table, Domain, DiscreteVariable, ContinuousVariable
from Orange.data.util import get_unique_names
from Orange.widgets import settings
from Orange.widgets.widget import OWWidget
from orangewidget.widget import Input, Output
from orangewidget.utils.widgetpreview import WidgetPreview
from orangewidget.utils.itemmodels import PyListModel
from Orange.widgets.utils.itemmodels import DomainModel
from Orange.widgets.utils.slidergraph import SliderGraph
from orangewidget import gui
import plotly.express as px

from pyqtgraph import mkPen, TextItem
BorderRole = next(gui.OrangeUserRole)

# user selects type of rotation.
class Rotation:
    NoRotation, Varimax, Promax, Oblimin, Oblimax, Quartimin, Quartimax, Equamax = 0, 1, 2, 3, 4, 5, 6, 7

    @staticmethod
    def items():
        return ["NoRotation", "Varimax", "Promax", "Oblimin", "Oblimax", "Quartimin", "Quartimax", "Equamax"]

class OWFactorAnalysis(OWWidget):
    name = "Factor Analysis"
    description = "Randomly selects a subset of instances from the dataset."
    icon = "icons/factor-analysis.svg"
    priority = 20

    want_control_area = False

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        sample = Output("Sampled Data", Table)

    n_components = settings.ContextSetting(2)
    rotation = settings.Setting(Rotation.NoRotation)
    x_axis_setting = 1
    y_axis_setting = 1
    autocommit = settings.Setting(True)
    
    def __init__(self):
        self.dataset = None     # this contains the input dataset.
        self.attributes = []    # this contains the list of attribute (variable) names.
        self.fa_loadings = None # this contains factorial values after rotation was applied.
        self.eigen_values = None
        self.components_accumulation = [1]
        self.communalities = None
        self.layout_main_area()

    def layout_main_area(self):
        # Main area settings
        self.attr_box = gui.hBox(self.mainArea, margin=0)
        
        self.n_components_spin = gui.spin(
            self.attr_box, self, "n_components", label="Number of components:",
            minv=1, maxv=100, step=1, controlWidth=30,
            callback=self.n_components_changed,
        )
        self.n_components_spin.setValue(self.n_components)

        gui.comboBox(
            self.attr_box, self, "rotation", label="Rotation:", labelWidth=50,
            items=Rotation.items(), orientation=Qt.Horizontal, 
            contentsLength=12, callback=self.n_components_changed
        )

        gui.auto_commit(
            self.attr_box, self, 'autocommit', 'Commit',
            orientation=Qt.Horizontal
        )

        gui.separator(self.mainArea)

        # Table
        box = gui.vBox(self.mainArea, box = "Factor Loadings")
        self.tablemodel = QStandardItemModel(self)
        view = self.tableview = QTableView(
            editTriggers=QTableView.NoEditTriggers)
        view.setModel(self.tablemodel)
        view.horizontalHeader()
        view.horizontalHeader().setMinimumSectionSize(40)
        view.setShowGrid(True)
        view.setSizePolicy(QSizePolicy.MinimumExpanding,
                           QSizePolicy.MinimumExpanding)
        box.layout().addWidget(view)

        gui.separator(self.mainArea)

        self.axis_box = gui.hBox(self.mainArea, box = "Graph Settings")
        self.axis_value_model_x = PyListModel(iterable=[self.x_axis_setting])
        x_axis = gui.comboBox(
            self.axis_box, self, "x_axis_setting", label="X-axis:", labelWidth=50,
            model=self.axis_value_model_x, orientation=Qt.Horizontal,
            contentsLength=5, callback=self.axis_graph_settings
        )

        self.axis_value_model_y = PyListModel(iterable=[self.y_axis_setting])
        y_axis = gui.comboBox(
            self.axis_box, self, "y_axis_setting", label="Y-axis:", labelWidth=50,
            model=self.axis_value_model_y, orientation=Qt.Horizontal,
            contentsLength=5, callback=self.axis_graph_settings
        )

        # Graph
        self.plot = SliderGraph("", "", lambda x: None)
        self.mainArea.layout().addWidget(self.plot)


    def n_components_changed(self):
        self.components_accumulation.append(self.n_components)
        self.factor_analysis()
        self.axis_graph_settings()
        self.commit.deferred()

    # cleaning values in table after n_components was changed to a smaller value.
    def clear_table(self):
        if len(self.components_accumulation) < 2:
            return

        prev_n_components = self.components_accumulation[-2]
        for i in range(prev_n_components):
            for j in range(1 + len(self.fa_loadings.X[0])):     #1 column for eigen + number of variables.
                self.insert_item(i, j, "")

        self.tablemodel.removeRows(self.n_components, prev_n_components - self.n_components)

    @Inputs.data
    def set_data(self, dataset):
        self.dataset = dataset
        # extract list of attribute (variables) names from the self.dataset.domain.attributes.
        self.attributes = []
        for j in range(len(self.dataset.domain.attributes)):
            self.attributes.append(self.dataset.domain.attributes[j].name)
        self.n_components_spin.setMaximum(len(self.dataset.domain.attributes))
        self.n_components_changed()
        self.commit.now()

    # insert item into row i and column j of the table
    def insert_item(self, i, j, val):
        item = QStandardItem()
        bkcolor = QColor.fromHsl([0, 240][i == j], 160, 255)
        item.setData(QBrush(bkcolor), Qt.BackgroundRole)
        # bkcolor is light-ish so use a black text
        item.setData(QBrush(Qt.black), Qt.ForegroundRole)
        item.setData("trbl", BorderRole)
        # item.setToolTip("actual: {}\npredicted: {}".format(
        # self.headers[i], self.headers[j]))
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        if type(val) != str:
            val = str(round(val, 2))

        item.setData(val, Qt.DisplayRole)          # set our val into item
        self.tablemodel.setItem(i, j, item)


    # set up the table which will be shown in the Main Area.
    def insert_table(self):
        # insert attribute (variable) names into horizontal header.
        hheader_labels = ["eigenvalue",]
        for att in self.attributes:
            hheader_labels.append(att)
        self.tablemodel.setHorizontalHeaderLabels(hheader_labels)

        # insert factor names into vertical header.
        vheader_labels = ["communalities",]
        for i in range(self.n_components):
            vheader_labels.append(f"F{i + 1}")
        self.tablemodel.setVerticalHeaderLabels(vheader_labels)

        self.clear_table()
        # insert eigen values.
        for factor in range(len(self.fa_loadings.X)):
            eigen = self.eigen_values[factor]
            self.insert_item(factor + 1, 0, eigen)

        # insert communalities in the first row.
        for j in range(len(self.fa_loadings.X[0])):
            val = self.communalities[j]
            self.insert_item(0, j + 1, val)

        # insert values into the table.
        for i in range(len(self.fa_loadings.X)):         #i = rows = factors
            for j in range(len(self.fa_loadings.X[0])):  #j = columns = variables
                val = self.fa_loadings.X[i][j]           #from i-row and j-column we had a specific variable value
                self.insert_item(i + 1, j + 1, val)      #insert into columns from 1 onwards, because of the first eigen row

    def axis_graph_settings(self):
        if self.n_components < 2:
            return

        x_axis_list = [self.x_axis_setting]
        for i in range(1, self.n_components + 1):
            if i != self.x_axis_setting:
                x_axis_list.append(i)

        self.axis_value_model_x[:] = x_axis_list

        y_axis_list = [self.y_axis_setting]
        for i in range(1, self.n_components + 1):
            if i != self.y_axis_setting:
                y_axis_list.append(i)

        self.axis_value_model_y[:] = y_axis_list

        # reset when max value of axis setting exceeds n_components.
        if  max(self.x_axis_setting, self.y_axis_setting) >= self.n_components + 1:
            return

        self.setup_plot()

    def draw_arrowhead(self, x, y, color, arrow_angle_deg = 30, arrow_length_px = 20):
        # No arrowhead for 0-length vectors
        if x == 0 and y == 0:
            return

        scale_x = self.plot.viewRect().width() / self.plot.range.width()
        scale_y = self.plot.viewRect().height() / self.plot.range.height()
        theta_rad = np.radians(arrow_angle_deg / 2)
        
        # convert to pixel-size
        dx, dy = x / scale_x, y / scale_y
        length = np.hypot(dx, dy)
        ux, uy = dx / length, dy / length

        def rotate_and_scale(dx, dy, theta, arrow_len, scale_x, scale_y):
            cos_t, sin_t = np.cos(theta), np.sin(theta)
            rx = cos_t * dx - sin_t * dy
            ry = sin_t * dx + cos_t * dy
            return rx * arrow_len * scale_x, ry * arrow_len * scale_y

        # Rotate and scale both sides
        left_dx, left_dy = rotate_and_scale(-ux, -uy, +theta_rad, arrow_length_px, scale_x, scale_y)
        right_dx, right_dy = rotate_and_scale(-ux, -uy, -theta_rad, arrow_length_px, scale_x, scale_y)

        self.plot.plot([x, x + left_dx], [y, y + left_dy],
            pen=mkPen(color, width=1), antialias=True
        )
        self.plot.plot([x, x + right_dx], [y, y + right_dy],
            pen=mkPen(color, width=1), antialias=True
        )


    def setup_plot(self):
        self.plot.clear_plot()
        if self.dataset is None: return

        # i want the graph axis selection combo box to start from 1,
        # but i want factor 1 to correspond to first row in the table - row with index 0.
        self.factor1 = self.fa_loadings.X[self.x_axis_setting - 1]
        self.factor2 = self.fa_loadings.X[self.y_axis_setting - 1]

        # assign names to axis based on factors selected.
        axis = self.plot.getAxis("bottom")
        axis.setLabel(f"Factor {self.x_axis_setting}")
        axis = self.plot.getAxis("left")
        axis.setLabel(f"Factor {self.y_axis_setting}")

        # set the range.
        self.set_range_graph()

        foreground = self.plot.palette().text().color()
        foreground.setAlpha(128)

        palette = px.colors.qualitative.Plotly
        c_i = 0
        # draw the variable vectors and their names into the graph.
        for x, y, attr_name in zip(self.factor1, self.factor2, self.attributes):
            color = palette[c_i % len(palette)]
            c_i += 1

            x_vector, y_vector = [0, x], [0, y]
            self.plot.plot(x_vector, y_vector,
                pen=mkPen(color, width=1), antialias=True,
            )

            self.draw_arrowhead(x, y, color, 30)

            label = TextItem(text=attr_name, anchor=(0, 1), color=foreground)
            label.setPos(x_vector[-1], y_vector[-1])
            self.plot.x = x_vector
            self.plot._set_anchor(label, len(x_vector) - 1, True)
            self.plot.addItem(label)

        # --- Scatterplot of projected data points colored by class ---
        if self.dataset is not None and self.dataset.domain.has_discrete_class:
            class_var = self.dataset.domain.class_var
            class_vals = self.dataset.Y.astype(int)  # Assumes single discrete class
            n_classes = len(class_var.values)

            # Project data
            loadings_matrix = np.array([self.factor1, self.factor2]).T
            data_proj = self.dataset.X @ loadings_matrix
            data_proj = self.scale_data_proj(data_proj)

            for class_idx in range(n_classes):
                indices = np.where(class_vals == class_idx)[0]
                xs = data_proj[indices, 0]
                ys = data_proj[indices, 1]
                scatter = self.plot.plot(
                    xs, ys,
                    pen=None,
                    symbol='o',
                    symbolSize=6,
                    symbolBrush=palette[class_idx],
                    symbolPen=mkPen(None),
                    name=class_var.values[class_idx]
                )

    def scale_data_proj(self, data_proj: np.ndarray):
        min_x = np.min(data_proj[:, 0])
        max_x = np.max(data_proj[:, 0])
        min_y = np.min(data_proj[:, 1])
        max_y = np.max(data_proj[:, 1])
        range_x = max_x - min_x
        range_y = max_y - min_y
        if range_x == 0 or range_y == 0:
            return data_proj

        bbox = self.plot.viewRect()
        scale_x = bbox.width() / range_x
        scale_y = bbox.height() / range_y
        offset_x = min_x * scale_x - bbox.x()
        offset_y = min_y * scale_y - bbox.y()

        out_proj = data_proj.copy()
        out_proj[:, 0] = out_proj[:, 0] * scale_x - offset_x
        out_proj[:, 1] = out_proj[:, 1] * scale_y - offset_y
        return out_proj

    def set_range_graph(self):
        factor1_range = np.max(1.1 * np.abs(self.factor1))  # function to remember > the largest abs value * 1.1 of factor
        factor2_range = np.max(1.1 * np.abs(self.factor2))
        self.plot.setRange(xRange=(-factor1_range, factor1_range), yRange=(-factor2_range, factor2_range))

    # def factor_analysis_new(self):
    #     # with chosen n_components and depending on the user-selected rotation, calculate the FA on self.dataset.
    #     rotation = [None, "Varimax", "Promax", "Oblimin", "Oblimax", "Quartimin", "Quartimax", "Equamax"][self.rotation]
    #     if rotation is not None: rotation = rotation.lower()
    #     fa = FactorAnalysis(rotation=rotation, n_components=self.n_components, tol=0.0)
    #     fa.fit(self.dataset.X)

    #     # transform loadings correct format.
    #     loadings = fa.components_.T
    #     self.communalities = np.sum(loadings ** 2, axis=1)

    #     # from result variable (instance of FactorAnalyzer class) get the eigenvalues.
    #     X_std = (self.dataset.X - np.mean(self.dataset.X, axis=0)) / np.std(self.dataset.X, axis=0)
    #     corr = np.corrcoef(X_std, rowvar=False)
    #     eigen_vals, _ = np.linalg.eigh(corr)
    #     self.eigen_values = np.flip(np.sort(eigen_vals))

    #     # transform the table back to Orange.data.Table.
    #     self.fa_loadings = Table.from_numpy(Domain(self.dataset.domain.attributes), loadings.T)

    def factor_analysis(self):
        if self.dataset is None: return
        # with chosen n_components and depending on the user-selected rotation, calculate the FA on self.dataset.
        rotation = [None, "Varimax", "Promax", "Oblimin", "Oblimax", "Quartimin", "Quartimax", "Equamax"][self.rotation]
        fa = FactorAnalyzer(rotation=rotation, n_factors=self.n_components)
        fa.fit(self.dataset.X)

        # transform loadings correct format.
        loadings = []
        for i in range(self.n_components):
            row = []
            for x in fa.loadings_:
                row.append(x[i])
            loadings.append(row)

        self.communalities = fa.get_communalities()

        # from result variable (instance of FactorAnalyzer class) get the eigenvalues.
        self.eigen_values = fa.get_eigenvalues()
        self.eigen_values = self.eigen_values[0]
    
       # transform the table back to Orange.data.Table.
        self.fa_loadings = Table.from_numpy(Domain(self.dataset.domain.attributes), loadings)

    @gui.deferred
    def commit(self):
        if self.dataset is None:
            self.Outputs.sample.send(None)
        else:
            self.factor_analysis()
            # send self.fa_loadings in Outputs channel
            self.Outputs.sample.send(self.fa_loadings)
            self.insert_table()

if __name__ == "__main__":
    from orangecontrib.factoranalysis.widgets.darkmode import apply_dark_theme
    WidgetPreview(OWFactorAnalysis).run(Table("iris"))
