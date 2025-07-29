import reflex as rx
from reflex_nova.components.model.units import Units, u
from reflex_nova.components.model.fields import IndependentVar, DependentVar
from reflex_nova.components.model.nomenclature import BaseNomenclature
from reflex_nova.components.reflex.components import input_with_units, output_with_units

from reflex_nova import TopologicalSolver

mass = Units(
    si=u.kilogram,
    imp=u.kilogram,
    opts=[u.kilogram, u.pound],
)

area = Units(
    si=u.meter**2,
    imp=u.foot**2,
    opts=[u.meter**2],
)

u_1 = Units(
    si=u.meter**2/u.kilogram**(594/1000),
    imp=u.inch,
    # imp=u.feet**2/u.pound**(594/1000),
    opts=[u.meter**2/u.kilogram**(594/1000)],
)

u_2 = Units(
    si=u.meter**2/u.kilogram**(762/1000),
    imp=u.inch,
    # imp=u.feet**2/u.pound**(762/1000),
    opts=[u.meter**2/u.kilogram**(762/1000)],
)

class FrontalArea(BaseNomenclature):
    m = IndependentVar(
        sym="m",
        name="Body Mass",
        value=70,
        unit=mass,
        doc="Body mass of the cyclist",
    )

    C_tops = IndependentVar(
        sym="C_tops",
        name="Constant (Tops)",
        value=0.04038,
        unit=u_1,
        doc="Constant for tops position",
    )
    C_hoods = IndependentVar(
        sym="C_hoods",
        name="Constant (Hoods)",
        value=0.04324,
        unit=u_1,
        doc="Constant for hoods position",
    )
    C_drops = IndependentVar(
        sym="C_drops",
        name="Constant (Drops)",
        value=0.04091,
        unit=u_1,
        doc="Constant for drops position",
    )
    C_drops_low = IndependentVar(
        sym="C_drops_low",
        name="Constant (Drops Low)",
        value=0.03534,
        unit=u_1,
        doc="Constant for low drops position",
    )
    C_aero = IndependentVar(
        sym="C_aero",
        name="Constant (Aero)",
        value=0.0163,
        unit=u_2,
        doc="Constant for aero position",
    )

    A_tops = DependentVar(
        sym="A_tops",
        name="Frontal Area (Tops)",
        eqn="{A_tops} == {C_tops}*{m}**0.594",
        unit=area,
        doc="Frontal area when the cyclist is in the tops position",
    )

    A_hoods = DependentVar(
        sym="A_hoods",
        name="Frontal Area (Hoods)",
        eqn="{A_hoods} == {C_hoods}*{m}**0.594",
        unit=area,
        doc="Frontal area when the cyclist is in the hoods position",
    )

    A_drops = DependentVar(
        sym="A_drops",
        name="Frontal Area (Drops)",
        eqn="{A_drops} == {C_drops}*{m}**0.594",
        unit=area,
        doc="Frontal area when the cyclist is in the drops position",
    )

    A_drops_low = DependentVar(
        sym="A_drops_low",
        name="Frontal Area (Low Drops)",
        eqn="{A_drops_low} == {C_drops_low}*{m}**0.594",
        unit=area,
        doc="Frontal area when the cyclist is in the low drops position",
    )

    A_aero = DependentVar(
        sym="A_aero",
        name="Frontal Area (Aero)",
        eqn="{A_aero} == {C_aero}*{m}**0.762",
        unit=area,
        doc="Frontal area when the cyclist is in the aero position",
    )

_names = FrontalArea()

class FrontalAreaCalc(TopologicalSolver):
    """An example of a solver that extends TopologicalSolver."""
    # You can add additional methods or override existing ones here
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_component(cls, *children, **props) -> rx.Component:
        super().get_component(*children, **props)

        return rx.card(
            rx.vstack(
                rx.heading("Frontal Area Calculator"),
                input_with_units(cls.variables[_names.m], cls.on_value_change, cls.input_unit_change),
                output_with_units(cls.variables[_names.A_hoods], cls.output_unit_change),
                output_with_units(cls.variables[_names.A_drops], cls.output_unit_change),
                output_with_units(cls.variables[_names.A_tops], cls.output_unit_change),
                output_with_units(cls.variables[_names.A_drops_low], cls.output_unit_change),
                output_with_units(cls.variables[_names.A_aero], cls.output_unit_change),
            ),
            width="320px",
        )

frontal_area_calc = FrontalAreaCalc.create(variables=_names)
