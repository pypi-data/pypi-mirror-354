"""
Simplified COCO utilities for CarinaNet package
"""

import torch
import numpy as np
import kwcoco
from .constants import COCO_LABELS_INVERSE, ANNO_FILE_NAME_FIELD


def get_annotations_by_image_id(
    coco_annotations: kwcoco.CocoDataset, coco_image_id: int
) -> list[dict]:
    """Get annotations for a specific image ID."""
    coco_anno_ids = coco_annotations.gid_to_aids[coco_image_id]
    coco_annos = [coco_annotations.anns[id] for id in coco_anno_ids]
    return coco_annos


def convert_coco_annot_to_tensors(coco_annots: list[dict]) -> torch.Tensor:
    """Convert COCO annotations to tensors."""
    # get ground truth annotations
    annotations = np.zeros((0, 5))

    for coco_annot in coco_annots:
        annotation = np.zeros((1, 5))
        annotation[0, :4] = coco_annot["bbox"]
        annotation[0, 4] = COCO_LABELS_INVERSE[coco_annot["category_id"]]
        annotations = np.append(annotations, annotation, axis=0)

    # transform from [x, y, w, h] to [x1, y1, x2, y2]
    annotations[:, 2] = annotations[:, 0] + annotations[:, 2]
    annotations[:, 3] = annotations[:, 1] + annotations[:, 3]

    return torch.tensor(annotations)


def get_image_file_path(
    coco_annotations: kwcoco.CocoDataset, coco_image_id: int
) -> str:
    """Get image file path for a specific image ID."""
    return coco_annotations.imgs[coco_image_id][ANNO_FILE_NAME_FIELD] 