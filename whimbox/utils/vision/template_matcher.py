import cv2
import numpy as np
from whimbox.utils.common import is_rgba_image

def alpha_aware_match(image: np.ndarray, template_rgba: np.ndarray):
    h_img, w_img = image.shape[:2]
    h_tpl, w_tpl = template_rgba.shape[:2]

    if is_rgba_image(template_rgba):
        tpl = template_rgba[..., :3].astype(np.float32)
        alpha = template_rgba[..., 3].astype(np.float32) / 255.0
        alpha = alpha[..., None]
    else:
        tpl = template_rgba.astype(np.float32)
        alpha = np.ones((h_tpl, w_tpl, 1), dtype=np.float32)

    img = image[..., :3].astype(np.float32)

    best_score = -np.inf
    best_pos = (0, 0)

    for y in range(h_img - h_tpl + 1):
        for x in range(w_img - w_tpl + 1):
            roi = img[y:y+h_tpl, x:x+w_tpl]
            roi_w = roi * alpha
            tpl_w = tpl * alpha

            roi_mean = roi_w.mean()
            tpl_mean = tpl_w.mean()

            roi_n = roi_w - roi_mean
            tpl_n = tpl_w - tpl_mean

            numer = (roi_n * tpl_n).sum()
            denom = np.sqrt((roi_n**2).sum() * (tpl_n**2).sum())

            if denom <= 0:
                continue

            score = numer / denom
            if score > best_score:
                best_score = score
                best_pos = (x, y)

    return best_pos, best_score

def fast_alpha_match(image: np.ndarray, template_rgba: np.ndarray, threshold=0.8):
    img_bgr = image[..., :3]
    tpl_bgr = template_rgba[..., :3]

    if is_rgba_image(template_rgba):
        alpha = template_rgba[..., 3]
        _, mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)
    else:
        mask = None

    res = cv2.matchTemplate(img_bgr, tpl_bgr, cv2.TM_CCOEFF_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return max_loc, max_val, res
    return None, max_val, res

def multi_channel_match(image: np.ndarray, template_rgba: np.ndarray, weights=None):
    if weights is None:
        weights = [0.3, 0.3, 0.4]

    img = image[..., :3]
    tpl = template_rgba[..., :3]

    if is_rgba_image(template_rgba):
        alpha = template_rgba[..., 3] / 255.0
        mask = (alpha * 255).astype(np.uint8)
    else:
        mask = None

    scores = []
    for i, w in enumerate(weights):
        ch = cv2.matchTemplate(img[..., i], tpl[..., i], cv2.TM_CCOEFF_NORMED, mask=mask)
        scores.append(ch * w)

    combined = np.sum(scores, axis=0)
    _, max_val, _, max_loc = cv2.minMaxLoc(combined)
    return max_loc, max_val, combined

def edge_based_match(image: np.ndarray, template_rgba: np.ndarray):
    gray = cv2.cvtColor(image[..., :3], cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(gray, 50, 150)

    if is_rgba_image(template_rgba):
        alpha = template_rgba[..., 3]
        tpl_edges = cv2.Canny(alpha, 50, 150)
    else:
        tpl_gray = cv2.cvtColor(template_rgba, cv2.COLOR_BGR2GRAY)
        tpl_edges = cv2.Canny(tpl_gray, 50, 150)

    res = cv2.matchTemplate(img_edges.astype(np.float32), tpl_edges.astype(np.float32),
                            cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    return max_loc, max_val, res

def feature_match(image: np.ndarray, template_rgba: np.ndarray, nfeatures=500, top_n=10):
    img = image[..., :3]
    tpl = template_rgba[..., :3]

    orb = cv2.ORB_create(nfeatures=nfeatures)

    mask = None
    if is_rgba_image(template_rgba):
        alpha = template_rgba[..., 3]
        mask = (alpha > 10).astype(np.uint8)

    kp1, des1 = orb.detectAndCompute(tpl, mask)
    kp2, des2 = orb.detectAndCompute(img, None)

    if des1 is None or des2 is None or len(kp1) == 0 or len(kp2) == 0:
        return None, 0.0, {"matches": [], "kp1": kp1, "kp2": kp2}

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    if not matches:
        return None, 0.0, {"matches": [], "kp1": kp1, "kp2": kp2}

    matches = sorted(matches, key=lambda x: x.distance)
    good = matches[:min(top_n, len(matches))]
    score = np.mean([1.0 / (m.distance + 1) for m in good])

    best = good[0]
    cx, cy = kp2[best.trainIdx].pt
    return (int(cx), int(cy)), score, {"matches": matches, "kp1": kp1, "kp2": kp2}