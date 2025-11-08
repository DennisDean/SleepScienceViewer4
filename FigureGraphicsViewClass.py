# Custom Graphic View for Sleep Science Viewer
# Provides support for right-clicking on figures
#

# Import modules
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGraphicsView,
    QGraphicsScene,
    QLineEdit,
    QMenu,
    QMessageBox,
    QSizePolicy,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtGui import QImage, QGuiApplication, QPixmap
import matplotlib.pyplot as plt
import copy
import io

# Extend Existing Class
class FigureGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.figure = None
        self.canvas_item = None
    # --- Optional if you embed figures dynamically ---
    def set_figure(self, figure):
        if self.canvas_item:
            self.scene.removeItem(self.canvas_item)
        self.figure = figure
        canvas = FigureCanvas(figure)
        self.scene.addWidget(canvas)
        canvas.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.fixed)
        canvas.updateGeometry()
        self.canvas_item = canvas

    # --- Right-click context menu ---
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        save_action = menu.addAction("Save Figure...")
        menu.addSeparator()
        menu.addAction("Cancel")

        action = menu.exec(event.globalPos())

        if action == save_action:
            self.open_save_dialog()

    # --- Save dialog ---
    def open_save_dialog(self):
        if self.figure is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Save Figure")
        layout = QFormLayout(dialog)

        # --- Figure Dimensions ---
        width_spin = QDoubleSpinBox()
        width_spin.setRange(1.0, 50.0)
        width_spin.setValue(self.figure.get_size_inches()[0])
        layout.addRow("Width (inches):", width_spin)

        height_spin = QDoubleSpinBox()
        height_spin.setRange(1.0, 50.0)
        height_spin.setValue(self.figure.get_size_inches()[1])
        layout.addRow("Height (inches):", height_spin)

        dpi_spin = QDoubleSpinBox()
        dpi_spin.setRange(72, 600)
        dpi_spin.setValue(self.figure.dpi)
        layout.addRow("DPI:", dpi_spin)

        # --- Font Controls ---
        xlabel_font_spin = QDoubleSpinBox()
        xlabel_font_spin.setRange(4, 40)
        xlabel_font_spin.setValue(10)
        layout.addRow("X Label Font Size:", xlabel_font_spin)

        ylabel_font_spin = QDoubleSpinBox()
        ylabel_font_spin.setRange(4, 40)
        ylabel_font_spin.setValue(10)
        layout.addRow("Y Label Font Size:", ylabel_font_spin)

        title_font_spin = QDoubleSpinBox()
        title_font_spin.setRange(6, 60)
        title_font_spin.setValue(14)
        layout.addRow("Title Font Size:", title_font_spin)

        # --- Title Text ---
        title_edit = QLineEdit()
        layout.addRow("Title:", title_edit)

        # --- Buttons ---
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        copy_button = buttons.addButton("Copy", QDialogButtonBox.ActionRole)
        layout.addWidget(buttons)

        # --- Helper to apply fonts ---
        def apply_fonts(ax):
            ax.xaxis.label.set_size(xlabel_font_spin.value())
            ax.yaxis.label.set_size(ylabel_font_spin.value())
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontsize(min(xlabel_font_spin.value(), ylabel_font_spin.value()))

        # --- Create a temporary copy of the figure ---
        def get_figure_copy():
            fig_copy = copy.deepcopy(self.figure)
            fig_copy.set_size_inches(width_spin.value(), height_spin.value())
            fig_copy.set_dpi(dpi_spin.value())
            fig_copy.set_layout_engine('constrained')

            if title_edit.text():
                fig_copy.suptitle(title_edit.text(), fontsize=title_font_spin.value())
            for ax in fig_copy.axes:
                apply_fonts(ax)
            return fig_copy

        # --- Save Handler ---
        def save_figure():
            file_name, _ = QFileDialog.getSaveFileName(
                dialog,
                "Save Figure",
                "",
                "PNG Files (*.png);;JPEG Files (*.jpg);;PDF Files (*.pdf)"
            )
            if not file_name:
                return

            fig_copy = get_figure_copy()
            fig_copy.savefig(file_name, dpi=dpi_spin.value(), bbox_inches="tight")
            QMessageBox.information(dialog, "Saved", f"Figure saved to:\n{file_name}")
            plt.close(fig_copy)  # clean up
            dialog.accept()

        # --- Copy Handler ---
        def copy_figure():
            fig_copy = get_figure_copy()
            buf = io.BytesIO()
            fig_copy.savefig(buf, format="png", dpi=dpi_spin.value(), bbox_inches="tight")
            qimage = QImage.fromData(buf.getvalue(), "PNG")
            QGuiApplication.clipboard().setPixmap(QPixmap.fromImage(qimage))
            plt.close(fig_copy)  # clean up
            QMessageBox.information(dialog, "Copied", "Figure copied to clipboard.")
            dialog.accept()

        # --- Connect Buttons ---
        buttons.accepted.connect(save_figure)
        buttons.rejected.connect(dialog.reject)
        copy_button.clicked.connect(copy_figure)

        dialog.exec()
    def show_context_menu(self, pos):
        menu = QMenu(self)
        save_action = menu.addAction("Save Figure…")
        menu.addSeparator()
        menu.addAction("Cancel")
        action = menu.exec(self.mapToGlobal(pos))
        if action == save_action:
            self.open_save_dialog()
    # --- Save file method ---
    def save_figure_to_file(self, width, height, dpi, xlabel_fontsize=None, ylabel_fontsize=None, title_text=None):
        print('Safe figure to file')
        if self.figure is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Figure", "figure.png",
            "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg)"
        )
        if not file_path:
            return

        axes = self.figure.get_axes()
        if not axes:
            print('no axes found')
            return

        # --- Save original properties ---
        original_size = self.figure.get_size_inches().copy()
        original_dpi = self.figure.dpi
        original_margins = {
            'left': self.figure.subplotpars.left,
            'right': self.figure.subplotpars.right,
            'top': self.figure.subplotpars.top,
            'bottom': self.figure.subplotpars.bottom,
        }
        oringinal_sup_title = self.figure.get_suptitle()
        print(oringinal_sup_title)
        print(original_margins)

        # --- Save font sizes and suptitle ---
        original_fontsizes = [
            {
                'xlabel': ax.xaxis.label.get_fontsize(),
                'ylabel': ax.yaxis.label.get_fontsize(),
                'title': ax.title.get_fontsize()
            } for ax in axes
        ]

        print('got figure axis and orignial parameters')
        try:
            print('tring to apply new features')
            # --- Apply new size and resolution ---
            self.figure.set_size_inches(width, height)
            self.figure.set_dpi(dpi)

            # --- Update axis label and tick font sizes ---
            for ax in axes:
                if xlabel_fontsize is not None:
                    ax.xaxis.label.set_fontsize(xlabel_fontsize)
                    ax.tick_params(axis='x', labelsize=xlabel_fontsize)
                if ylabel_fontsize is not None:
                    ax.yaxis.label.set_fontsize(ylabel_fontsize)
                    ax.tick_params(axis='y', labelsize=ylabel_fontsize)

            # --- Add or preserve title ---
            if title_text:
                fontsize_for_title = max(
                    f for f in [xlabel_fontsize, ylabel_fontsize] if f is not None
                ) if any([xlabel_fontsize, ylabel_fontsize]) else 12  # fallback

                for ax in axes:
                    ax.set_title(title_text, fontsize=fontsize_for_title, pad=10)
                else:
                    for ax in axes:
                        ax.set_title("double check code is called")


            # --- Save the figure ---
            self.figure.savefig(file_path, dpi=dpi, bbox_inches='tight')

        finally:
            print('entering finally')
            # --- Restore size, margins, and fonts ---
            self.figure.set_size_inches(original_size)
            self.figure.set_dpi(original_dpi)
            self.figure.subplots_adjust(**original_margins)

            for ax, fontsizes in zip(axes, original_fontsizes):
                ax.xaxis.label.set_fontsize(fontsizes['xlabel'])
                ax.yaxis.label.set_fontsize(fontsizes['ylabel'])
                ax.tick_params(axis='x', labelsize=fontsizes['xlabel'])
                ax.tick_params(axis='y', labelsize=fontsizes['ylabel'])

            # --- Restore suptitle ---

            for ax_f in axes:
                title_list.append(ax_f.get_title())


            if title_list:
                for (ax_f, title_f) in zip(axes,title_list) :
                    ax_f.set_title(title_f)
            elif has_suptitle:
                for (ax_f, title_f) in zip(axes, title_list):
                    ax_f.set_title('')

            # --- Redraw once at the end ---
            if self.canvas_item:
                self.canvas_item.draw()
            self.scene.update()
