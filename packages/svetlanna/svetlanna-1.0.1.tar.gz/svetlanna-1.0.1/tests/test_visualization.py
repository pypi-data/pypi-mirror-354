import svetlanna
from svetlanna.visualization.widgets import default_widget_html_method
from svetlanna.visualization.widgets import generate_structure_html
from svetlanna.visualization import show_structure, show_specs
from svetlanna.visualization.widgets import draw_wavefront
from svetlanna.visualization import show_stepwise_forward
from svetlanna.specs.specs_writer import _ElementInTree
from svetlanna.visualization.widgets import SpecsWidget, StepwiseForwardWidget
import torch
import builtins
import pytest


def test_html_element():
    sim_params = svetlanna.SimulationParameters(
        {'W': torch.tensor([0]), 'H': torch.tensor([0]), 'wavelength': 1}
    )
    element = svetlanna.elements.FreeSpace(sim_params, distance=1, method='AS')

    assert element._repr_html_()


def test_default_widget_html_method():
    assert default_widget_html_method(123, 'test', 'element_type', [])


def test_generate_structure_html():
    sim_params = svetlanna.SimulationParameters(
        {'W': torch.tensor([0]), 'H': torch.tensor([0]), 'wavelength': 1}
    )
    element = svetlanna.elements.FreeSpace(sim_params, distance=1, method='AS')

    class NoWidgetHTMLElement:
        def to_specs(self):
            return []

    assert generate_structure_html(
        [
            _ElementInTree(element, 0, [
                _ElementInTree(NoWidgetHTMLElement(), 0, [])
            ])
        ]
    )


def test_show_structure(monkeypatch):
    import IPython.display

    # monkeypatch IPython.display.display
    displayed = False

    def set_displayed():
        nonlocal displayed
        displayed = True

    monkeypatch.setattr(IPython.display, 'display', lambda _: set_displayed())

    # Test if the HTML has been displayed
    displayed = False
    show_structure()
    assert displayed

    # Test if the warning displayed in the case of IPython absence
    # monkeypatching import statement
    original_import = builtins.__import__

    def import_with_no_ipython(name, *args, **kwargs):
        if name == "IPython.display":
            raise ImportError
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_with_no_ipython)

    warning_msg = "Currently only display via ipython is supported."
    with pytest.warns(UserWarning, match=warning_msg):
        displayed = False
        show_structure()
        assert not displayed


def test_show_specs():
    sim_params = svetlanna.SimulationParameters(
        {'W': torch.tensor([0]), 'H': torch.tensor([0]), 'wavelength': 1}
    )
    element = svetlanna.elements.FreeSpace(sim_params, distance=1, method='AS')

    widget = show_specs(element)
    assert isinstance(widget, SpecsWidget)
    assert len(widget.elements) == 1
    assert widget.elements[0]['name'] == 'FreeSpace'


def test_draw_wavefront():
    sim_params = svetlanna.SimulationParameters(
        {
            'W': torch.linspace(-1, 1, 10),
            'H': torch.linspace(-1, 1, 10),
            'wavelength': 1
        }
    )
    wavefront = svetlanna.Wavefront.plane_wave(sim_params)

    # Single type
    types = ('A', 'I', 'phase', 'Re', 'Im')
    for t in types:
        assert draw_wavefront(
            wavefront,
            sim_params,
            types_to_plot=(t,)
        )

    # All types
    assert draw_wavefront(
        wavefront,
        sim_params,
        types_to_plot=types
    )


def test_show_stepwise_forward():
    sim_params = svetlanna.SimulationParameters(
        {
            'W': torch.linspace(-1, 1, 10),
            'H': torch.linspace(-1, 1, 10),
            'wavelength': 1
        }
    )

    class NoneForwardElement(torch.nn.Module):
        def forward(self, x):
            return None

        def to_specs(self):
            return []

    class WrongTensorForwardElement(torch.nn.Module):
        def forward(self, x):
            return torch.tensor([1, 2, 3.])

        def to_specs(self):
            return []

    element1 = svetlanna.elements.FreeSpace(sim_params, distance=1, method='AS')
    element2 = NoneForwardElement()
    element3 = WrongTensorForwardElement()

    wavefront = svetlanna.Wavefront.plane_wave(sim_params)

    widget = show_stepwise_forward(
        element1,
        element2,
        element3,
        input=wavefront,
        simulation_parameters=sim_params
    )

    assert isinstance(widget, StepwiseForwardWidget)
    assert len(widget.elements) == 3

    element1_json = widget.elements[0]
    assert element1_json['name'] == 'FreeSpace'
    assert element1_json['output_image']

    element2_json = widget.elements[1]
    assert element2_json['name'] == 'NoneForwardElement'
    assert element2_json['output_image'] is None

    element3_json = widget.elements[2]
    assert element3_json['name'] == 'WrongTensorForwardElement'
    assert element3_json['output_image'][:1] == '\n'
