rmdir /s /q python
mkdir python
pip3 install  --platform manylinux2014_x86_64 --only-binary=:all: -r requirements.txt -t python/

xcopy arbhelpers python\arbhelpers /E /I
tar -acf ./target/lambda_layer.zip python