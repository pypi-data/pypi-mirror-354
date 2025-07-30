import pytest
import torch

from svetlanna.elements import Element
from svetlanna import SimulationParameters
from svetlanna.detector import Detector, DetectorProcessorClf


def test_detector_types():
    """
    Test on types for a detector.
    """
    detector = Detector(
        SimulationParameters(
            {
                'W': torch.linspace(-1e-2/2, 1e-2/2, 5),
                'H': torch.linspace(-1e-2/2, 1e-2/2, 5),
                'wavelength': 1e-6
            }
        )
    )
    assert isinstance(detector, torch.nn.Module)
    assert isinstance(detector, Element)


@pytest.mark.parametrize(
    "x_size, y_size, x_nodes, y_nodes, wavelength", [
        (10e-2, 10e-2, 10, 10, 1e-6),
        (15e-2, 20e-2, 15, 20, 1e-6),
    ]
)
def test_detector_intensity(x_size, y_size, x_nodes, y_nodes, wavelength):
    """
    Check a detector that returns a map of intensities (func='intensity').

    Parameters
    ----------
    x_size, y_size : float
    x_nodes, y_nodes : int
        Simulation parameters for detector.
    """
    detector = Detector(
        SimulationParameters(
            {
                'W': torch.linspace(-x_size/2, x_size/2, x_nodes),
                'H': torch.linspace(-y_size/2, y_size/2, y_nodes),
                'wavelength': wavelength
            }
        ),
        func='intensity'
    )
    input_field = torch.rand(size=[y_nodes, x_nodes])

    detector_image = detector.forward(input_field)
    assert input_field.shape == detector_image.shape
    assert torch.allclose(detector_image, input_field.abs().pow(2))


@pytest.mark.parametrize(
    "num_classes, detector_x, expected_mask", [
        (4, 8, [[0, 0, 1, 1, 2, 2, 3, 3]]),         # num_classes - even, detector_x - even
        (2, 4, [[0, 0, 1, 1]]),
        (2, 7, [[0, 0, 0, -1, 1, 1, 1]]),           # num_classes - even, detector_x - odd
        (4, 7, [[-1, 0, 1, -1, 2, 3, -1]]),
        (3, 8, [[-1, 0, 0, 1, 1, 2, 2, -1]]),       # num_classes - odd, detector_x - even
        (3, 10, [[0, 0, 0, 1, 1, 1, 1, 2, 2, 2]]),
        (3, 7, [[0, 0, 1, 1, 1, 2, 2]]),            # num_classes - odd, detector_x - odd
        (5, 7, [[-1, 0, 1, 2, 3, 4, -1]]),
        (5, 11, [[0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4]]),
    ]
)
def test_detector_segmentation_strips(num_classes, detector_x, expected_mask):
    """
    Test of a method of DetectorProcessorClf for strips segmentation of a detector by classes zones.
    ...

    Parameters
    ----------
    num_classes
        Number of classes.
    detector_x
        Horizontal size of a detector.
    expected_mask
        Expected segmentation by strips.
    """
    processor = DetectorProcessorClf(
        num_classes=num_classes,
        simulation_parameters=SimulationParameters(
            {
                'W': torch.linspace(-1e-2/2, 1e-2/2, detector_x),
                'H': torch.linspace(0, 0, 1),
                'wavelength': 500e-6
            }
        )
    )
    assert isinstance(processor, torch.nn.Module)

    # segmentation = processor.detector_segmentation(torch.Size([1, detector_x]))

    for ind_class in range(num_classes):  # check if all classes zones are marked
        assert ind_class in processor.segmented_detector

    assert torch.allclose(processor.segmented_detector, torch.tensor(expected_mask, dtype=torch.int32))


@pytest.mark.parametrize(
    "num_classes, segmented_detector, expected_weights", [
        (2, [[0, 0, 1, 1, 0, 1, 0, 0]], [[3 / 5, 1.0]]),
        (3, [[-1, -1, 0, 0, 0, 1, 2, 0, 1, 2, 2, 2, -1, -1]], [[0.5, 1.0, 0.5]]),
        (4,
         [[-1, -1, 1,  1,   -1, -1,  3,  3],
          [0,  0,  -1, -1,  2,  2,   -1, -1]],
         [[1.0, 1.0, 1.0, 1.0]]
         ),
    ]
)
def test_detector_weight_segments(num_classes, segmented_detector, expected_weights):
    """
    Test of a method of DetectorProcessorClf for weighting classes segments.
    ...

    Parameters
    ----------
    num_classes
        Number of classes.
    segmented_detector
        A segmented detector.
    expected_weights
        Expected weights for segments.
    """
    segmented_detector_tensor = torch.tensor(segmented_detector, dtype=torch.int32)
    all_detector_size = segmented_detector_tensor.size()

    processor = DetectorProcessorClf(
        num_classes=num_classes,
        simulation_parameters=SimulationParameters(
            {
                'W': torch.linspace(-1e-2 / 2, 1e-2 / 2, all_detector_size[1]),
                'H': torch.linspace(-1e-2 / 2, 1e-2 / 2, all_detector_size[0]),
                'wavelength': 500e-6
            }
        ),
        segmented_detector=segmented_detector_tensor,
    )
    assert torch.allclose(processor.segments_weights, torch.tensor(expected_weights))

    # probabilities are same for a mono-value detector image
    detector_data = torch.ones(size=segmented_detector_tensor.shape)
    assert torch.unique(processor.forward(detector_data)).shape[0] == 1


@pytest.mark.parametrize(
    "num_classes, segmented_detector, batch_detector_data, expected_probas", [
        (
                2,
                [[0, 0], [1, 1]],
                [
                    [[0.00, 0.00], [1.00, 0.00]],
                    [[0.10, 0.00], [0.00, 0.90]],
                    [[0.22, 0.00], [0.30, 0.48]]
                ],
                [
                    [0.00, 1.00],
                    [0.10, 0.90],
                    [0.22, 0.78]
                ]
         ),
    ]
)
def test_detector_batch_forward(num_classes, segmented_detector, batch_detector_data, expected_probas):
    """
    Test of a method of DetectorProcessorClf for calculating probabilities for a batch.
    ...

    Parameters
    ----------
    num_classes
        Number of classes.
    segmented_detector
        A segmented detector.
    batch_detector_data
        A batch of a detector data.
    expected_probas
        Expected probabilities of classes.
    """
    batch_detector_data = torch.tensor(batch_detector_data)

    segmented_detector_tensor = torch.tensor(segmented_detector, dtype=torch.int32)
    all_detector_size = segmented_detector_tensor.size()

    processor = DetectorProcessorClf(
        num_classes=num_classes,
        simulation_parameters=SimulationParameters(
            {
                'W': torch.linspace(-1e-2 / 2, 1e-2 / 2, all_detector_size[1]),
                'H': torch.linspace(-1e-2 / 2, 1e-2 / 2, all_detector_size[0]),
                'wavelength': 500e-6
            }
        ),
        segmented_detector=segmented_detector_tensor,
    )

    # calculate probabilities
    probas = processor.batch_forward(batch_detector_data)

    assert torch.allclose(probas, torch.tensor(expected_probas))


@pytest.mark.parametrize(
    "num_classes, segments_zone_size, segmented_detector", [
        (
                2,
                [2, 2],
                [
                    [-1, -1, -1, -1],
                    [-1,  0,  1, -1],
                    [-1,  0,  1, -1],
                    [-1, -1, -1, -1]
                ]
         ),
    ]
)
def test_detector_segmentation_for_aperture(num_classes, segments_zone_size, segmented_detector):
    """
    Test of a feature of DetectorProcessorClf that extends segmented detector sizes to match SimulationParameters.
    ...

    Parameters
    ----------
    num_classes
        Number of classes.
    segments_zone_size
        Shape of the cenral part of a detector that must be segmented.
    segmented_detector
        A segmented detector - goal.
    """

    segmented_detector_tensor = torch.tensor(segmented_detector, dtype=torch.int32)
    all_detector_size = segmented_detector_tensor.size()

    processor = DetectorProcessorClf(
        num_classes=num_classes,
        simulation_parameters=SimulationParameters(
            {
                'W': torch.linspace(-1e-2 / 2, 1e-2 / 2, all_detector_size[1]),
                'H': torch.linspace(-1e-2 / 2, 1e-2 / 2, all_detector_size[0]),
                'wavelength': 500e-6
            }
        ),
        segments_zone_size=torch.Size(segments_zone_size),
    )

    assert torch.allclose(processor.segmented_detector, segmented_detector_tensor)


def test_detector_device():
    """
    A simple test of a method .to() and a property .device of DetectorProcessorClf.
    """

    processor = DetectorProcessorClf(
        num_classes=2,
        simulation_parameters=SimulationParameters(
            {
                'W': torch.linspace(-1e-2 / 2, 1e-2 / 2, 5),
                'H': torch.linspace(-1e-2 / 2, 1e-2 / 2, 5),
                'wavelength': 500e-6
            }
        ),
    )

    processor_2 = processor.to('cpu')
    assert isinstance(processor_2, DetectorProcessorClf)

    # available device?
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if device == torch.device('cpu'):
        device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

    processor_3 = processor.to(device)
    device_3 = processor_3.device
    assert isinstance(processor_3, DetectorProcessorClf)
    assert device_3 == device
