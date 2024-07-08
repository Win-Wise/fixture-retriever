rmdir /s /q python
mkdir python
pip3 install -r requirements.txt -t python/
xcopy arbhelpers python\arbhelpers /E /I
tar -acf ./target/lambda_layer.zip python