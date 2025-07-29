"""Non-maximum suppression utilities."""

import numpy as np
from typing import List


def non_max_suppression(
    boxes: np.ndarray,
    scores: np.ndarray,
    threshold: float = 0.4
) -> List[int]:
    """Apply non-maximum suppression to bounding boxes.
    
    Args:
        boxes: Array of bounding boxes [x1, y1, x2, y2]
        scores: Array of confidence scores
        threshold: IoU threshold for suppression
        
    Returns:
        List of indices to keep
    """
    if len(boxes) == 0:
        return []
    
    # Calculate areas
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    
    # Sort by scores
    indices = np.argsort(scores)[::-1]
    
    keep = []
    while len(indices) > 0:
        # Take the highest scoring box
        current = indices[0]
        keep.append(current)
        
        if len(indices) == 1:
            break
            
        # Calculate IoU with remaining boxes
        remaining = indices[1:]
        ious = calculate_iou(boxes[current], boxes[remaining], areas[current], areas[remaining])
        
        # Keep boxes with IoU below threshold
        indices = remaining[ious <= threshold]
    
    return keep


def calculate_iou(
    box: np.ndarray,
    boxes: np.ndarray,
    area: float,
    areas: np.ndarray
) -> np.ndarray:
    """Calculate Intersection over Union (IoU) between boxes.
    
    Args:
        box: Single bounding box [x1, y1, x2, y2]
        boxes: Array of bounding boxes
        area: Area of the single box
        areas: Areas of the boxes array
        
    Returns:
        Array of IoU values
    """
    # Find intersection coordinates
    xx1 = np.maximum(box[0], boxes[:, 0])
    yy1 = np.maximum(box[1], boxes[:, 1])
    xx2 = np.minimum(box[2], boxes[:, 2])
    yy2 = np.minimum(box[3], boxes[:, 3])
    
    # Calculate intersection area
    w = np.maximum(0.0, xx2 - xx1)
    h = np.maximum(0.0, yy2 - yy1)
    intersection = w * h
    
    # Calculate union area
    union = area + areas - intersection
    
    # Avoid division by zero
    union = np.maximum(union, 1e-8)
    
    return intersection / union 