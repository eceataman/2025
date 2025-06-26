import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional

class CameraMovementDetector:
    """Advanced Camera Movement Detection using multiple algorithms"""
    
    def __init__(self):
        # Initialize feature detectors
        self.orb = cv2.ORB_create(nfeatures=1000)
        self.sift = None
        try:
            self.sift = cv2.SIFT_create()
        except AttributeError:
            pass  # SIFT might not be available in some OpenCV builds
        
        # Parameters for different algorithms
        self.feature_matching_params = {
            'distance_threshold': 0.7,
            'min_match_count': 10,
            'ransac_threshold': 5.0,
            'ransac_max_iters': 1000
        }
        
        self.optical_flow_params = {
            'feature_params': dict(
                maxCorners=100,
                qualityLevel=0.3,
                minDistance=7,
                blockSize=7
            ),
            'lk_params': dict(
                winSize=(15, 15),
                maxLevel=2,
                criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
            )
        }

    def detect_with_feature_matching(self, frame1: np.ndarray, frame2: np.ndarray) -> Dict:
        """Detect camera movement using ORB feature matching"""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        
        # Detect keypoints and descriptors
        kp1, des1 = self.orb.detectAndCompute(gray1, None)
        kp2, des2 = self.orb.detectAndCompute(gray2, None)
        
        if des1 is None or des2 is None or len(kp1) < 10 or len(kp2) < 10:
            return {'movement_detected': False, 'confidence': 0.0, 'method': 'feature_matching'}
        
        # Match features
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        
        if len(matches) < self.feature_matching_params['min_match_count']:
            return {'movement_detected': False, 'confidence': 0.0, 'method': 'feature_matching'}
        
        # Filter good matches
        good_matches = [m for m in matches if m.distance < self.feature_matching_params['distance_threshold'] * 255]
        
        if len(good_matches) < self.feature_matching_params['min_match_count']:
            return {'movement_detected': False, 'confidence': 0.0, 'method': 'feature_matching'}
        
        # Extract matched points
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        
        # Find homography with RANSAC
        homography, mask = cv2.findHomography(
            src_pts, dst_pts, 
            cv2.RANSAC, 
            self.feature_matching_params['ransac_threshold']
        )
        
        if homography is None:
            return {'movement_detected': False, 'confidence': 0.0, 'method': 'feature_matching'}
        
        # Analyze transformation
        movement_analysis = self._analyze_homography(homography)
        
        # Calculate confidence based on inliers and transformation
        inliers = np.sum(mask) if mask is not None else 0
        inlier_ratio = inliers / len(good_matches)
        
        # Detect significant camera movement
        is_camera_movement = (
            movement_analysis['translation'] > 20 or  # pixels
            movement_analysis['rotation'] > 5 or      # degrees  
            movement_analysis['scale_change'] > 0.1   # 10% scale change
        )
        
        confidence = min(inlier_ratio * movement_analysis['magnitude'], 1.0)
        
        return {
            'movement_detected': is_camera_movement,
            'confidence': confidence,
            'method': 'feature_matching',
            'details': {
                'matches_found': len(good_matches),
                'inliers': int(inliers),
                'inlier_ratio': inlier_ratio,
                'translation': movement_analysis['translation'],
                'rotation': movement_analysis['rotation'],
                'scale_change': movement_analysis['scale_change'],
                'homography': homography.tolist() if homography is not None else None
            }
        }

    def detect_with_optical_flow(self, frame1: np.ndarray, frame2: np.ndarray) -> Dict:
        """Detect camera movement using optical flow"""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        
        # Detect corners to track
        corners = cv2.goodFeaturesToTrack(gray1, **self.optical_flow_params['feature_params'])
        
        if corners is None or len(corners) < 10:
            return {'movement_detected': False, 'confidence': 0.0, 'method': 'optical_flow'}
        
        # Calculate optical flow
        new_corners, status, error = cv2.calcOpticalFlowPyrLK(
            gray1, gray2, corners, None, **self.optical_flow_params['lk_params']
        )
        
        # Filter good tracking points
        good_old = corners[status == 1]
        good_new = new_corners[status == 1]
        
        if len(good_old) < 10:
            return {'movement_detected': False, 'confidence': 0.0, 'method': 'optical_flow'}
        
        # Calculate motion vectors
        motion_vectors = good_new - good_old
        
        # Analyze global motion
        global_motion = self._analyze_global_motion(motion_vectors)
        
        # Detect camera movement based on consistent global motion
        is_camera_movement = (
            global_motion['dominant_motion_strength'] > 0.6 and
            global_motion['average_magnitude'] > 3.0
        )
        
        confidence = global_motion['dominant_motion_strength']
        
        return {
            'movement_detected': is_camera_movement,
            'confidence': confidence,
            'method': 'optical_flow',
            'details': {
                'tracked_points': len(good_old),
                'average_magnitude': global_motion['average_magnitude'],
                'dominant_direction': global_motion['dominant_direction'],
                'motion_consistency': global_motion['dominant_motion_strength']
            }
        }

    def _analyze_homography(self, homography: np.ndarray) -> Dict:
        """Analyze homography matrix to extract transformation parameters"""
        # Decompose homography to get transformation parameters
        try:
            # Extract translation
            translation = np.sqrt(homography[0, 2]**2 + homography[1, 2]**2)
            
            # Extract rotation (approximate)
            rotation = np.arctan2(homography[1, 0], homography[0, 0]) * 180 / np.pi
            
            # Extract scale change
            scale_x = np.sqrt(homography[0, 0]**2 + homography[1, 0]**2)
            scale_y = np.sqrt(homography[0, 1]**2 + homography[1, 1]**2)
            scale_change = abs(1.0 - (scale_x + scale_y) / 2.0)
            
            # Overall magnitude of transformation
            magnitude = translation / 100.0 + abs(rotation) / 45.0 + scale_change
            
            return {
                'translation': translation,
                'rotation': abs(rotation),
                'scale_change': scale_change,
                'magnitude': min(magnitude, 1.0)
            }
        except:
            return {
                'translation': 0,
                'rotation': 0,
                'scale_change': 0,
                'magnitude': 0
            }

    def _analyze_global_motion(self, motion_vectors: np.ndarray) -> Dict:
        """Analyze motion vectors to detect global camera movement"""
        if len(motion_vectors) == 0:
            return {
                'average_magnitude': 0,
                'dominant_direction': 0,
                'dominant_motion_strength': 0
            }
        
        # Calculate magnitudes and angles
        magnitudes = np.sqrt(motion_vectors[:, 0]**2 + motion_vectors[:, 1]**2)
        angles = np.arctan2(motion_vectors[:, 1], motion_vectors[:, 0])
        
        average_magnitude = np.mean(magnitudes)
        
        # Find dominant direction using circular statistics
        mean_x = np.mean(np.cos(angles))
        mean_y = np.mean(np.sin(angles))
        dominant_direction = np.arctan2(mean_y, mean_x) * 180 / np.pi
        
        # Measure consistency of motion (how well vectors align)
        dominant_motion_strength = np.sqrt(mean_x**2 + mean_y**2)
        
        return {
            'average_magnitude': average_magnitude,
            'dominant_direction': dominant_direction,
            'dominant_motion_strength': dominant_motion_strength
        }

    def detect_frame_difference(self, frame1: np.ndarray, frame2: np.ndarray, threshold: float = 50.0) -> Dict:
        """Basic frame differencing method (legacy support)"""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        
        # Resize for performance
        height, width = gray1.shape[:2]
        if width > 640:
            scale = 640.0 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            gray1 = cv2.resize(gray1, (new_width, new_height))
            gray2 = cv2.resize(gray2, (new_width, new_height))
        
        diff = cv2.absdiff(gray1, gray2)
        score = np.mean(diff)
        significant_pixels = np.sum(diff > 30) / diff.size * 100
        combined_score = score + (significant_pixels * 2)
        
        is_movement = combined_score > threshold
        confidence = min(combined_score / (threshold * 2), 1.0)
        
        return {
            'movement_detected': is_movement,
            'confidence': confidence,
            'method': 'frame_difference',
            'details': {
                'difference_score': score,
                'significant_pixels_percent': significant_pixels,
                'combined_score': combined_score
            }
        }

def detect_significant_movement(frames: List[np.ndarray], threshold: float = 50.0, method: str = 'auto') -> List[int]:
    """
    Main function for detecting significant camera movement.
    
    Args:
        frames: List of image frames (as numpy arrays).
        threshold: Sensitivity threshold for detecting movement.
        method: Detection method ('auto', 'feature_matching', 'optical_flow', 'frame_difference')
    
    Returns:
        List of indices where significant movement is detected.
    """
    if len(frames) < 2:
        return []
    
    detector = CameraMovementDetector()
    movement_indices = []
    
    for idx in range(1, len(frames)):
        try:
            frame1 = frames[idx-1]
            frame2 = frames[idx]
            
            # Ensure frames are valid
            if frame1.shape != frame2.shape:
                continue
            
            results = []
            
            if method in ['auto', 'feature_matching']:
                result = detector.detect_with_feature_matching(frame1, frame2)
                results.append(result)
            
            if method in ['auto', 'optical_flow']:
                result = detector.detect_with_optical_flow(frame1, frame2)
                results.append(result)
            
            if method in ['auto', 'frame_difference'] or len(results) == 0:
                result = detector.detect_frame_difference(frame1, frame2, threshold)
                results.append(result)
            
            # Fusion of multiple methods for 'auto' mode
            if method == 'auto' and len(results) > 1:
                # Use weighted voting
                weighted_score = 0
                total_weight = 0
                
                for result in results:
                    if result['movement_detected']:
                        weight = result['confidence']
                        if result['method'] == 'feature_matching':
                            weight *= 1.5  # Higher weight for feature matching
                        elif result['method'] == 'optical_flow':
                            weight *= 1.2  # Medium weight for optical flow
                        
                        weighted_score += weight
                        total_weight += 1
                
                # Movement detected if weighted average confidence > 0.3
                movement_detected = (weighted_score / max(total_weight, 1)) > 0.3
            else:
                movement_detected = any(r['movement_detected'] for r in results)
            
            if movement_detected:
                movement_indices.append(idx)
                
        except Exception as e:
            print(f"Error processing frame {idx}: {str(e)}")
            continue
    
    return movement_indices
