# Custom Graphic View for Sleep Science Viewer
# Provides support for right-clicking on figures
#

# Import modules
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QMenu,
    QDialog,
    QFormLayout,
    QDoubleSpinBox,
    QDialogButtonBox,
    QFileDialog,
    QSizePolicy
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

        width_spin = QDoubleSpinBox()
        width_spin.setRange(1.0, 50.0)
        width_spin.setValue(self.figure.get_size_inches()[0])
        layout.addRow("Width (inches):", width_spin)

        height_spin = QDoubleSpinBox()
        height_spin.setRange(1.0, 50.0)
        height_spin.setValue(self.figure.get_size_inches()[1])
        layout.addRow("Height (inches):", height_spin)

        dpi_spin = QDoubleSpinBox()
        dpi_spin.setRange(50, 1200)
        dpi_spin.setValue(self.figure.dpi)
        layout.addRow("DPI:", dpi_spin)

        # Get current font sizes from the first axes
        axes = self.figure.get_axes()
        current_xlabel_size = 10  # default
        current_ylabel_size = 10  # default
        if axes:
            ax = axes[0]
            xlabel_obj = ax.xaxis.get_label()
            ylabel_obj = ax.yaxis.get_label()

            # Try to get font size, handle different return types
            try:
                current_xlabel_size = float(xlabel_obj.get_fontsize())
            except (TypeError, ValueError, AttributeError):
                current_xlabel_size = 10

            try:
                current_ylabel_size = float(ylabel_obj.get_fontsize())
            except (TypeError, ValueError, AttributeError):
                current_ylabel_size = 10

        # Font size controls
        xlabel_fontsize_spin = QDoubleSpinBox()
        xlabel_fontsize_spin.setRange(4, 72)
        xlabel_fontsize_spin.setValue(current_xlabel_size)
        layout.addRow("X-Label Font Size:", xlabel_fontsize_spin)

        ylabel_fontsize_spin = QDoubleSpinBox()
        ylabel_fontsize_spin.setRange(4, 72)
        ylabel_fontsize_spin.setValue(current_ylabel_size)
        layout.addRow("Y-Label Font Size:", ylabel_fontsize_spin)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.Accepted:
            width = width_spin.value()
            height = height_spin.value()
            dpi = dpi_spin.value()
            xlabel_fontsize = xlabel_fontsize_spin.value()
            ylabel_fontsize = ylabel_fontsize_spin.value()
            self.save_figure_to_file(width, height, dpi, xlabel_fontsize, ylabel_fontsize)
    def show_context_menu(self, pos):
        menu = QMenu(self)
        save_action = menu.addAction("Save Figure…")
        menu.addSeparator()
        menu.addAction("Cancel")
        action = menu.exec(self.mapToGlobal(pos))
        if action == save_action:
            self.open_save_dialog()
    # --- Save file method ---
    def save_figure_to_file(self, width, height, dpi, xlabel_fontsize=None, ylabel_fontsize=None):
        if self.figure is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Figure", "figure.png", "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg)"
        )
        if not file_path:
            return

        axes = self.figure.get_axes()

        # --- Save original state ---
        original_size = self.figure.get_size_inches().copy()
        original_dpi = self.figure.dpi

        # Save margins (subplots_adjust settings)
        original_margins = self.figure.subplotpars.__dict__.copy()

        # Save font sizes
        original_fontsizes = []
        for ax in axes:
            original_fontsizes.append({
                'xlabel': ax.xaxis.label.get_fontsize(),
                'ylabel': ax.yaxis.label.get_fontsize(),
                'title': ax.title.get_fontsize()
            })

        try:
            # --- Apply new settings ---
            self.figure.set_size_inches(width, height)
            self.figure.set_dpi(dpi)

            # Apply font sizes
            for ax in axes:
                if xlabel_fontsize is not None:
                    ax.xaxis.label.set_fontsize(xlabel_fontsize)
                    ax.tick_params(axis='x', labelsize=xlabel_fontsize)
                if ylabel_fontsize is not None:
                    ax.yaxis.label.set_fontsize(ylabel_fontsize)
                    ax.tick_params(axis='y', labelsize=ylabel_fontsize)

            # Prevent Matplotlib from auto-adjusting subplots when saving
            self.figure.subplots_adjust(
                left=original_margins['left'],
                right=original_margins['right'],
                top=original_margins['top'],
                bottom=original_margins['bottom']
            )

            self.figure.canvas.draw_idle()

            # Save the figure
            self.figure.savefig(file_path, dpi=dpi, bbox_inches='tight')

        finally:
            # --- Restore original figure state ---
            self.figure.set_size_inches(original_size)
            self.figure.set_dpi(original_dpi)

            # Restore margins exactly as before
            self.figure.subplots_adjust(
                left=original_margins['left'],
                right=original_margins['right'],
                top=original_margins['top'],
                bottom=original_margins['bottom']
            )

            for ax, fontsizes in zip(axes, original_fontsizes):
                ax.xaxis.label.set_fontsize(fontsizes['xlabel'])
                ax.yaxis.label.set_fontsize(fontsizes['ylabel'])
                ax.title.set_fontsize(fontsizes['title'])
                ax.tick_params(axis='x', labelsize=fontsizes['xlabel'])
                ax.tick_params(axis='y', labelsize=fontsizes['ylabel'])

            if self.canvas_item:
                self.canvas_item.draw()

            self.scene.update()
