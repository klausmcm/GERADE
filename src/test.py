from pystrich.datamatrix import DataMatrixEncoder

encoder = DataMatrixEncoder("random data")
encoder.save("/home/klaus/sample.png")
print(encoder.get_ascii())