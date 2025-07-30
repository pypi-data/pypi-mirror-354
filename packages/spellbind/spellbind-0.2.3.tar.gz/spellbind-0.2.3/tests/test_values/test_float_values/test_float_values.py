import gc

from spellbind.float_values import FloatConstant, MaxFloatValues, MinFloatValues, FloatVariable
from spellbind.values import SimpleVariable


def test_float_constant_str():
    const = FloatConstant(3.14)
    assert str(const) == "3.14"


def test_max_float_values():
    a = SimpleVariable(10.5)
    b = SimpleVariable(20.3)
    c = SimpleVariable(5.7)

    max_val = MaxFloatValues(a, b, c)
    assert max_val.value == 20.3

    a.value = 30.1
    assert max_val.value == 30.1


def test_max_float_values_with_literals():
    a = SimpleVariable(10.5)

    max_val = MaxFloatValues(a, 25.7, 15.2)
    assert max_val.value == 25.7

    a.value = 30.1
    assert max_val.value == 30.1


def test_min_float_values():
    a = SimpleVariable(10.5)
    b = SimpleVariable(20.3)
    c = SimpleVariable(5.7)

    min_val = MinFloatValues(a, b, c)
    assert min_val.value == 5.7

    c.value = 2.1
    assert min_val.value == 2.1


def test_min_float_values_with_literals():
    a = SimpleVariable(10.5)

    min_val = MinFloatValues(a, 25.7, 15.2)
    assert min_val.value == 10.5

    a.value = 5.1
    assert min_val.value == 5.1


def test_add_float_values_keeps_reference():
    v0 = FloatVariable(1.5)
    v1 = FloatVariable(2.5)
    v2 = v0 + v1
    assert len(v0._on_change._subscriptions) == 1
    gc.collect()

    v0.value = 3.5
    assert len(v0._on_change._subscriptions) == 1


def test_add_int_values_garbage_collected():
    v0 = FloatVariable(1.5)
    v1 = FloatVariable(2.5)
    v2 = v0 + v1
    assert len(v0._on_change._subscriptions) == 1
    assert len(v1._on_change._subscriptions) == 1
    v2 = None
    gc.collect()
    v0.value = 3.5  # trigger removal of weak references
    v1.value = 4.5  # trigger removal of weak references
    assert len(v0._on_change._subscriptions) == 0
    assert len(v1._on_change._subscriptions) == 0


def test_clamp_float_values_in_range():
    value = FloatVariable(15.5)
    min_val = FloatVariable(10.0)
    max_val = FloatVariable(20.0)

    clamped = value.clamp(min_val, max_val)
    assert clamped.value == 15.5


def test_clamp_float_values_below_min():
    value = FloatVariable(5.2)
    min_val = FloatVariable(10.0)
    max_val = FloatVariable(20.0)

    clamped = value.clamp(min_val, max_val)
    assert clamped.value == 10.0


def test_clamp_float_values_above_max():
    value = FloatVariable(25.8)
    min_val = FloatVariable(10.0)
    max_val = FloatVariable(20.0)

    clamped = value.clamp(min_val, max_val)
    assert clamped.value == 20.0


def test_clamp_float_values_with_literals_in_range():
    value = FloatVariable(15.5)

    clamped = value.clamp(10.0, 20.0)
    assert clamped.value == 15.5


def test_clamp_float_values_with_literals_below_min():
    value = FloatVariable(5.2)

    clamped = value.clamp(10.0, 20.0)
    assert clamped.value == 10.0


def test_clamp_float_values_with_literals_above_max():
    value = FloatVariable(25.8)

    clamped = value.clamp(10.0, 20.0)
    assert clamped.value == 20.0


def test_clamp_float_values_reactive_value_changes():
    value = FloatVariable(15.5)
    min_val = FloatVariable(10.0)
    max_val = FloatVariable(20.0)

    clamped = value.clamp(min_val, max_val)
    assert clamped.value == 15.5

    value.value = 5.2
    assert clamped.value == 10.0

    value.value = 25.8
    assert clamped.value == 20.0

    value.value = 12.3
    assert clamped.value == 12.3


def test_clamp_float_values_reactive_bounds_changes():
    value = FloatVariable(15.5)
    min_val = FloatVariable(10.0)
    max_val = FloatVariable(20.0)

    clamped = value.clamp(min_val, max_val)
    assert clamped.value == 15.5

    min_val.value = 18.0
    assert clamped.value == 18.0

    min_val.value = 11.0
    assert clamped.value == 15.5

    max_val.value = 12.0
    assert clamped.value == 12.0
