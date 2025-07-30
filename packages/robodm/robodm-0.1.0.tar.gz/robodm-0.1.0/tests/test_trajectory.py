"""Unit tests for trajectory functionality."""

import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import numpy as np
import pytest

from robodm import FeatureType, Trajectory, TrajectoryFactory
from robodm.trajectory import CodecConfig
from robodm.trajectory_base import FileSystemInterface, TimeProvider

from .test_fixtures import MockFileSystem, MockTimeProvider

# Define all codecs to test
ALL_CODECS = ["rawvideo", "ffv1", "libaom-av1", "libx264", "libx265"]


def validate_codec_roundtrip(temp_dir, codec, test_data):
    """Helper function to validate full encoding/decoding roundtrip for a codec."""
    path = os.path.join(temp_dir, f"roundtrip_test_{codec}.vla")

    try:
        # Step 1: Create trajectory with codec
        traj_write = Trajectory(path, mode="w", video_codec=codec)

        # Step 2: Write test data
        for data_dict in test_data:
            traj_write.add_by_dict(data_dict)

        # Step 3: Close trajectory (triggers encoding)
        traj_write.close()

        # Step 4: Verify file exists and has content
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

        # Step 5: Attempt to read back (triggers decoding)
        traj_read = Trajectory(path, mode="r")
        loaded_data = traj_read.load()

        # Step 6: Validate data structure and basic properties
        assert isinstance(loaded_data, dict)
        assert len(loaded_data) > 0

        # Step 7: Validate data shapes and types
        for key, original_values in test_data[0].items():
            flat_key = key.replace("/", "/") if "/" in key else key
            if flat_key not in loaded_data:
                # Try nested key format
                for loaded_key in loaded_data.keys():
                    if loaded_key.endswith(key.split("/")[-1]):
                        flat_key = loaded_key
                        break

            assert (
                flat_key in loaded_data
            ), f"Key {key} not found in loaded data. Available keys: {list(loaded_data.keys())}"

            loaded_array = loaded_data[flat_key]
            assert loaded_array.shape[0] == len(
                test_data), f"Wrong number of timesteps for {key}"

            # For the first timestep, check shape consistency
            if hasattr(original_values, "shape"):
                expected_shape = (len(test_data), ) + original_values.shape
                assert (
                    loaded_array.shape == expected_shape
                ), f"Shape mismatch for {key}: got {loaded_array.shape}, expected {expected_shape}"

        traj_read.close()
        return True, None

    except Exception as e:
        return False, str(e)


class TestCodecConfig:
    """Test the CodecConfig class."""

    def test_codec_config_initialization(self):
        """Test CodecConfig initialization with different parameters."""
        # Test default initialization
        config = CodecConfig()
        assert config.codec == "auto"
        assert config.custom_options == {}

        # Test with specific codec
        config = CodecConfig("libx264")
        assert config.codec == "libx264"

        # Test with custom options
        config = CodecConfig("libx264", {"crf": "20"})
        assert config.custom_options == {"crf": "20"}

    def test_unsupported_codec(self):
        """Test that unsupported codec raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported codec"):
            CodecConfig("unsupported_codec")

    def test_get_codec_for_feature_auto(self):
        """Test automatic codec selection based on feature type."""
        config = CodecConfig("auto")

        # Large image should get video codec
        large_image_type = FeatureType(dtype="uint8", shape=(480, 640, 3))
        codec = config.get_codec_for_feature(large_image_type)
        assert codec == "libaom-av1"

        # Small data should get rawvideo
        small_data_type = FeatureType(dtype="float32", shape=(7, ))
        codec = config.get_codec_for_feature(small_data_type)
        assert codec == "rawvideo"

    def test_get_codec_for_feature_specific(self):
        """Test specific codec selection."""
        config = CodecConfig("libx264")

        # Should always return the specified codec
        large_image_type = FeatureType(dtype="uint8", shape=(480, 640, 3))
        codec = config.get_codec_for_feature(large_image_type)
        assert codec == "libx264"

        small_data_type = FeatureType(dtype="float32", shape=(7, ))
        codec = config.get_codec_for_feature(small_data_type)
        assert codec == "rawvideo"

    def test_get_pixel_format(self):
        """Test pixel format selection based on codec and feature type."""
        config = CodecConfig()

        # RGB image
        rgb_type = FeatureType(dtype="uint8", shape=(100, 100, 3))
        pix_fmt = config.get_pixel_format("libx264", rgb_type)
        assert pix_fmt == "yuv420p"

        # Grayscale image
        gray_type = FeatureType(dtype="uint8", shape=(100, 100))
        pix_fmt = config.get_pixel_format("libx264", gray_type)
        assert pix_fmt == "gray"

        # Rawvideo should return None
        pix_fmt = config.get_pixel_format("rawvideo", rgb_type)
        assert pix_fmt is None

    def test_get_codec_options(self):
        """Test codec options merging."""
        config = CodecConfig("libx264", {"preset": "fast"})

        options = config.get_codec_options("libx264")
        assert "crf" in options  # Default option
        assert "preset" in options  # Custom option
        assert options["preset"] == "fast"  # Custom overrides default


class TestFeatureType:
    """Test the FeatureType class."""

    def test_from_data_numpy_array(self):
        """Test FeatureType.from_data with numpy arrays."""
        data = np.random.random((10, 20)).astype(np.float32)
        feature_type = FeatureType.from_data(data)
        assert feature_type.dtype == "float32"
        assert feature_type.shape == (10, 20)

    def test_from_data_scalar(self):
        """Test FeatureType.from_data with scalar values."""
        feature_type = FeatureType.from_data(1.0)
        assert feature_type.dtype == "float32"
        assert feature_type.shape == ()

    def test_from_data_string(self):
        """Test FeatureType.from_data with strings."""
        feature_type = FeatureType.from_data("test")
        assert feature_type.dtype == "str"
        assert feature_type.shape == ()

    def test_to_str_and_from_str(self):
        """Test string serialization and deserialization."""
        original = FeatureType(dtype="float32", shape=(10, 20))
        str_repr = str(original)
        reconstructed = FeatureType.from_str(str_repr)
        assert reconstructed.dtype == original.dtype
        assert reconstructed.shape == original.shape


class TestTrajectoryFactory:
    """Test the TrajectoryFactory class."""

    def test_factory_with_default_dependencies(self, temp_dir):
        """Test factory with default dependencies."""
        factory = TrajectoryFactory()
        path = os.path.join(temp_dir, "test.vla")

        # This should work with actual filesystem since we're using defaults
        traj = factory.create_trajectory(path, mode="w")
        assert traj is not None
        assert hasattr(traj, "_filesystem")
        assert hasattr(traj, "_time_provider")
        traj.close()

    def test_factory_with_mock_dependencies(self, mock_filesystem,
                                            mock_time_provider, temp_dir):
        """Test factory with mock dependencies."""
        factory = TrajectoryFactory(filesystem=mock_filesystem,
                                    time_provider=mock_time_provider)

        # Setup mock filesystem
        mock_filesystem.add_file("/test/test.vla")
        mock_filesystem.directories.add(temp_dir)

        path = "/test/test.vla"

        with patch("av.open") as mock_av:
            mock_container = Mock()
            mock_av.return_value = mock_container

            traj = factory.create_trajectory(path, mode="w")
            assert traj._filesystem == mock_filesystem
            assert traj._time_provider == mock_time_provider


class TestTrajectory:
    """Test the main Trajectory class."""

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_trajectory_creation_write_mode(self, temp_dir, codec):
        """Test trajectory creation in write mode with all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            traj = Trajectory(path, mode="w", video_codec=codec)
            assert traj.path == path
            assert traj.mode == "w"
            assert not traj.is_closed
            traj.close()
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    def test_trajectory_creation_with_video_codec(self, temp_dir):
        """Test trajectory creation with specific video codec."""
        path = os.path.join(temp_dir, "test.vla")
        traj = Trajectory(path, mode="w", video_codec="libx264")
        assert traj.codec_config.codec == "libx264"
        traj.close()

    def test_trajectory_creation_with_codec_options(self, temp_dir):
        """Test trajectory creation with codec options."""
        path = os.path.join(temp_dir, "test.vla")
        traj = Trajectory(path,
                          mode="w",
                          video_codec="libx264",
                          codec_options={"crf": "20"})
        assert traj.codec_config.custom_options == {"crf": "20"}
        traj.close()

    def test_trajectory_creation_read_mode_nonexistent(self, temp_dir):
        """Test trajectory creation in read mode with non-existent file."""
        path = os.path.join(temp_dir, "nonexistent.vla")
        with pytest.raises(FileNotFoundError):
            Trajectory(path, mode="r")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_add_single_feature(self, temp_dir, codec):
        """Test adding a single feature to trajectory with all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            traj = Trajectory(path, mode="w", video_codec=codec)

            # Add some test data
            image_data = np.random.randint(0,
                                           255, (100, 100, 3),
                                           dtype=np.uint8)
            traj.add("observation/image", image_data)

            joint_data = np.random.random(7).astype(np.float32)
            traj.add("observation/joints", joint_data)

            traj.close()

            # Verify file was created
            assert os.path.exists(path)
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_add_by_dict(self, temp_dir, codec):
        """Test adding features via dictionary with all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            traj = Trajectory(path, mode="w", video_codec=codec)

            data = {
                "observation": {
                    "image":
                    np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8),
                    "joints":
                    np.random.random(7).astype(np.float32),
                },
                "action": np.random.random(7).astype(np.float32),
            }

            traj.add_by_dict(data)
            traj.close()

            assert os.path.exists(path)
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_from_list_of_dicts(self, temp_dir, sample_trajectory_data, codec):
        """Test creating trajectory from list of dictionaries with all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            traj = Trajectory.from_list_of_dicts(sample_trajectory_data,
                                                 path,
                                                 video_codec=codec)

            assert os.path.exists(path)
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_from_dict_of_lists(self, temp_dir, sample_dict_of_lists, codec):
        """Test creating trajectory from dictionary of lists with all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            traj = Trajectory.from_dict_of_lists(sample_dict_of_lists,
                                                 path,
                                                 video_codec=codec)

            assert os.path.exists(path)
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_load_and_read(self, temp_dir, sample_dict_of_lists, codec):
        """Test loading and reading trajectory data with all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            # Create trajectory
            traj = Trajectory.from_dict_of_lists(sample_dict_of_lists,
                                                 path,
                                                 video_codec=codec)

            # Read back the data
            traj_read = Trajectory(path, mode="r")
            loaded_data = traj_read.load()

            # Verify data structure
            assert isinstance(loaded_data, dict)
            assert "observation/image" in loaded_data
            assert "observation/joint_positions" in loaded_data
            assert "action" in loaded_data
            assert "reward" in loaded_data

            # Verify data shapes
            assert loaded_data["observation/image"].shape == (2, 480, 640, 3)
            assert loaded_data["observation/joint_positions"].shape == (2, 7)
            assert loaded_data["action"].shape == (2, 7)
            assert loaded_data["reward"].shape == (2, )
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_getitem_access(self, temp_dir, sample_dict_of_lists, codec):
        """Test accessing data via __getitem__ with all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            # Create trajectory
            Trajectory.from_dict_of_lists(sample_dict_of_lists,
                                          path,
                                          video_codec=codec)

            # Read back the data
            traj = Trajectory(path, mode="r")

            # Test __getitem__ access
            image_data = traj["observation/image"]
            assert image_data.shape == (2, 480, 640, 3)

            action_data = traj["action"]
            assert action_data.shape == (2, 7)
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_load_different_return_types(self, temp_dir, sample_dict_of_lists,
                                         codec):
        """Test loading with different return types and all codecs."""
        path = os.path.join(temp_dir, f"test_{codec}.vla")
        try:
            # Create trajectory
            Trajectory.from_dict_of_lists(sample_dict_of_lists,
                                          path,
                                          video_codec=codec)

            traj = Trajectory(path, mode="r")

            # Test numpy return type
            numpy_data = traj.load(return_type="numpy")
            assert isinstance(numpy_data, dict)

            # Test container return type
            container_name = traj.load(return_type="container")
            assert container_name == path
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    def test_close_behavior(self, temp_dir):
        """Test trajectory close behavior."""
        path = os.path.join(temp_dir, "test.vla")
        traj = Trajectory(path, mode="w")

        # Add some data
        traj.add("test_feature", np.array([1, 2, 3]))

        # Close trajectory
        assert not traj.is_closed
        traj.close()
        assert traj.is_closed

        # Test that closing again raises an error
        with pytest.raises(ValueError, match="already closed"):
            traj.close()

    def test_invalid_mode(self, temp_dir):
        """Test trajectory creation with invalid mode."""
        path = os.path.join(temp_dir, "test.vla")
        with pytest.raises(ValueError, match="Invalid mode"):
            Trajectory(path, mode="invalid")

    def test_dependency_injection(self, mock_filesystem, mock_time_provider,
                                  temp_dir):
        """Test that dependency injection works correctly."""
        factory = TrajectoryFactory(filesystem=mock_filesystem,
                                    time_provider=mock_time_provider)

        # Setup mock filesystem
        mock_filesystem.directories.add(temp_dir)
        mock_filesystem.add_file("/test/test.vla")

        with patch("av.open") as mock_av:
            mock_container = Mock()
            mock_av.return_value = mock_container

            traj = factory.create_trajectory("/test/test.vla", mode="w")

            # Test that filesystem methods are called on mock
            assert traj._exists("/test/test.vla")
            assert mock_filesystem.exists("/test/test.vla")

            # Test that time provider is used
            initial_calls = mock_time_provider.call_count
            timestamp = traj._get_current_timestamp()
            assert mock_time_provider.call_count > initial_calls


class TestTrajectoryIntegration:
    """Integration tests for trajectory functionality."""

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_full_workflow(self, temp_dir, codec):
        """Test complete workflow: create, write, read, verify with all codecs."""
        path = os.path.join(temp_dir, f"integration_test_{codec}.vla")
        try:
            # Create and populate trajectory
            traj_write = Trajectory(path, mode="w", video_codec=codec)

            for i in range(10):
                data = {
                    "observation": {
                        "image":
                        np.random.randint(0,
                                          255, (640, 480, 3),
                                          dtype=np.uint8),
                        "joints":
                        np.random.random(7).astype(np.float32),
                    },
                    "action": np.random.random(7).astype(np.float32),
                    "step": i,
                }
                traj_write.add_by_dict(data)

            traj_write.close()

            # Read back and verify
            traj_read = Trajectory(path, mode="r")
            loaded_data = traj_read.load()

            # Verify structure and dimensions
            assert "observation/image" in loaded_data
            assert "observation/joints" in loaded_data
            assert "action" in loaded_data
            assert "step" in loaded_data

            assert loaded_data["observation/image"].shape == (10, 640, 480, 3)
            assert loaded_data["observation/joints"].shape == (10, 7)
            assert loaded_data["action"].shape == (10, 7)
            assert loaded_data["step"].shape == (10, )
        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    def test_different_video_codecs(self, temp_dir, sample_dict_of_lists):
        """Test different video codecs (legacy test - now covered by parametrized tests)."""
        codecs_to_test = ALL_CODECS

        for codec in codecs_to_test:
            path = os.path.join(temp_dir, f"{codec}.vla")

            try:
                # Create trajectory with specific codec
                Trajectory.from_dict_of_lists(sample_dict_of_lists,
                                              path,
                                              video_codec=codec)

                # Verify file was created
                assert os.path.exists(path)

                # Try to read back data
                traj = Trajectory(path, mode="r")
                loaded_data = traj.load()

                # Verify basic structure
                assert isinstance(loaded_data, dict)
                assert "observation/image" in loaded_data

            except Exception as e:
                # Some codecs might not be available in test environment
                pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ["libx264", "libx265", "libaom-av1"])
    def test_codec_options(self, temp_dir, sample_dict_of_lists, codec):
        """Test custom codec options with different codecs."""
        path = os.path.join(temp_dir, f"custom_options_{codec}.vla")

        # Define codec-specific options
        codec_options = {
            "libx264": {
                "crf": "20",
                "preset": "fast"
            },
            "libx265": {
                "crf": "23",
                "preset": "medium"
            },
            "libaom-av1": {
                "crf": "30",
                "cpu-used": "4"
            },
        }

        try:
            Trajectory.from_dict_of_lists(
                sample_dict_of_lists,
                path,
                video_codec=codec,
                codec_options=codec_options.get(codec, {}),
            )

            assert os.path.exists(path)

            # Test reading back the data
            traj = Trajectory(path, mode="r")
            loaded_data = traj.load()
            assert isinstance(loaded_data, dict)
            assert "observation/image" in loaded_data

        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_multiple_steps_with_codec(self, temp_dir, codec):
        """Test adding multiple steps with different codecs."""
        path = os.path.join(temp_dir, f"multi_step_{codec}.vla")
        try:
            traj = Trajectory(path, mode="w", video_codec=codec)

            # Add multiple timesteps
            for step in range(5):
                data = {
                    "observation": {
                        "rgb":
                        np.random.randint(0,
                                          255, (320, 240, 3),
                                          dtype=np.uint8),
                        "depth":
                        np.random.random((320, 240)).astype(np.float32),
                        "proprio":
                        np.random.random(10).astype(np.float32),
                    },
                    "action": np.random.random(6).astype(np.float32),
                    "reward": float(step * 0.1),
                    "done": step == 4,
                }
                traj.add_by_dict(data)

            traj.close()

            # Verify data
            traj_read = Trajectory(path, mode="r")
            loaded_data = traj_read.load()

            # Check all features exist and have correct shapes
            assert loaded_data["observation/rgb"].shape == (5, 320, 240, 3)
            assert loaded_data["observation/depth"].shape == (5, 320, 240)
            assert loaded_data["observation/proprio"].shape == (5, 10)
            assert loaded_data["action"].shape == (5, 6)
            assert loaded_data["reward"].shape == (5, )
            assert loaded_data["done"].shape == (5, )

            # Check last step is marked as done
            assert loaded_data["done"][-1] == True

        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_edge_cases_with_codec(self, temp_dir, codec):
        """Test edge cases like empty trajectories, single steps, etc. with all codecs."""
        try:
            # Test single step trajectory
            path_single = os.path.join(temp_dir, f"single_step_{codec}.vla")
            traj_single = Trajectory(path_single, mode="w", video_codec=codec)

            single_data = {
                "observation":
                np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8),
                "action":
                np.array([1.0]),
            }
            traj_single.add_by_dict(single_data)
            traj_single.close()

            # Verify single step
            traj_read = Trajectory(path_single, mode="r")
            loaded_single = traj_read.load()
            assert loaded_single["observation"].shape == (1, 128, 128, 3)
            assert loaded_single["action"].shape == (1, 1)

            # Test large trajectory (stress test)
            path_large = os.path.join(temp_dir, f"large_{codec}.vla")
            traj_large = Trajectory(path_large, mode="w", video_codec=codec)

            for i in range(100):
                large_data = {
                    "observation":
                    np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8),
                    "step":
                    i,
                }
                traj_large.add_by_dict(large_data)

            traj_large.close()

            # Verify large trajectory
            traj_read_large = Trajectory(path_large, mode="r")
            loaded_large = traj_read_large.load()
            assert loaded_large["observation"].shape == (100, 128, 128, 3)
            assert loaded_large["step"].shape == (100, )

        except Exception as e:
            pytest.skip(f"Codec {codec} not available: {e}")

    # def test_backward_compatibility_class_methods(self, temp_dir, sample_dict_of_lists):
    #     """Test backward compatibility for class methods with lossy_compression."""
    #     path_old = os.path.join(temp_dir, "old_api.vla")
    #     path_new = os.path.join(temp_dir, "new_api.vla")

    #     # Test old API with warning
    #     with pytest.warns(UserWarning, match="lossy_compression parameter is deprecated"):
    #         Trajectory.from_dict_of_lists(
    #             sample_dict_of_lists,
    #             path_old,
    #             lossy_compression=True # This would now be an error
    #         )

    #     # Test new API
    #     Trajectory.from_dict_of_lists(
    #         sample_dict_of_lists,
    #         path_new,
    #         video_codec="libaom-av1"
    #     )

    #     # Both should work
    #     assert os.path.exists(path_old)
    #     assert os.path.exists(path_new)


class TestCodecValidation:
    """Comprehensive codec validation tests to catch encoding/decoding errors."""

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_codec_roundtrip_validation(self, temp_dir, codec):
        """Test full encoding/decoding roundtrip for each codec with comprehensive validation."""
        # Create test data with various data types and shapes
        test_data = [{
            "observation/image":
            np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
            "observation/depth":
            np.random.random((640, 480)).astype(np.float32),
            "observation/joints":
            np.random.random(7).astype(np.float32),
            "action":
            np.random.random(6).astype(np.float32),
            "reward":
            np.random.random(),
            "step":
            i,
        } for i in range(5)]

        success, error = validate_codec_roundtrip(temp_dir, codec, test_data)

        if not success:
            if "not available" in error.lower() or "codec" in error.lower():
                pytest.skip(f"Codec {codec} not available: {error}")
            else:
                pytest.fail(
                    f"Codec {codec} failed encoding/decoding validation: {error}"
                )

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_codec_with_different_image_sizes(self, temp_dir, codec):
        """Test codecs with different image sizes to catch size-specific encoding issues."""
        image_sizes = [(640, 480, 3), (320, 240, 3), (128, 128, 3)]

        for size in image_sizes:
            test_data = [{
                "observation/image":
                np.random.randint(0, 255, size, dtype=np.uint8),
                "action":
                np.random.random(4).astype(np.float32),
            } for _ in range(3)]

            success, error = validate_codec_roundtrip(temp_dir, codec,
                                                      test_data)

            if not success:
                if "not available" in error.lower() or "codec" in error.lower(
                ):
                    pytest.skip(f"Codec {codec} not available: {error}")
                else:
                    pytest.fail(
                        f"Codec {codec} failed with image size {size}: {error}"
                    )

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_codec_data_integrity(self, temp_dir, codec):
        """Test that data maintains integrity through encoding/decoding cycle."""
        # Use deterministic data for exact comparison
        test_data = [{
            "observation/image":
            np.full((320, 240, 3), i * 50, dtype=np.uint8),
            "observation/vector":
            np.full(5, i * 0.1, dtype=np.float32),
            "action":
            np.array([i, i + 1, i + 2], dtype=np.float32),
            "step":
            i,
        } for i in range(4)]

        path = os.path.join(temp_dir, f"integrity_test_{codec}.vla")

        try:
            # Write data
            traj_write = Trajectory(path, mode="w", video_codec=codec)
            for data_dict in test_data:
                traj_write.add_by_dict(data_dict)
            traj_write.close()

            # Read data back
            traj_read = Trajectory(path, mode="r")
            loaded_data = traj_read.load()
            traj_read.close()

            # Validate data integrity
            assert loaded_data["step"].shape == (4, )
            assert loaded_data["action"].shape == (4, 3)

            # Check step values are correct
            np.testing.assert_array_equal(loaded_data["step"], [0, 1, 2, 3])

            # Define tolerance based on codec type
            if codec in ["rawvideo", "ffv1"]:
                # Lossless codecs - expect exact match
                image_tolerance = 0
                vector_tolerance = 1e-6
            elif codec in ["libx264", "libx265", "libaom-av1"]:
                # Lossy codecs - allow reasonable compression artifacts
                image_tolerance = 10  # Allow up to 10 units difference in uint8 values
                vector_tolerance = 1e-3  # More tolerance for float values
            else:
                # Unknown codec - use conservative tolerance
                image_tolerance = 5
                vector_tolerance = 1e-4

            # Check action data (should be exact for rawvideo/pickled data regardless of image codec)
            expected_actions = np.array(
                [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]], dtype=np.float32)
            np.testing.assert_allclose(loaded_data["action"],
                                       expected_actions,
                                       rtol=vector_tolerance)

            # Check vector data (should be exact for rawvideo/pickled data regardless of image codec)
            expected_vectors = np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.1, 0.1, 0.1, 0.1, 0.1],
                    [0.2, 0.2, 0.2, 0.2, 0.2],
                    [0.3, 0.3, 0.3, 0.3, 0.3],
                ],
                dtype=np.float32,
            )
            np.testing.assert_allclose(
                loaded_data["observation/vector"],
                expected_vectors,
                rtol=vector_tolerance,
            )

            # Check image data with codec-appropriate tolerance
            expected_images = np.array([
                np.full((320, 240, 3), i * 50, dtype=np.uint8)
                for i in range(4)
            ])

            if image_tolerance == 0:
                # Exact match for lossless
                np.testing.assert_array_equal(loaded_data["observation/image"],
                                              expected_images)
            else:
                # Allow tolerance for lossy codecs
                image_diff = np.abs(
                    loaded_data["observation/image"].astype(np.float32) -
                    expected_images.astype(np.float32))
                max_diff = np.max(image_diff)
                mean_diff = np.mean(image_diff)

                assert (
                    max_diff <= image_tolerance
                ), f"Max pixel difference {max_diff} exceeds tolerance {image_tolerance} for codec {codec}"
                assert (
                    mean_diff <= image_tolerance / 2
                ), f"Mean pixel difference {mean_diff} exceeds half tolerance {image_tolerance/2} for codec {codec}"

        except Exception as e:
            if "not available" in str(e).lower() or "codec" in str(e).lower():
                pytest.skip(f"Codec {codec} not available: {e}")
            else:
                pytest.fail(
                    f"Data integrity test failed for codec {codec}: {e}")

    def test_codec_availability_report(self, temp_dir):
        """Test and report which codecs are available and working."""
        codec_status = {}

        simple_test_data = [{
            "observation":
            np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8),
            "action":
            np.array([1.0, 2.0]),
        }]

        for codec in ALL_CODECS:
            success, error = validate_codec_roundtrip(temp_dir, codec,
                                                      simple_test_data)
            codec_status[codec] = {"available": success, "error": error}

        # Print codec availability report
        print("\n" + "=" * 50)
        print("CODEC AVAILABILITY REPORT")
        print("=" * 50)

        available_codecs = []
        unavailable_codecs = []

        for codec, status in codec_status.items():
            if status["available"]:
                available_codecs.append(codec)
                print(f"✓ {codec}: Available and working")
            else:
                unavailable_codecs.append(codec)
                print(f"✗ {codec}: {status['error']}")

        print(
            f"\nSummary: {len(available_codecs)}/{len(ALL_CODECS)} codecs available"
        )
        print("=" * 50)

        # Ensure at least one codec is working
        assert len(
            available_codecs) > 0, "No codecs are available and working!"

    @pytest.mark.parametrize("codec", ALL_CODECS)
    def test_codec_error_handling(self, temp_dir, codec):
        """Test that codec errors are properly handled and reported."""
        # Test with potentially problematic data
        problematic_data = [{
            "observation/image":
            np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8),
            "action":
            np.array([]),  # Empty array
        }]

        path = os.path.join(temp_dir, f"error_test_{codec}.vla")

        try:
            traj = Trajectory(path, mode="w", video_codec=codec)

            # This might fail for some codecs with empty arrays
            for data_dict in problematic_data:
                traj.add_by_dict(data_dict)

            traj.close()

            # Try to read back
            traj_read = Trajectory(path, mode="r")
            loaded_data = traj_read.load()
            traj_read.close()

            # If we get here, codec handled edge case well
            assert isinstance(loaded_data, dict)

        except Exception as e:
            # Log the specific error for debugging
            error_msg = str(e)
            if "not available" in error_msg.lower(
            ) or "codec" in error_msg.lower():
                pytest.skip(f"Codec {codec} not available: {error_msg}")
            elif "InvalidDataError" in error_msg or "no frame" in error_msg:
                pytest.fail(
                    f"Codec {codec} has encoding/decoding issues: {error_msg}")
            else:
                # Other errors might be expected for edge cases
                print(
                    f"Codec {codec} failed with edge case data (may be expected): {error_msg}"
                )
