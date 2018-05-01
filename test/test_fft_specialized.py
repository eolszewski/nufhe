import numpy

from tfhe.fft_specialized import RFFT, IRFFT, RTFFT, IRTFFT


def test_rfft(thread):

    N = 1024
    a = numpy.random.normal(size=(10, N))

    res_ref = numpy.fft.rfft(a)

    a_dev = thread.to_device(a)
    res_dev = thread.empty_like(res_ref)

    rfft = RFFT(a_dev).compile(thread)

    rfft(res_dev, a_dev)
    res_test = res_dev.get()

    assert numpy.allclose(res_test, res_ref)


def test_irfft(thread):

    N = 1024
    a = numpy.random.normal(size=(10, N // 2 + 1)) + 1j * numpy.random.normal(size=(10, N // 2 + 1))

    res_ref = numpy.fft.irfft(a)

    a_dev = thread.to_device(a)
    res_dev = thread.empty_like(res_ref)

    rfft = IRFFT(a_dev).compile(thread)

    rfft(res_dev, a_dev)
    res_test = res_dev.get()

    assert numpy.allclose(res_test, res_ref)


def test_rtfft(thread):

    N = 1024
    a = numpy.random.normal(size=(10, N))

    a_double = numpy.concatenate([a, -a], axis=1)
    res_ref = numpy.ascontiguousarray(numpy.fft.rfft(a_double)[:,1::2])

    a_dev = thread.to_device(a)
    res_dev = thread.empty_like(res_ref)

    rtfft = RTFFT(a_dev).compile(thread)

    rtfft(res_dev, a_dev)
    res_test = res_dev.get()

    assert numpy.allclose(res_test, res_ref)


def test_irtfft(thread):

    N = 1024
    batch = 10
    a = numpy.random.normal(size=(batch, N // 4)) + 1j * numpy.random.normal(size=(batch, N // 4))

    a_full = numpy.zeros((batch, N // 2 + 1), a.dtype)
    a_full[:,1::2] = a
    res_ref = numpy.fft.irfft(a_full)[:,:N//2]

    a_dev = thread.to_device(a)
    irtfft = IRTFFT(a_dev).compile(thread)
    res_dev = thread.empty_like(irtfft.parameter.output)

    irtfft(res_dev, a_dev)
    res_test = res_dev.get()

    assert numpy.allclose(res_test, res_ref)
