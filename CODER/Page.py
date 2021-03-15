import os
from PIL import Image


class Page:
    PX_UNAVAILABLE = (0, 0, 0)
    PX_AVAILABLE = (255, 255, 255)
    PX_FAILED = (255, 0, 0)

    def __init__(self, file_path_template, file_path_output, dpi=(600, 600)):
        self.dpi = dpi
        self.template = Image.open(file_path_template)
        self.template_pixels = self.template.load()
        self.template_width = self.template.size[0]
        self.template_height = self.template.size[1]
        self.output = (
            Image.new("RGB", self.template.size, "white")
            if not os.path.isfile(file_path_output)
            else Image.open(file_path_output)
        )

    def find_coordinates_for_next_available_spot(self, label):
        """"""

        def has_enough_space(label, coordinates):
            label_size = label.get_image().size
            if (
                self.template_pixels[coordinates[0], coordinates[1]]
                == self.PX_UNAVAILABLE
                or self.template_pixels[coordinates[0], coordinates[1]]
                == self.PX_FAILED
            ):
                return False
            elif (
                coordinates[0] + label_size[0] > self.template_width
                or coordinates[1] + label_size[1] > self.template_height
            ):
                self.template_pixels[coordinates[0], coordinates[1]] = self.PX_FAILED
                return False
            else:
                for y_label in range(label_size[1]):
                    for x_label in range(label_size[0]):
                        if (
                            self.template_pixels[
                                coordinates[0] + x_label, coordinates[1] + y_label
                            ]
                            == self.PX_UNAVAILABLE
                            or self.template_pixels[
                                coordinates[0] + x_label, coordinates[1] + y_label
                            ]
                            == self.PX_FAILED
                        ):
                            self.template_pixels[x_label, y_label] = self.PX_FAILED
                            return False
                        else:
                            self.template_pixels[
                                coordinates[0] + x_label, coordinates[1] + y_label
                            ] = self.PX_FAILED
            return True

        for y in range(self.template.size[1]):
            for x in range(self.template.size[0]):
                if has_enough_space(label, (x, y)):
                    return (x, y)

        return (-1, -1)

    def add_label(self, label, label_coordinates, overlap=False):
        """"""

        def get_adjusted_coordinates(label, coordinates, overlap):
            """"""
            if overlap:
                label_coordinates = (
                    coordinates[0] - label.get_border_thickness(),
                    coordinates[1] - label.get_border_thickness(),
                )
            else:
                label_coordinates = coordinates
            return label_coordinates

        def update_output(output, label, label_coordinates):
            """"""
            output.paste(label.get_image(), label_coordinates)
            return output

        def update_template(template, label, label_coordinates, pixel_value):
            """"""
            template_pixels = template.load()
            for y_label in range(label.get_image().size[1]):
                for x_label in range(label.get_image().size[0]):
                    template_pixels[
                        label_coordinates[0] + x_label, label_coordinates[1] + y_label
                    ] = pixel_value
            return template

        update_template(self.template, label, label_coordinates, self.PX_AVAILABLE)
        label_coordinates = get_adjusted_coordinates(label, label_coordinates, overlap)
        update_output(self.output, label, label_coordinates)
        update_template(self.template, label, label_coordinates, self.PX_UNAVAILABLE)

        return

    def get_page_dimensions(self):
        """"""
        return self.template.size

    def clean_template(self):
        """"""
        for y in range(self.template_height):
            for x in range(self.template_width):
                if self.template_pixels[x, y] == self.PX_FAILED:
                    self.template_pixels[x, y] = self.PX_AVAILABLE
        return

    def save_page_to_file(self, file_path):
        """
        Write template image to an image file.
        """
        self.output.save(file_path, dpi=self.dpi)

    def save_template_to_file(self, file_path):
        """"""
        self.template.save(file_path, dpi=self.dpi)
