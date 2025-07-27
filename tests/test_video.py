import pytest
from unittest.mock import patch, MagicMock
import io

def test_video_processing(tmp_path):
    """Test quá trình xử lý video"""
    # Mock VideoFileClip
    with patch('moviepy.editor.VideoFileClip') as mock_clip:
        mock_clip.return_value = MagicMock(
            duration=10,
            fx=MagicMock(return_value=MagicMock(
                write_videofile=MagicMock()
            ))
        )
        
        from video_processor import process_video
        
        # Tạo mock uploaded file
        mock_file = MagicMock()
        mock_file.read.return_value = b"fake_video_data"
        
        result = process_video(mock_file)
        
        assert result["status"] == "success"
        assert result["duration"] == 10

def test_streamlit_ui():
    """Test giao diện Streamlit"""
    # Mock file uploader và các thành phần UI
    with patch('streamlit.file_uploader') as mock_uploader, \
         patch('streamlit.button') as mock_button, \
         patch('streamlit.spinner'):
        
        # Thiết lập mock
        mock_uploader.return_value = MagicMock(
            name="test.mp4",
            type="video/mp4",
            size=1024*1024,
            read=MagicMock(return_value=b"fake_data")
        )
        mock_button.return_value = True
        
        from dashboard_ai import video_upload_section
        video_upload_section()
        
        # Verify các thành phần được gọi đúng
        mock_uploader.assert_called_once_with(
            "Chọn file video (MP4/AVI)",
            type=["mp4", "avi"],
            key="video_uploader"
        )