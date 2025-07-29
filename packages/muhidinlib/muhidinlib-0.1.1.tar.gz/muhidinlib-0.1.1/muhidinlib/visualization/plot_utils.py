import matplotlib.pyplot as plt

class BarChart:
    """
    Kelas untuk membuat grafik bar vertikal atau horizontal dengan nilai yang ditampilkan.

    Attributes:
        labels (list): Label kategori untuk sumbu x/y
        values (list): Nilai numerik untuk setiap label
        title (str): Judul grafik
        color (str): Warna batang grafik
    """

    def __init__(self, labels, values, title=None, color='skyblue'):
        self.labels = labels
        self.values = values
        self.title = title
        self.color = color

    def plot_vertical(self, show_values=True):
        """
        Menampilkan grafik bar vertikal.

        Args:
            show_values (bool): Jika True, tampilkan nilai di atas setiap bar.
        """
        fig, ax = plt.subplots()
        bars = ax.bar(self.labels, self.values, color=self.color)

        if show_values:
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + max(self.values) * 0.01,
                    f'{height:.1f}',
                    ha='center'
                )

        if self.title:
            ax.set_title(self.title)

        plt.tight_layout()
        plt.show()

    def plot_horizontal(self, show_values=True):
        """
        Menampilkan grafik bar horizontal.

        Args:
            show_values (bool): Jika True, tampilkan nilai di sebelah kanan setiap bar.
        """
        fig, ax = plt.subplots()
        bars = ax.barh(self.labels, self.values, color=self.color)

        if show_values:
            for bar in bars:
                width = bar.get_width()
                ax.text(
                    width + max(self.values) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f'{width:.1f}',
                    va='center'
                )

        if self.title:
            ax.set_title(self.title)

        plt.tight_layout()
        plt.show()