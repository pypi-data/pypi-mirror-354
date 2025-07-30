import svetlanna.elements
from svetlanna.logging import agr_short_description
from svetlanna.logging import log_message
from svetlanna.logging import forward_logging_hook, register_logging_hook
import torch
import svetlanna
import logging
import pytest


@pytest.mark.parametrize(
        'input', [
            torch.tensor([10., 10.]),
            torch.tensor(20),
            svetlanna.Parameter(11.),
            svetlanna.ConstrainedParameter(11., min_value=-10, max_value=100),
            123,
            123.,
            None
        ]
)
def test_agr_short_description(input):
    if isinstance(input, torch.Tensor):
        # test for torch.Tensor
        assert agr_short_description(input) == (
            f"{type(input)} shape={input.shape}, "
            f"dtype={input.dtype}, device={input.device}"
        )
    else:
        # test for other types
        assert agr_short_description(input) == f'{type(input)}'


def test_log_message(capfd, caplog):
    # test for 'print' type
    svetlanna.set_debug_logging(False, type='print')  # set 'print' type
    # log_message prints the message even if mode set to False!

    log_message('test message')  # print message
    out, _ = capfd.readouterr()  # read stdout

    assert out == 'test message\n'

    # test for 'logging' type
    svetlanna.set_debug_logging(False, type='logging')  # set 'logging' type

    logger = logging.getLogger('svetlanna.logging')  # get logger
    logger.setLevel(logging.DEBUG)  # set logging level to DEBUG

    log_message('test message')  # print message

    assert caplog.record_tuples == [
        ("svetlanna.logging", logging.DEBUG, "test message")
    ]


@pytest.mark.parametrize(
        'input', [
            1, 1., (1, 2), tuple()
        ]
)
@pytest.mark.parametrize(
        'output', [
            1, 1., (1, 2), tuple()
        ]
)
def test_forward_logging_hook(input, output, capfd):
    svetlanna.set_debug_logging(False, type='print')  # set 'print' type

    # test for random element ignorance
    class NotElement(torch.nn.Module):
        pass

    forward_logging_hook(NotElement(), input, output)

    out, _ = capfd.readouterr()  # read stdout
    assert out == ''

    # test for elements
    class ElementLike(svetlanna.elements.Element):
        def forward(self, *args, **kwargs):
            pass

    element = ElementLike(
        simulation_parameters=svetlanna.SimulationParameters(
            axes={
                'H': torch.linspace(-1, 1, 10),
                'W': torch.linspace(-1, 1, 10),
                'wavelength': 1.
            }
        )
    )

    forward_logging_hook(element, input, output)

    expected_out = 'The forward method of ElementLike was computed'
    input = input if isinstance(input, tuple) else (input,)
    output = output if isinstance(output, tuple) else (output,)
    for i, _input in enumerate(input):
        expected_out += f'\n   input {i}: {type(_input)}'
    for i, _output in enumerate(output):
        expected_out += f'\n   output {i}: {type(_output)}'

    out, _ = capfd.readouterr()  # read stdout
    assert out == expected_out + '\n'


@pytest.mark.parametrize(
        'input', [
            1, 1., (1, 2), tuple()
        ]
)
@pytest.mark.parametrize(
        'type_', [
            'Parameter', 'Buffer', 'Module'
        ]
)
def test_register_logging_hook(input, type_, capfd):
    svetlanna.set_debug_logging(False, type='print')  # set 'print' type

    # test for random element ignorance
    class NotElement(torch.nn.Module):
        pass

    register_logging_hook(NotElement(), 'test_name', input, type_)

    out, _ = capfd.readouterr()  # read stdout
    assert out == ''

    # test for elements
    class ElementLike(svetlanna.elements.Element):
        def forward(self, *args, **kwargs):
            pass

    element = ElementLike(
        simulation_parameters=svetlanna.SimulationParameters(
            axes={
                'H': torch.linspace(-1, 1, 10),
                'W': torch.linspace(-1, 1, 10),
                'wavelength': 1.
            }
        )
    )

    register_logging_hook(element, 'test_name', input, type_)

    expected_out = f'{type_} of {element._get_name()} was registered with name test_name:'
    expected_out += f'\n   {type(input)}'

    out, _ = capfd.readouterr()  # read stdout
    assert out == expected_out + '\n'


@pytest.mark.parametrize(
        'input', [
            1, 1., (1, 2), tuple()
        ]
)
@pytest.mark.parametrize(
        'output', [
            1, 1., (1, 2), tuple()
        ]
)
def test_set_debug_logging(input, output, capfd, caplog):
    # test wrong type
    with pytest.raises(ValueError):
        svetlanna.set_debug_logging(False, type='123')  # type: ignore

    input = input if isinstance(input, tuple) else (input,)
    output = output if isinstance(output, tuple) else (output,)

    class ElementLike(svetlanna.elements.Element):
        def __init__(
            self,
            simulation_parameters: svetlanna.SimulationParameters
        ) -> None:
            super().__init__(simulation_parameters)
            self.a = torch.nn.Module()
            self.b = svetlanna.Parameter(123.)
            self.register_buffer('c', torch.tensor(123.))

        def forward(self, *args, **kwargs):
            return output

    def run_element():
        element = ElementLike(
            simulation_parameters=svetlanna.SimulationParameters(
                axes={
                    'H': torch.linspace(-1, 1, 10),
                    'W': torch.linspace(-1, 1, 10),
                    'wavelength': 1.
                }
            )
        )
        element(*input)

    expected_output_1 = (
        "Module of ElementLike was registered with name a:\n"
        "   <class 'torch.nn.modules.module.Module'>"
    )
    expected_output_2 = (
        "Module of ElementLike was registered with name b_svtlnn_inner_parameter:\n"
        "   <class 'svetlanna.parameters.InnerParameterStorageModule'>"
    )
    expected_output_3 = (
        "Buffer of ElementLike was registered with name c:\n"
        "   <class 'torch.Tensor'> shape=torch.Size([]), dtype=torch.float32, device=cpu"
    )
    expected_output_4 = (
        "The forward method of ElementLike was computed"
    )
    for i, _input in enumerate(input):
        expected_output_4 += f'\n   input {i}: {type(_input)}'
    for i, _output in enumerate(output):
        expected_output_4 += f'\n   output {i}: {type(_output)}'

    expected_outputs = [
        expected_output_1,
        expected_output_2,
        expected_output_3,
        expected_output_4
    ]

    # test for print type
    svetlanna.set_debug_logging(True, type='print')
    run_element()
    out, _ = capfd.readouterr()  # read stdout
    assert out == '\n'.join(expected_outputs) + '\n'

    # test for print type, with disabled debug logging
    svetlanna.set_debug_logging(False, type='print')
    run_element()
    out, _ = capfd.readouterr()  # read stdout
    assert out == ''

    # test for logging type
    svetlanna.set_debug_logging(True, type='logging')
    logger = logging.getLogger('svetlanna.logging')  # get logger
    logger.setLevel(logging.DEBUG)  # set logging level to DEBUG
    run_element()
    assert caplog.record_tuples == [
        (
            "svetlanna.logging",
            logging.DEBUG,
            message
        ) for message in expected_outputs
    ]

    caplog.clear()  # clear caplog
    assert caplog.record_tuples == []

    # test for logging type, with disabled debug logging
    svetlanna.set_debug_logging(False, type='logging')
    run_element()
    assert caplog.record_tuples == []
