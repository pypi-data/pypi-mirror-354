# OpenBlas and libresample should already be installed on Ubuntu
# apt install -y libopenblas-dev libresample1 libresample-dev
# you can check executing this "ldconfig -p | grep blas" and "ldconfig -p | grep resample"
set(KRISP_THIRDPARTY_LIBS
	blas
	lapack
	resample
)