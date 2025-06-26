import streamlit as st
import numpy as np
from PIL import Image
import cv2
import tempfile
import os
import movement_detector

def extract_frames_from_video(video_path, max_frames=100):
    """Extract frames from video file"""
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    st.info(f"Video info: {total_frames} total frames, {fps} FPS")
    
    # Sample frames if video is too long
    frame_step = max(1, total_frames // max_frames)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_step == 0:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
            
        frame_count += 1
        
        if len(frames) >= max_frames:
            break
    
    cap.release()
    return frames

st.title("🎥 Camera Movement Detection")
st.write(
    "Upload a video file or a sequence of images. The app will detect frames with significant camera movement."
)

# Create tabs for different input methods
tab1, tab2 = st.tabs(["📁 Video File", "🖼️ Image Sequence"])

frames = []
input_method = None

with tab1:
    st.subheader("Upload Video File")
    uploaded_video = st.file_uploader(
        "Choose a video file", 
        type=["mp4", "avi", "mov", "mkv", "webm"],
        help="Supported formats: MP4, AVI, MOV, MKV, WebM"
    )
    
    if uploaded_video is not None:
        # Save uploaded video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_video.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_video.read())
            temp_video_path = tmp_file.name
        
        try:
            st.success(f"Video uploaded: {uploaded_video.name}")
            
            # Extract frames
            with st.spinner("Extracting frames from video..."):
                frames = extract_frames_from_video(temp_video_path)
            
            input_method = "video"
            
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_video_path):
                os.unlink(temp_video_path)

with tab2:
    st.subheader("Upload Image Sequence")
    uploaded_files = st.file_uploader(
        "Choose image files", 
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        accept_multiple_files=True,
        help="Upload multiple images in sequence"
    )

    if uploaded_files:
        frames = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            frame = np.array(image)
            if frame.shape[-1] == 4:  # RGBA to RGB
                frame = frame[:, :, :3]
            frames.append(frame)
        
        input_method = "images"
        st.success(f"Loaded {len(frames)} images")

# Process frames if any input is provided
if frames:
    st.write(f"📊 Processing {len(frames)} frames...")
    
    # Algorithm selection
    algorithm_method = st.selectbox(
        "🔬 Detection Algorithm",
        ["auto", "feature_matching", "optical_flow", "frame_difference"],
        index=0,
        help="""
        • auto: Combines multiple methods for best accuracy
        • feature_matching: ORB keypoints + RANSAC homography (advanced)
        • optical_flow: Lucas-Kanade optical flow tracking
        • frame_difference: Basic pixel difference (fast)
        """
    )
    
    # Add threshold slider (only for frame_difference method)
    if algorithm_method in ['auto', 'frame_difference']:
        threshold = st.slider(
            "Movement Detection Threshold", 
            min_value=10.0, 
            max_value=200.0, 
            value=50.0, 
            step=5.0,
            help="Lower values = more sensitive detection (mainly for frame difference method)"
        )
    else:
        threshold = 50.0  # Default for other methods
    
    # Detect movement
    with st.spinner(f"Analyzing camera movement using {algorithm_method} method..."):
        if algorithm_method == 'auto':
            movement_indices = movement_detector.detect_significant_movement(
                frames, threshold=threshold, method='auto'
            )
        else:
            movement_indices = movement_detector.detect_significant_movement(
                frames, threshold=threshold, method=algorithm_method
            )
    
    # Display results
    if movement_indices:
        st.success(f"🚨 Significant movement detected at {len(movement_indices)} frames: {movement_indices}")
        
        # Show detailed analysis for advanced methods
        if algorithm_method in ['auto', 'feature_matching', 'optical_flow']:
            with st.expander("🔍 Detailed Analysis"):
                detector = movement_detector.CameraMovementDetector()
                
                for idx in movement_indices[:3]:  # Show details for first 3 detected frames
                    if idx > 0:
                        st.subheader(f"Frame {idx} Analysis")
                        
                        frame1 = frames[idx-1]
                        frame2 = frames[idx]
                        
                        cols = st.columns(3)
                        
                        if algorithm_method in ['auto', 'feature_matching']:
                            with cols[0]:
                                st.write("**Feature Matching:**")
                                result = detector.detect_with_feature_matching(frame1, frame2)
                                if result['movement_detected']:
                                    st.write(f"✅ Movement: {result['confidence']:.2f} confidence")
                                    st.json(result['details'])
                                else:
                                    st.write("❌ No movement detected")
                        
                        if algorithm_method in ['auto', 'optical_flow']:
                            with cols[1]:
                                st.write("**Optical Flow:**")
                                result = detector.detect_with_optical_flow(frame1, frame2)
                                if result['movement_detected']:
                                    st.write(f"✅ Movement: {result['confidence']:.2f} confidence")
                                    st.json(result['details'])
                                else:
                                    st.write("❌ No movement detected")
                        
                        if algorithm_method in ['auto', 'frame_difference']:
                            with cols[2]:
                                st.write("**Frame Difference:**")
                                result = detector.detect_frame_difference(frame1, frame2, threshold)
                                if result['movement_detected']:
                                    st.write(f"✅ Movement: {result['confidence']:.2f} confidence")
                                    st.json(result['details'])
                                else:
                                    st.write("❌ No movement detected")
                        
                        st.divider()
        
        # Create columns for frame display
        cols_per_row = 3
        for i in range(0, len(movement_indices), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, idx in enumerate(movement_indices[i:i+cols_per_row]):
                with cols[j]:
                    st.image(
                        frames[idx], 
                        caption=f"Frame {idx} - Movement Detected", 
                        use_container_width=True
                    )
    else:
        st.info("✅ No significant camera movement detected in the provided frames")
        
        # Show what was analyzed
        st.write(f"**Analysis Summary:**")
        st.write(f"• Method used: {algorithm_method}")
        st.write(f"• Frames analyzed: {len(frames)}")
        st.write(f"• Threshold: {threshold}")
    
    # Show sample frames for reference
    with st.expander("📸 View Sample Frames"):
        sample_indices = [0, len(frames)//4, len(frames)//2, 3*len(frames)//4, -1]
        sample_indices = [i for i in sample_indices if 0 <= i < len(frames)]
        
        cols = st.columns(len(sample_indices))
        for i, idx in enumerate(sample_indices):
            with cols[i]:
                movement_status = "🚨 Movement" if idx in movement_indices else "✅ Static"
                st.image(
                    frames[idx], 
                    caption=f"Frame {idx}\n{movement_status}", 
                    use_container_width=True
                )
