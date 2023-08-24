import numpy as np
from tsdpe import OrderDomainNormalisation


def test_fit_parameters():
    o = OrderDomainNormalisation()
    o.fit_parameters(fs=1000, bandwidth_orders=10)
    assert o.fitted_fs == 1000
    assert o.bandwidth_orders == 10
    assert o.fft_size == 1024

def test_transform():
    o = OrderDomainNormalisation()
    o.fit_parameters(fs=1000, bandwidth_orders=10)

    # Create some mock data
    data = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1])

    # Transform the data
    order_axis, results = o.transform(data, fs=1000, fo=50)

    # Now check that the outputs are what you expect. This is just an example,
    # replace these checks with whatever makes sense for your application.
    print("Length of order axis:",len(order_axis))
    print("Length of results:",results.shape)
    assert len(order_axis) == o.fft_size // 2 + 1
    assert results.shape == (o.fft_size // 2 + 1, 1)

# Add more tests to validate other aspects of the class