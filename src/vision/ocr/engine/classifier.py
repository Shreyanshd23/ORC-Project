from typing import List, Dict
from pdf2image import convert_from_path
import numpy as np
import cv2


class LayoutClassifier:

    def classify(self, pdf_path: str, start_page=None, end_page=None) -> List[Dict]:

        images = convert_from_path(
            pdf_path,
            dpi=120,
            first_page=start_page,
            last_page=end_page,
            poppler_path=r"C:\poppler\Library\bin"
        )

        regions = []

        for i, img in enumerate(images):

            img_np = np.array(img)
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

            edges = cv2.Canny(gray, 50, 150)

            lines = cv2.HoughLinesP(
                edges, 1, np.pi/180,
                threshold=100,
                minLineLength=50,
                maxLineGap=10
            )

            line_count = 0 if lines is None else len(lines)
            edge_density = np.sum(edges > 0) / edges.size

            row_var = np.std(np.mean(gray, axis=1))
            col_var = np.std(np.mean(gray, axis=0))

            if (
                line_count > 30 or
                edge_density > 0.15 or
                (row_var < 20 and col_var < 20)
            ):
                label = "table"
            else:
                label = "text"

            regions.append({
                "page": (start_page or 1) + i,
                "label": label
            })

        return regions
