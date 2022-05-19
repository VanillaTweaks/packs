# The base number for all Vanilla Tweaks `CustomModelData` values.
CUSTOM_MODEL_DATA_BASE = 880000


def custom_model_data(value: int):
    """Gets an absolute `CustomModelData` value from a value from 0 to 9999.

    >>> customModelData(3)
    880003
    """

    if value not in range(10000):
        raise ValueError(
            "The following `CustomModelData` value is not an integer from 0 to 9999: "
            + str(value)
        )

    return CUSTOM_MODEL_DATA_BASE + value
