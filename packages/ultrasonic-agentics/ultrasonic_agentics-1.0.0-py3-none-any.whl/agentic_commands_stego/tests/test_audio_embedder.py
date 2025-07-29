"""
Tests for audio embedder using London School TDD approach.
Tests interactions between components using mocks.
"""

import pytest
from unittest.mock import Mock, patch, call
import tempfile
import os
from pydub import AudioSegment
import numpy as np

from ..embed.audio_embedder import AudioEmbedder
from ..crypto.cipher import CipherService
from ..embed.ultrasonic_encoder import UltrasonicEncoder


class TestAudioEmbedder:
    """Test suite for AudioEmbedder using mockist/London style TDD."""
    
    def test_audio_embedder_initializes_with_cipher_and_encoder(self):
        """Test that AudioEmbedder properly initializes its dependencies."""
        key = b'test_key_32_bytes_long_for_test!'
        embedder = AudioEmbedder(key=key)
        
        assert embedder.cipher is not None
        assert embedder.encoder is not None
        assert embedder.cipher.get_key() == key
    
    def test_embed_calls_encrypt_and_encode_in_sequence(self):
        """Test that embed method calls encryption then encoding then merging."""
        embedder = AudioEmbedder()
        
        # Mock the internal methods to check call sequence
        embedder._encrypt_payload = Mock(return_value=b"encrypted_payload")
        embedder._encode_ultrasonic = Mock(return_value=AudioSegment.silent(100))
        embedder._merge_audio = Mock(return_value=AudioSegment.silent(100))
        
        test_audio = AudioSegment.silent(duration=1000, frame_rate=48000)
        
        # Act: Call embed
        result = embedder.embed(test_audio, "test_command", obfuscate=True)
        
        # Assert: Verify the interaction sequence
        embedder._encrypt_payload.assert_called_once_with("test_command", True)
        embedder._encode_ultrasonic.assert_called_once_with(b"encrypted_payload")
        embedder._merge_audio.assert_called_once()
        
        # Verify arguments to merge_audio
        merge_args = embedder._merge_audio.call_args[0]
        assert merge_args[0] == test_audio  # Original audio
        # Second arg should be the ultrasonic signal
    
    def test_embed_skips_obfuscation_when_disabled(self):
        """Test that obfuscation is skipped when obfuscate=False."""
        embedder = AudioEmbedder()
        
        # Mock the internal methods
        embedder._encrypt_payload = Mock(return_value=b"encrypted")
        embedder._encode_ultrasonic = Mock(return_value=AudioSegment.silent(100))
        embedder._merge_audio = Mock(return_value=AudioSegment.silent(100))
        
        test_audio = AudioSegment.silent(duration=1000, frame_rate=48000)
        
        # Call with obfuscate=False
        embedder.embed(test_audio, "test", obfuscate=False)
        
        # Verify encrypt_payload was called with obfuscate=False
        embedder._encrypt_payload.assert_called_once_with("test", False)
    
    def test_embed_file_calls_embed_with_loaded_audio(self):
        """Test that embed_file loads audio, calls embed, and exports result."""
        embedder = AudioEmbedder()
        
        # Mock the methods
        embedder.embed = Mock(return_value=AudioSegment.silent(1000))
        
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_input:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_output:
                try:
                    # Create a minimal audio file
                    test_audio = AudioSegment.silent(duration=1000, frame_rate=48000)
                    test_audio.export(temp_input.name, format="mp3")
                    
                    # Mock the export to avoid actual file writing
                    with patch.object(AudioSegment, 'export') as mock_export:
                        embedder.embed_file(temp_input.name, temp_output.name, "test_command")
                    
                    # Verify embed was called
                    embedder.embed.assert_called_once()
                    args, kwargs = embedder.embed.call_args
                    assert kwargs.get('obfuscate', True) == True  # Default value
                    assert args[1] == "test_command"
                    
                    # Verify export was called
                    mock_export.assert_called_once()
                    
                finally:
                    # Clean up
                    for path in [temp_input.name, temp_output.name]:
                        if os.path.exists(path):
                            os.unlink(path)
    
    def test_encrypt_payload_calls_cipher_methods_correctly(self):
        """Test that _encrypt_payload calls cipher methods in correct order."""
        embedder = AudioEmbedder()
        
        # Mock cipher methods
        embedder.cipher.encrypt_command = Mock(return_value=b"encrypted")
        embedder.cipher.add_obfuscation = Mock(return_value=b"obfuscated")
        
        # Test with obfuscation
        result = embedder._encrypt_payload("test_command", obfuscate=True)
        
        embedder.cipher.encrypt_command.assert_called_once_with("test_command")
        embedder.cipher.add_obfuscation.assert_called_once_with(b"encrypted")
        assert result == b"obfuscated"
        
        # Reset mocks and test without obfuscation
        embedder.cipher.encrypt_command.reset_mock()
        embedder.cipher.add_obfuscation.reset_mock()
        
        result = embedder._encrypt_payload("test_command", obfuscate=False)
        
        embedder.cipher.encrypt_command.assert_called_once_with("test_command")
        embedder.cipher.add_obfuscation.assert_not_called()
        assert result == b"encrypted"
    
    def test_encode_ultrasonic_calls_encoder_methods_correctly(self):
        """Test that _encode_ultrasonic calls encoder methods correctly."""
        embedder = AudioEmbedder()
        
        # Mock encoder methods
        mock_signal = np.array([0.1, 0.2, 0.3])
        mock_audio_segment = Mock(spec=AudioSegment)
        
        embedder.encoder.encode_payload = Mock(return_value=mock_signal)
        embedder.encoder.create_audio_segment = Mock(return_value=mock_audio_segment)
        
        test_payload = b"test_payload"
        result = embedder._encode_ultrasonic(test_payload)
        
        embedder.encoder.encode_payload.assert_called_once_with(test_payload)
        embedder.encoder.create_audio_segment.assert_called_once_with(mock_signal)
        assert result == mock_audio_segment
    
    def test_merge_audio_handles_different_sample_rates(self):
        """Test that _merge_audio normalizes sample rates."""
        embedder = AudioEmbedder()
        
        # Create audio with different sample rates
        original = AudioSegment.silent(duration=1000, frame_rate=44100)
        ultrasonic = AudioSegment.silent(duration=500, frame_rate=48000)
        
        # Mock the set_frame_rate method
        with patch.object(AudioSegment, 'set_frame_rate') as mock_set_rate:
            mock_set_rate.return_value = AudioSegment.silent(duration=1000, frame_rate=48000)
            
            result = embedder._merge_audio(original, ultrasonic)
            
            # Should have called set_frame_rate to normalize
            assert mock_set_rate.called
            # Check that 48000 was passed as argument at least once
            calls = [call for call in mock_set_rate.call_args_list if call[0][0] == 48000]
            assert len(calls) > 0
    
    def test_merge_audio_handles_different_channel_counts(self):
        """Test that _merge_audio handles mono/stereo conversion."""
        embedder = AudioEmbedder()
        
        # Create stereo original and mono ultrasonic
        original = AudioSegment.silent(duration=1000, frame_rate=48000).set_channels(2)
        ultrasonic = AudioSegment.silent(duration=500, frame_rate=48000).set_channels(1)
        
        # Mock the from_mono_audiosegments method
        with patch.object(AudioSegment, 'from_mono_audiosegments') as mock_from_mono:
            mock_from_mono.return_value = AudioSegment.silent(duration=500, frame_rate=48000).set_channels(2)
            
            result = embedder._merge_audio(original, ultrasonic)
            
            # Should have called from_mono_audiosegments to convert ultrasonic to stereo
            mock_from_mono.assert_called_once()
    
    def test_merge_audio_extends_original_when_ultrasonic_is_longer(self):
        """Test that original audio is extended when ultrasonic signal is longer."""
        embedder = AudioEmbedder()
        
        # Create short original and long ultrasonic
        original = AudioSegment.silent(duration=1000, frame_rate=48000)
        ultrasonic = AudioSegment.silent(duration=2000, frame_rate=48000)
        
        result = embedder._merge_audio(original, ultrasonic)
        
        # Result should be at least as long as ultrasonic
        assert len(result) >= len(ultrasonic)
    
    def test_get_format_from_path_returns_correct_formats(self):
        """Test that file format detection works correctly."""
        embedder = AudioEmbedder()
        
        format_tests = [
            ('test.mp3', 'mp3'),
            ('test.wav', 'wav'),
            ('test.flac', 'flac'),
            ('test.ogg', 'ogg'),
            ('test.m4a', 'mp4'),
            ('test.aac', 'aac'),
            ('test.unknown', 'mp3'),  # Default fallback
        ]
        
        for path, expected_format in format_tests:
            assert embedder._get_format_from_path(path) == expected_format
    
    def test_validate_audio_compatibility_checks_frequency_range(self):
        """Test that audio compatibility validation works correctly."""
        embedder = AudioEmbedder()
        
        # Test compatible audio (high sample rate)
        compatible_audio = AudioSegment.silent(duration=1000, frame_rate=48000)
        result = embedder.validate_audio_compatibility(compatible_audio)
        
        assert result['compatible'] == True
        assert result['sample_rate'] == 48000
        assert 'nyquist_frequency' in result
        assert 'ultrasonic_range' in result
        
        # Test incompatible audio (low sample rate)
        incompatible_audio = AudioSegment.silent(duration=1000, frame_rate=22050)
        result = embedder.validate_audio_compatibility(incompatible_audio)
        
        assert result['compatible'] == False
    
    def test_estimate_embedding_duration_uses_cipher_and_encoder(self):
        """Test that duration estimation uses both cipher and encoder."""
        embedder = AudioEmbedder()
        
        # Mock the cipher and encoder methods
        embedder.cipher.encrypt_command = Mock(return_value=b"encrypted" * 5)
        embedder.cipher.add_obfuscation = Mock(return_value=b"obfuscated" * 6)
        embedder.encoder.estimate_payload_duration = Mock(return_value=1.5)
        
        result = embedder.estimate_embedding_duration("test command")
        
        embedder.cipher.encrypt_command.assert_called_once_with("test command")
        embedder.cipher.add_obfuscation.assert_called_once()
        embedder.encoder.estimate_payload_duration.assert_called_once()
        assert result == 1.5
    
    def test_cipher_key_management_methods(self):
        """Test cipher key getter and setter methods."""
        original_key = b'original_key_32_bytes_for_test'
        embedder = AudioEmbedder(key=original_key)
        
        assert embedder.get_cipher_key() == original_key
        
        new_key = b'new_key_here_32_bytes_for_test'
        embedder.set_cipher_key(new_key)
        
        assert embedder.get_cipher_key() == new_key
        assert embedder.cipher.get_key() == new_key
    
    def test_frequency_management_methods(self):
        """Test frequency getter and setter methods."""
        embedder = AudioEmbedder()
        
        original_range = embedder.get_frequency_range()
        assert len(original_range) == 2
        
        new_freq_0, new_freq_1 = 17000, 18000
        embedder.set_frequencies(new_freq_0, new_freq_1)
        
        updated_range = embedder.get_frequency_range()
        assert updated_range == (new_freq_0, new_freq_1)
    
    def test_amplitude_management_method(self):
        """Test amplitude setter method."""
        embedder = AudioEmbedder()
        
        new_amplitude = 0.5
        embedder.set_amplitude(new_amplitude)
        
        assert embedder.encoder.amplitude == new_amplitude
    
    @patch('agentic_commands_stego.embed.audio_embedder.AudioSegment.from_file')
    @patch('agentic_commands_stego.embed.audio_embedder.AudioSegment.export')
    def test_embed_file_handles_file_operations_correctly(self, mock_export, mock_from_file):
        """Test that embed_file handles file I/O correctly."""
        # Arrange
        embedder = AudioEmbedder()
        mock_audio = Mock(spec=AudioSegment)
        mock_audio.frame_rate = 48000
        mock_from_file.return_value = mock_audio
        
        embedder.embed = Mock(return_value=mock_audio)
        
        # Act
        embedder.embed_file("input.mp3", "output.mp3", "test_command")
        
        # Assert
        mock_from_file.assert_called_once_with("input.mp3")
        embedder.embed.assert_called_once_with(mock_audio, "test_command", True)
        mock_export.assert_called_once()
        
        # Check export parameters
        export_call = mock_export.call_args
        assert export_call[0][0] == "output.mp3"  # First positional arg
        assert export_call[1]['format'] == 'mp3'
        assert export_call[1]['bitrate'] == '192k'